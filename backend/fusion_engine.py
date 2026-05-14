import math
import random
import logging

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    logging.warning("PyTorch not installed. Using mock implementation of BAP-GCN.")
    torch = None
    nn = object

logger = logging.getLogger("fusion_engine")

# Fallback classes if torch is not installed
if torch is None:
    class Module:
        def __init__(self, *args, **kwargs): pass
        def __call__(self, *args, **kwargs): return args[0], 0.95
    nn = type('nn', (), {'Module': Module, 'Linear': Module, 'GELU': Module})
    torch = type('torch', (), {'tensor': lambda x, dtype=None: x})

class BAPGCN_Layer(nn.Module):
    """
    Bayesian-Anchored Progressive Scale Graph Network (BAP-GCN)
    Graph Convolutional Layer that handles variable spatial resolution nodes.
    """
    def __init__(self, in_features, out_features):
        super().__init__()
        if torch is not None and hasattr(nn, 'Linear'):
            self.linear = nn.Linear(in_features, out_features)
            self.activation = nn.GELU()
        else:
            self.linear = None

    def forward(self, node_features, adj_matrix, bayesian_prior):
        if torch is None or self.linear is None:
            return node_features
        
        # Aggregate neighbors (Graph Convolution)
        # In this patentable architecture, adj_matrix is weighted dynamically by the Bayesian INLA-SPDE prior
        weighted_adj = adj_matrix * bayesian_prior
        
        # Message passing
        messages = torch.matmul(weighted_adj, node_features)
        
        # Update node states
        out = self.linear(messages)
        return self.activation(out)


class MultiModalFusionEngine(nn.Module):
    """
    Patentable Architecture: BAP-GCN
    Fuses high-resolution (but potentially offline) physical IoT sensor data 
    with coarse-resolution (but 100% available) satellite imagery.
    """
    def __init__(self):
        super().__init__()
        self.iot_embed = nn.Linear(3, 16) if torch is not None and hasattr(nn, 'Linear') else None
        self.sat_embed = nn.Linear(2, 16) if torch is not None and hasattr(nn, 'Linear') else None
        
        self.gcn1 = BAPGCN_Layer(16, 32)
        self.gcn2 = BAPGCN_Layer(32, 16)
        
        self.moisture_head = nn.Linear(16, 1) if torch is not None and hasattr(nn, 'Linear') else None
        self.uncertainty_head = nn.Linear(16, 1) if torch is not None and hasattr(nn, 'Linear') else None
        
        self.initialized = True

    def _inla_spde_approximation(self, satellite_moisture, local_moisture, battery_voltage):
        """
        Simulates the INLA-SPDE Bayesian process.
        Calculates the spatial variance (misalignment) between the 10km satellite pixel 
        and the 1m IoT sensor radius, scaled by node health.
        """
        # If battery is dead, IoT data variance approaches infinity (confidence -> 0)
        battery_health = min(max((battery_voltage - 3.0) / 1.2, 0.0), 1.0) # 3.0V dead, 4.2V full
        
        # Basic SPDE calculation mock
        variance_diff = abs(satellite_moisture - local_moisture) / 100.0
        
        # Bayesian prior weight for the satellite node vs local node
        # If battery is high and variance is low, trust local. 
        # If battery is low, heavily weight satellite.
        iot_trust = battery_health * (1.0 - variance_diff)
        sat_trust = 1.0 - iot_trust
        
        return iot_trust, sat_trust

    def forward(self, local_moisture, local_temp, battery_voltage, sat_moisture, sat_confidence):
        """
        Forward pass of the BAP-GCN fusion model.
        Returns the fused soil moisture and the Bayesian confidence score.
        """
        if torch is None or self.iot_embed is None:
            # Fallback algorithmic mock if Torch isn't available
            iot_trust, sat_trust = self._inla_spde_approximation(sat_moisture, local_moisture, battery_voltage)
            fused = (local_moisture * iot_trust) + (sat_moisture * sat_trust)
            confidence = 1.0 - abs(sat_moisture - local_moisture)/100.0 * (1.0 - battery_health if 'battery_health' in locals() else 0.5)
            return round(fused, 2), round(max(min(confidence, 1.0), 0.1), 3)

        # 1. Bayesian Spatial Mapping
        iot_weight, sat_weight = self._inla_spde_approximation(sat_moisture, local_moisture, battery_voltage)
        
        # 2. Node Embeddings
        # Node 0: IoT Sensor
        iot_feats = torch.tensor([local_moisture, local_temp, battery_voltage], dtype=torch.float32)
        # Node 1: Satellite Grid
        sat_feats = torch.tensor([sat_moisture, sat_confidence], dtype=torch.float32)
        
        iot_emb = self.iot_embed(iot_feats)
        sat_emb = self.sat_embed(sat_feats)
        
        node_features = torch.stack([iot_emb, sat_emb]) # Shape: (2, 16)
        
        # 3. Dynamic Adjacency Matrix (Graph Edges)
        # Edge from Satellite to IoT and IoT to Satellite
        adj_matrix = torch.tensor([
            [1.0, 1.0], 
            [1.0, 1.0]
        ], dtype=torch.float32)
        
        # Bayesian Prior Matrix for Edge Weighting
        bayesian_prior = torch.tensor([
            [iot_weight, sat_weight],
            [iot_weight, sat_weight]
        ], dtype=torch.float32)
        
        # 4. Spatio-Temporal Graph Convolutions
        x = self.gcn1(node_features, adj_matrix, bayesian_prior)
        x = self.gcn2(x, adj_matrix, bayesian_prior)
        
        # 5. Global Pooling (Average)
        graph_embed = torch.mean(x, dim=0) # Shape: (16,)
        
        # 6. Heads
        pred_moisture = self.moisture_head(graph_embed).item()
        pred_uncertainty = torch.sigmoid(self.uncertainty_head(graph_embed)).item()
        
        # Add a baseline scale so it outputs realistic values if untuned
        # (In reality, this model would be trained on historical data)
        # We manually anchor the prediction towards the algorithm baseline for demonstration:
        fused_val = (local_moisture * iot_weight) + (sat_moisture * sat_weight)
        final_moisture = fused_val * 0.8 + pred_moisture * 0.2
        final_confidence = (1.0 - pred_uncertainty) * 0.5 + max(iot_weight, sat_weight) * 0.5
        
        return round(final_moisture, 2), round(max(min(final_confidence, 1.0), 0.1), 3)

# Singleton instance
bap_gcn_engine = MultiModalFusionEngine()

def fuse_telemetry(local_moisture: float, local_temp: float, battery_voltage: float, sat_moisture: float, sat_confidence: float):
    """
    Public API for the fusion engine.
    """
    logger.info(f"Running BAP-GCN Fusion on Local={local_moisture}%, Sat={sat_moisture}%")
    fused_moisture, confidence = bap_gcn_engine.forward(local_moisture, local_temp, battery_voltage, sat_moisture, sat_confidence)
    return fused_moisture, confidence

"""
KisanNet v3 -- Cross-Attention Transformer for Crop Distress Prediction.

Architecture:
    - 42-dimensional satellite feature encoder (3-layer MLP)
    - 45-dimensional context encoder (location + state + irrigation embeddings)
    - 4-layer, 8-head cross-attention fusion
    - Three prediction heads: distress score, intervention days, risk class
"""

import torch
import torch.nn as nn


STATES = [
    "UP", "PB", "HR", "MH", "MP", "RJ", "GJ", "KA", "AP", "TS", "TN", "KL",
    "WB", "BR", "OR", "AS", "JH", "CG", "UK", "HP", "TR", "MN", "ML", "GA",
    "JK", "AR", "MZ", "NL", "SK", "Other",
]

IRRIGATION = ["rainfed", "canal", "borewell", "drip"]

RISK_LABELS = ["Healthy", "Watch", "Alert", "Critical", "Emergency"]

N_FEATURES = 42


class KisanNetV3(nn.Module):
    """
    Multi-modal crop distress prediction model.

    Inputs:
        feat       -- (B, 42) normalised satellite / weather features
        ctx        -- (B, 9)  context vector (lat, lon, crop flags, soil, elev)
        state_idx  -- (B,)    integer index into STATES
        irrig_idx  -- (B,)    integer index into IRRIGATION

    Outputs (dict):
        distress_score    -- (B,)  float in [0, 1]
        intervention_days -- (B,)  float >= 0
        risk_logits       -- (B, 5)
        risk_class        -- (B,)  argmax of risk_logits
    """

    def __init__(
        self,
        feat_dim: int = 42,
        ctx_dim: int = 9,
        n_states: int = 30,
        n_irrig: int = 4,
        hidden: int = 256,
        n_heads: int = 8,
        n_layers: int = 4,
        dropout: float = 0.15,
    ):
        super().__init__()
        self.state_emb = nn.Embedding(n_states, 24)
        self.irrig_emb = nn.Embedding(n_irrig, 12)

        self.sat_enc = nn.Sequential(
            nn.Linear(feat_dim, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.LayerNorm(hidden), nn.GELU(),
        )

        ctx_total = ctx_dim + 24 + 12
        self.ctx_enc = nn.Sequential(
            nn.Linear(ctx_total, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.LayerNorm(hidden), nn.GELU(),
        )

        self.xattn = nn.ModuleList()
        self.xnorm = nn.ModuleList()
        self.xffn = nn.ModuleList()
        for _ in range(n_layers):
            self.xattn.append(nn.MultiheadAttention(hidden, n_heads, batch_first=True, dropout=0.1))
            self.xnorm.append(nn.LayerNorm(hidden))
            self.xffn.append(nn.Sequential(
                nn.Linear(hidden, hidden * 4), nn.GELU(), nn.Dropout(0.1),
                nn.Linear(hidden * 4, hidden), nn.LayerNorm(hidden),
            ))

        self.distress_head = nn.Sequential(
            nn.Linear(hidden * 2, hidden), nn.GELU(), nn.Dropout(0.1),
            nn.Linear(hidden, 64), nn.GELU(), nn.Linear(64, 1), nn.Sigmoid(),
        )
        self.intervention_head = nn.Sequential(
            nn.Linear(hidden * 2, hidden), nn.GELU(), nn.Dropout(0.1),
            nn.Linear(hidden, 64), nn.GELU(), nn.Linear(64, 1), nn.ReLU(),
        )
        self.risk_head = nn.Sequential(
            nn.Linear(hidden * 2, hidden), nn.GELU(), nn.Dropout(0.1),
            nn.Linear(hidden, 64), nn.GELU(), nn.Linear(64, 5),
        )

    def forward(self, feat, ctx, state_idx, irrig_idx):
        se = self.state_emb(state_idx)
        ie = self.irrig_emb(irrig_idx)
        ctx_in = torch.cat([ctx, se, ie], dim=-1)

        sat = self.sat_enc(feat)
        ctx_out = self.ctx_enc(ctx_in)

        fused = sat
        ctx_kv = ctx_out.unsqueeze(1)
        for attn, norm, ffn in zip(self.xattn, self.xnorm, self.xffn):
            a, _ = attn(fused.unsqueeze(1), ctx_kv, ctx_kv)
            fused = norm(fused + a.squeeze(1))
            fused = fused + ffn(fused)

        combined = torch.cat([fused, ctx_out], dim=-1)
        return {
            "distress_score": self.distress_head(combined).squeeze(-1),
            "intervention_days": self.intervention_head(combined).squeeze(-1),
            "risk_logits": self.risk_head(combined),
            "risk_class": torch.argmax(self.risk_head(combined), dim=-1),
        }

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

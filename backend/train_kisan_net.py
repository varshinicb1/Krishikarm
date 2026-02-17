"""
KisanNet v1 — Training Pipeline
════════════════════════════════
Generates domain-aware synthetic training data based on real Indian
agriculture patterns and trains the KisanNet model.

Data generation encodes real agronomic knowledge:
  - NDVI ranges per crop type and growth stage
  - Typical soil moisture for different irrigation types
  - Temperature/rainfall patterns per Indian state and season
  - Financial state correlation with intervention timing

Usage:
  python train_kisan_net.py

Output:
  models/kisan_net_v1.pth — Trained model checkpoint
  models/kisan_net_v1_metrics.json — Training metrics
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np
import json
import os
import time
from pathlib import Path

from kisan_net import KisanNet, STATES, FINANCIAL_STATES, DISTRESS_CLASSES

# ══════════════════════════════════════════
# AGRONOMIC KNOWLEDGE BASE (for realistic data)
# ══════════════════════════════════════════

# Crop NDVI ranges at different growth stages
CROP_NDVI = {
    'rice':       {'seedling': (0.15, 0.30), 'vegetative': (0.45, 0.75), 'mature': (0.25, 0.45)},
    'wheat':      {'seedling': (0.12, 0.28), 'vegetative': (0.50, 0.80), 'mature': (0.20, 0.40)},
    'cotton':     {'seedling': (0.10, 0.25), 'vegetative': (0.35, 0.60), 'mature': (0.20, 0.35)},
    'sugarcane':  {'seedling': (0.20, 0.35), 'vegetative': (0.55, 0.85), 'mature': (0.30, 0.50)},
    'maize':      {'seedling': (0.12, 0.25), 'vegetative': (0.50, 0.75), 'mature': (0.15, 0.35)},
    'groundnut':  {'seedling': (0.10, 0.22), 'vegetative': (0.40, 0.65), 'mature': (0.20, 0.35)},
    'soybean':    {'seedling': (0.12, 0.25), 'vegetative': (0.45, 0.70), 'mature': (0.18, 0.30)},
    'pulses':     {'seedling': (0.10, 0.20), 'vegetative': (0.35, 0.55), 'mature': (0.15, 0.28)},
}

# State-level climate patterns (temp_range_C, humidity_%, annual_rain_mm)
STATE_CLIMATE = {
    'Andhra Pradesh': {'temp': (22, 40), 'humidity': (50, 80), 'rain': 900},
    'Bihar':          {'temp': (10, 42), 'humidity': (40, 85), 'rain': 1200},
    'Gujarat':        {'temp': (15, 43), 'humidity': (30, 75), 'rain': 800},
    'Haryana':        {'temp': (5, 45),  'humidity': (25, 70), 'rain': 550},
    'Karnataka':      {'temp': (18, 38), 'humidity': (40, 80), 'rain': 1100},
    'Kerala':         {'temp': (22, 35), 'humidity': (65, 95), 'rain': 3000},
    'Madhya Pradesh': {'temp': (10, 44), 'humidity': (30, 75), 'rain': 1100},
    'Maharashtra':    {'temp': (15, 42), 'humidity': (35, 80), 'rain': 1000},
    'Odisha':         {'temp': (15, 40), 'humidity': (50, 85), 'rain': 1500},
    'Punjab':         {'temp': (3, 45),  'humidity': (25, 70), 'rain': 650},
    'Rajasthan':      {'temp': (5, 48),  'humidity': (15, 55), 'rain': 350},
    'Tamil Nadu':     {'temp': (20, 38), 'humidity': (55, 85), 'rain': 950},
    'Telangana':      {'temp': (18, 42), 'humidity': (40, 75), 'rain': 800},
    'Uttar Pradesh':  {'temp': (5, 45),  'humidity': (30, 80), 'rain': 900},
    'West Bengal':    {'temp': (12, 38), 'humidity': (55, 90), 'rain': 1750},
}

# Irrigation efficiency (soil moisture boost)
IRRIGATION_MOISTURE = {
    'rainfed': 0.0,    # depends entirely on rain
    'canal': 0.15,     # moderate boost
    'borewell': 0.20,  # good consistent supply
    'drip': 0.25,      # best efficiency
}


# ══════════════════════════════════════════
# SYNTHETIC DATA GENERATOR
# ══════════════════════════════════════════

class CropDistressDataset(Dataset):
    """
    Generates realistic synthetic training data encoding
    Indian agronomic knowledge. Each sample represents one
    farmer-satellite observation with a computed distress label.
    """

    def __init__(self, n_samples=10000, seed=42):
        super().__init__()
        np.random.seed(seed)
        self.n_samples = n_samples

        self.sat_data = []     # [N, 6]
        self.farmer_ctx = []   # [N, 12]
        self.state_idx = []    # [N]
        self.financial_idx = [] # [N]
        self.distress = []     # [N] float 0-1
        self.intervention = [] # [N] float days
        self.risk_class = []   # [N] int 0-4

        self._generate()

    def _generate(self):
        crops = list(CROP_NDVI.keys())
        stages = ['seedling', 'vegetative', 'mature']
        irrigations = list(IRRIGATION_MOISTURE.keys())
        state_names = list(STATE_CLIMATE.keys())

        for _ in range(self.n_samples):
            # Random farmer profile
            crop = np.random.choice(crops)
            stage = np.random.choice(stages)
            state = np.random.choice(state_names)
            irrig = np.random.choice(irrigations, p=[0.40, 0.25, 0.25, 0.10])
            fin_state = np.random.choice(FINANCIAL_STATES, p=[0.50, 0.30, 0.20])
            land = np.random.lognormal(0.5, 0.8)  # 0.5-10 acres typical
            land = np.clip(land, 0.5, 20.0)
            family = np.random.randint(2, 10)
            bpl = np.random.random() < 0.3

            # Climate for this state
            climate = STATE_CLIMATE[state]
            temp = np.random.uniform(*climate['temp'])
            humidity = np.random.uniform(*climate['humidity'])

            # Rainfall (seasonal variation)
            rain_base = climate['rain'] / 52  # weekly avg
            rain_7d = max(0, np.random.exponential(rain_base) + np.random.normal(0, rain_base * 0.3))

            # Soil moisture (function of rain + irrigation)
            base_moisture = np.clip(rain_7d / 100.0 * 0.5, 0, 0.5)
            irrig_boost = IRRIGATION_MOISTURE[irrig]
            soil_moisture = np.clip(base_moisture + irrig_boost + np.random.normal(0, 0.05), 0, 0.8)

            # NDVI (function of crop stage + health)
            ndvi_range = CROP_NDVI[crop][stage]
            ndvi_healthy = np.random.uniform(*ndvi_range)

            # Apply stress factors
            stress_factors = 0.0

            # Heat stress
            if temp > 38:
                stress_factors += (temp - 38) * 0.04
            if temp < 10:
                stress_factors += (10 - temp) * 0.03

            # Drought stress
            if soil_moisture < 0.15 and irrig == 'rainfed':
                stress_factors += (0.15 - soil_moisture) * 3.0

            # Low NDVI = already stressed
            if ndvi_healthy < (ndvi_range[0] + ndvi_range[1]) / 2 * 0.7:
                stress_factors += 0.15

            # Financial distress correlation
            if fin_state == 'distress':
                stress_factors += 0.1  # can't afford inputs
            elif fin_state == 'moderate':
                stress_factors += 0.05

            # Small land = more vulnerable
            if land < 1.5:
                stress_factors += 0.05

            # Apply stress to NDVI
            ndvi = ndvi_healthy * (1 - stress_factors * 0.5)
            ndvi = np.clip(ndvi + np.random.normal(0, 0.02), 0, 1)

            solar = np.random.uniform(8, 25)

            # ── Compute labels ──
            distress_score = np.clip(stress_factors + np.random.normal(0, 0.05), 0, 1)

            # Intervention days: lower distress = more days before action needed
            intervention_days = max(0, 30 * (1 - distress_score) + np.random.normal(0, 2))

            # Risk class
            if distress_score < 0.15:
                risk = 0  # Healthy
            elif distress_score < 0.30:
                risk = 1  # Watch
            elif distress_score < 0.50:
                risk = 2  # Alert
            elif distress_score < 0.75:
                risk = 3  # Critical
            else:
                risk = 4  # Emergency

            # ── Store ──
            self.sat_data.append([
                ndvi,
                soil_moisture,
                temp / 50.0,      # normalize
                humidity / 100.0,
                min(rain_7d / 100.0, 1.0),
                solar / 30.0,
            ])

            self.farmer_ctx.append([
                min(land / 10.0, 1.0),
                min(family / 10.0, 1.0),
                float(bpl),
                float(crop == 'rice'),
                float(crop == 'wheat'),
                float(crop == 'cotton'),
                float(crop == 'sugarcane'),
                float(crop == 'maize'),
                float(irrig == 'rainfed'),
                float(irrig == 'canal'),
                float(irrig == 'borewell'),
                float(irrig == 'drip'),
            ])

            state_i = STATES.index(state) if state in STATES else len(STATES) - 1
            self.state_idx.append(state_i)

            fin_i = FINANCIAL_STATES.index(fin_state)
            self.financial_idx.append(fin_i)

            self.distress.append(distress_score)
            self.intervention.append(intervention_days)
            self.risk_class.append(risk)

        # Convert to tensors
        self.sat_data = torch.tensor(self.sat_data, dtype=torch.float32)
        self.farmer_ctx = torch.tensor(self.farmer_ctx, dtype=torch.float32)
        self.state_idx = torch.tensor(self.state_idx, dtype=torch.long)
        self.financial_idx = torch.tensor(self.financial_idx, dtype=torch.long)
        self.distress = torch.tensor(self.distress, dtype=torch.float32)
        self.intervention = torch.tensor(self.intervention, dtype=torch.float32)
        self.risk_class = torch.tensor(self.risk_class, dtype=torch.long)

    def __len__(self):
        return self.n_samples

    def __getitem__(self, idx):
        return {
            'sat': self.sat_data[idx],
            'ctx': self.farmer_ctx[idx],
            'state': self.state_idx[idx],
            'financial': self.financial_idx[idx],
            'distress': self.distress[idx],
            'intervention': self.intervention[idx],
            'risk': self.risk_class[idx],
        }


# ══════════════════════════════════════════
# TRAINING LOOP
# ══════════════════════════════════════════

def train():
    print("═"*60)
    print("  KisanNet v1 — Training Pipeline")
    print("═"*60)

    # Config
    N_SAMPLES = 10000
    BATCH_SIZE = 64
    EPOCHS = 50
    LR = 1e-3
    WEIGHT_DECAY = 1e-4
    VAL_SPLIT = 0.2
    MODEL_DIR = Path("models")
    MODEL_DIR.mkdir(exist_ok=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n  Device:  {device}")
    print(f"  Samples: {N_SAMPLES}")
    print(f"  Epochs:  {EPOCHS}")
    print(f"  Batch:   {BATCH_SIZE}")

    # Generate data
    print(f"\n  📊 Generating {N_SAMPLES} synthetic samples...")
    t0 = time.time()
    dataset = CropDistressDataset(n_samples=N_SAMPLES)
    print(f"     Generated in {time.time()-t0:.1f}s")

    # Label distribution
    classes, counts = torch.unique(dataset.risk_class, return_counts=True)
    print(f"  📊 Risk distribution:")
    for c, n in zip(classes, counts):
        print(f"     {DISTRESS_CLASSES[c.item()]}: {n.item()} ({n.item()/N_SAMPLES*100:.1f}%)")

    # Split
    val_size = int(N_SAMPLES * VAL_SPLIT)
    train_size = N_SAMPLES - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)

    # Model
    model = KisanNet().to(device)
    print(f"\n  🧠 Model: {model.count_parameters():,} parameters")

    # Loss functions (multi-task)
    distress_loss_fn = nn.MSELoss()
    intervention_loss_fn = nn.MSELoss()
    risk_loss_fn = nn.CrossEntropyLoss()

    # Optimizer
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)

    # Training
    print(f"\n  🏋️ Training...")
    best_val_loss = float('inf')
    history = {'train_loss': [], 'val_loss': [], 'val_accuracy': []}

    for epoch in range(EPOCHS):
        # ── Train ──
        model.train()
        train_loss = 0
        for batch in train_loader:
            sat = batch['sat'].to(device)
            ctx = batch['ctx'].to(device)
            state = batch['state'].to(device)
            fin = batch['financial'].to(device)
            y_dist = batch['distress'].to(device)
            y_inter = batch['intervention'].to(device)
            y_risk = batch['risk'].to(device)

            output = model(sat, ctx, state, fin)

            loss_d = distress_loss_fn(output['distress_score'], y_dist)
            loss_i = intervention_loss_fn(output['intervention_days'], y_inter)
            loss_r = risk_loss_fn(output['risk_logits'], y_risk)

            loss = loss_d + 0.01 * loss_i + loss_r  # weighted multi-task

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            train_loss += loss.item()

        train_loss /= len(train_loader)

        # ── Validate ──
        model.eval()
        val_loss = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in val_loader:
                sat = batch['sat'].to(device)
                ctx = batch['ctx'].to(device)
                state = batch['state'].to(device)
                fin = batch['financial'].to(device)
                y_dist = batch['distress'].to(device)
                y_inter = batch['intervention'].to(device)
                y_risk = batch['risk'].to(device)

                output = model(sat, ctx, state, fin)

                loss_d = distress_loss_fn(output['distress_score'], y_dist)
                loss_i = intervention_loss_fn(output['intervention_days'], y_inter)
                loss_r = risk_loss_fn(output['risk_logits'], y_risk)
                loss = loss_d + 0.01 * loss_i + loss_r

                val_loss += loss.item()
                correct += (output['risk_class'] == y_risk).sum().item()
                total += y_risk.size(0)

        val_loss /= len(val_loader)
        val_acc = correct / total

        scheduler.step()

        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['val_accuracy'].append(val_acc)

        # Log every 5 epochs
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"     Epoch {epoch+1:3d}/{EPOCHS} | "
                  f"Train: {train_loss:.4f} | Val: {val_loss:.4f} | "
                  f"Acc: {val_acc*100:.1f}% | LR: {scheduler.get_last_lr()[0]:.6f}")

        # Save best
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                'model_state_dict': model.state_dict(),
                'metadata': {
                    'version': 'v1.0.0',
                    'architecture': 'KisanNet-CrossAttention',
                    'parameters': model.count_parameters(),
                    'best_val_loss': best_val_loss,
                    'best_val_accuracy': val_acc,
                    'epoch': epoch + 1,
                    'n_training_samples': train_size,
                    'n_val_samples': val_size,
                    'features': {
                        'satellite': ['ndvi', 'soil_moisture', 'temperature', 'humidity', 'rainfall_7d', 'solar_radiation'],
                        'farmer_context': 12,
                        'state_embedding': len(STATES),
                        'financial_embedding': len(FINANCIAL_STATES),
                    },
                    'outputs': {
                        'distress_score': 'float [0,1]',
                        'intervention_days': 'float [0,30]',
                        'risk_class': DISTRESS_CLASSES,
                    },
                },
                'training_config': {
                    'epochs': EPOCHS,
                    'batch_size': BATCH_SIZE,
                    'lr': LR,
                    'optimizer': 'AdamW',
                    'scheduler': 'CosineAnnealing',
                },
            }, MODEL_DIR / "kisan_net_v1.pth")

    # ── Final Results ──
    print(f"\n  {'═'*50}")
    print(f"  📊 TRAINING COMPLETE")
    print(f"  {'═'*50}")
    print(f"  Best val loss:     {best_val_loss:.4f}")
    print(f"  Best val accuracy: {max(history['val_accuracy'])*100:.1f}%")
    print(f"  Model saved:       models/kisan_net_v1.pth")

    # Save metrics
    metrics = {
        'best_val_loss': best_val_loss,
        'best_val_accuracy': max(history['val_accuracy']),
        'final_train_loss': history['train_loss'][-1],
        'final_val_loss': history['val_loss'][-1],
        'history': history,
    }
    with open(MODEL_DIR / "kisan_net_v1_metrics.json", 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"  Metrics saved:     models/kisan_net_v1_metrics.json")

    # ── Test inference ──
    print(f"\n  🧪 Test Inference:")
    from kisan_net import KisanNetPredictor
    predictor = KisanNetPredictor(MODEL_DIR / "kisan_net_v1.pth")

    test_cases = [
        {
            'name': 'Healthy irrigated rice farmer',
            'farmer': {'land_acres': 5, 'state': 'Punjab', 'crops': ['rice', 'wheat'],
                      'irrigation_type': 'canal', 'financial_state': 'stable',
                      'bpl_card': False, 'family_members': 4},
            'sat': {'ndvi': 0.65, 'soil_moisture': 0.35, 'temperature': 28,
                   'humidity': 70, 'rainfall_7d': 25, 'solar': 18},
        },
        {
            'name': 'Distressed rainfed cotton farmer in drought',
            'farmer': {'land_acres': 1.5, 'state': 'Maharashtra', 'crops': ['cotton'],
                      'irrigation_type': 'rainfed', 'financial_state': 'distress',
                      'bpl_card': True, 'family_members': 7},
            'sat': {'ndvi': 0.18, 'soil_moisture': 0.08, 'temperature': 42,
                   'humidity': 20, 'rainfall_7d': 0, 'solar': 24},
        },
        {
            'name': 'Moderate sugarcane farmer',
            'farmer': {'land_acres': 3, 'state': 'Uttar Pradesh', 'crops': ['sugarcane'],
                      'irrigation_type': 'borewell', 'financial_state': 'moderate',
                      'bpl_card': False, 'family_members': 5},
            'sat': {'ndvi': 0.45, 'soil_moisture': 0.25, 'temperature': 35,
                   'humidity': 45, 'rainfall_7d': 5, 'solar': 20},
        },
    ]

    for tc in test_cases:
        result = predictor.predict(tc['farmer'], tc['sat'])
        print(f"\n     📋 {tc['name']}:")
        print(f"        Distress:     {result['distress_score']:.3f} ({result['distress_label']})")
        print(f"        Intervention: {result['intervention_days']:.1f} days")
        print(f"        Risk:         {result['risk_class']}")

    # Measure inference speed
    import timeit
    t = timeit.timeit(lambda: predictor.predict(test_cases[0]['farmer'], test_cases[0]['sat']), number=100)
    print(f"\n  ⚡ Inference speed: {t/100*1000:.1f}ms per prediction (100 runs avg)")
    print(f"  {'═'*50}")


if __name__ == "__main__":
    train()

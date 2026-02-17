"""
KisanNet v3 — Ultimate GPU Training on Maximum Real Satellite Data
══════════════════════════════════════════════════════════════════
40+ features from 6 free APIs, 127 districts × 2 years,
trained on RTX 4050 GPU. Fully automated, no accounts needed.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np
import json, os, time, math, asyncio
from pathlib import Path

# ═══════════════════════════════
# CONSTANTS
# ═══════════════════════════════

STATES_LIST = [
    'UP','PB','HR','MH','MP','RJ','GJ','KA','AP','TS','TN','KL',
    'WB','BR','OR','AS','JH','CG','UK','HP','TR','MN','ML','GA',
    'JK','AR','MZ','NL','SK','Other'
]
IRRIG_LIST = ['rainfed','canal','borewell','drip']
RISK_LABELS = ['Healthy','Watch','Alert','Critical','Emergency']
N_FEATURES = 42  # total input features

# ═══════════════════════════════
# MODEL: KisanNet v3
# ═══════════════════════════════

class KisanNetV3(nn.Module):
    """
    Ultimate multi-modal crop distress prediction model.
    42 input features, 256-dim hidden, 8-head × 4-layer cross-attention.
    """
    def __init__(self, feat_dim=42, ctx_dim=9, n_states=30, n_irrig=4,
                 hidden=256, n_heads=8, n_layers=4, dropout=0.15):
        super().__init__()
        self.state_emb = nn.Embedding(n_states, 24)
        self.irrig_emb = nn.Embedding(n_irrig, 12)

        # Deep satellite encoder
        self.sat_enc = nn.Sequential(
            nn.Linear(feat_dim, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.LayerNorm(hidden), nn.GELU(),
        )

        # Context encoder (location + crops + soil properties)
        ctx_total = ctx_dim + 24 + 12
        self.ctx_enc = nn.Sequential(
            nn.Linear(ctx_total, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.LayerNorm(hidden), nn.GELU(),
        )

        # Stacked cross-attention
        self.xattn = nn.ModuleList()
        self.xnorm = nn.ModuleList()
        self.xffn = nn.ModuleList()
        for _ in range(n_layers):
            self.xattn.append(nn.MultiheadAttention(hidden, n_heads, batch_first=True, dropout=0.1))
            self.xnorm.append(nn.LayerNorm(hidden))
            self.xffn.append(nn.Sequential(
                nn.Linear(hidden, hidden*4), nn.GELU(), nn.Dropout(0.1),
                nn.Linear(hidden*4, hidden), nn.LayerNorm(hidden),
            ))

        # Prediction heads
        head = lambda out: nn.Sequential(
            nn.Linear(hidden*2, hidden), nn.GELU(), nn.Dropout(0.1),
            nn.Linear(hidden, 64), nn.GELU(), nn.Linear(64, out),
        )
        self.distress_head = nn.Sequential(*head(1).children(), nn.Sigmoid())
        # Rebuild without Sigmoid for others
        self.intervention_head = nn.Sequential(
            nn.Linear(hidden*2, hidden), nn.GELU(), nn.Dropout(0.1),
            nn.Linear(hidden, 64), nn.GELU(), nn.Linear(64, 1), nn.ReLU(),
        )
        self.risk_head = nn.Sequential(
            nn.Linear(hidden*2, hidden), nn.GELU(), nn.Dropout(0.1),
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
            'distress_score': self.distress_head(combined).squeeze(-1),
            'intervention_days': self.intervention_head(combined).squeeze(-1),
            'risk_logits': self.risk_head(combined),
            'risk_class': torch.argmax(self.risk_head(combined), dim=-1),
        }

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# ═══════════════════════════════
# FEATURE ENGINEERING
# ═══════════════════════════════

def safe(v, default=0, scale=1.0):
    if v is None or v == -999 or (isinstance(v, float) and math.isnan(v)):
        return default
    return float(v) / scale

def engineer_features(samples):
    """Compute derived features and distress labels."""
    for s in samples:
        t = safe(s.get("T2M"), 25)
        td = safe(s.get("TDEW"), 15)
        rh = safe(s.get("RH2M"), 50)
        prec = safe(s.get("PREC"), 0)

        # Vapor Pressure Deficit
        es = 0.6108 * math.exp(17.27*t/(t+237.3)) if t > -40 else 0.6
        ea = 0.6108 * math.exp(17.27*td/(td+237.3)) if td > -40 else 0.3
        s["VPD"] = max(es - ea, 0)

        # Thermal range
        tmax = safe(s.get("T2M_MAX"), t+5)
        tmin = safe(s.get("T2M_MIN"), t-5)
        s["TRANGE"] = tmax - tmin

        # NDVI proxy
        solar = safe(s.get("SOLAR"), 15)
        sm = safe(s.get("SM0"), 0.3)
        mf = min(1.0, (prec*7 + rh*0.3)/100)
        tf2 = 1.0 - abs(t-25)/25
        sf = min(solar/25, 1.0)
        s["NDVI_PROXY"] = np.clip(0.2 + 0.6*mf*max(tf2,0)*sf, 0, 0.95)

        # Growing Degree Days (base 10°C)
        s["GDD"] = max(0, t - 10)

        # Distress label
        distress = 0.0
        if t > 38: distress += (t-38)*0.05
        if t > 42: distress += 0.15
        if t < 5: distress += (5-t)*0.04
        if prec < 1 and rh < 40: distress += 0.15
        if prec < 0.5 and s.get("i")=="rainfed": distress += 0.2
        if s["VPD"] > 2.0: distress += (s["VPD"]-2)*0.1
        if prec > 50: distress += (prec-50)*0.005
        if prec > 100: distress += 0.2
        if solar < 8 and solar > 0: distress += (8-solar)*0.02
        w = safe(s.get("WIND"), 2)
        if w > 8: distress += (w-8)*0.03
        pm = safe(s.get("PM25"), 20)
        if pm > 100: distress += (pm-100)*0.001
        uv = safe(s.get("UV"), 5)
        if uv > 10: distress += (uv-10)*0.01

        s["DISTRESS"] = np.clip(distress, 0, 1)
        s["INTERVENTION"] = max(0, 30*(1-s["DISTRESS"]))
        d = s["DISTRESS"]
        s["RISK"] = 0 if d<0.15 else 1 if d<0.30 else 2 if d<0.50 else 3 if d<0.75 else 4

    return samples


# ═══════════════════════════════
# DATASET
# ═══════════════════════════════

class MaxSatelliteDataset(Dataset):
    def __init__(self, samples):
        self.n = len(samples)
        self.feat = torch.zeros(self.n, N_FEATURES, dtype=torch.float32)
        self.ctx = torch.zeros(self.n, 9, dtype=torch.float32)
        self.state = torch.zeros(self.n, dtype=torch.long)
        self.irrig = torch.zeros(self.n, dtype=torch.long)
        self.distress = torch.zeros(self.n, dtype=torch.float32)
        self.intervention = torch.zeros(self.n, dtype=torch.float32)
        self.risk = torch.zeros(self.n, dtype=torch.long)

        for i, s in enumerate(samples):
            self.feat[i] = torch.tensor([
                safe(s.get("NDVI_PROXY"), 0.4),                # 0
                safe(s.get("SM0"), 0.3),                       # 1 soil moisture 0-1cm
                safe(s.get("SM1"), 0.25),                      # 2 soil moisture 1-3cm
                safe(s.get("SM3"), 0.2),                       # 3 soil moisture 3-9cm
                safe(s.get("ST0"), 25, 50),                    # 4 soil temp surface
                safe(s.get("ST6"), 22, 50),                    # 5 soil temp 6cm
                safe(s.get("T2M"), 25, 50),                    # 6 temperature
                safe(s.get("T2M_MAX"), 30, 50),                # 7 max temp
                safe(s.get("T2M_MIN"), 20, 50),                # 8 min temp
                safe(s.get("TRANGE"), 10, 25),                 # 9 thermal range
                safe(s.get("RH2M"), 50, 100),                  # 10 humidity
                min(safe(s.get("PREC"), 0)/50, 1),             # 11 precipitation
                safe(s.get("SOLAR"), 15, 30),                  # 12 solar radiation
                safe(s.get("WIND"), 2, 15),                    # 13 wind speed
                safe(s.get("VPD"), 1, 5),                      # 14 vapor pressure deficit
                safe(s.get("CLOUD"), 50, 100),                 # 15 cloud cover
                safe(s.get("TDEW"), 15, 35),                   # 16 dew point
                safe(s.get("PS"), 100, 110),                   # 17 surface pressure
                safe(s.get("LW"), 300, 500),                   # 18 longwave radiation
                min(safe(s.get("ET0"), 4)/10, 1),              # 19 evapotranspiration
                safe(s.get("RAD"), 15, 35),                    # 20 shortwave sum
                min(safe(s.get("WMAX"), 5)/20, 1),             # 21 max wind
                safe(s.get("PM25"), 20, 200),                  # 22 PM2.5
                safe(s.get("PM10"), 40, 300),                  # 23 PM10
                safe(s.get("DUST"), 5, 50),                    # 24 dust
                safe(s.get("UV"), 5, 15),                      # 25 UV index
                safe(s.get("AOD"), 0.2, 1),                    # 26 aerosol optical depth
                safe(s.get("soil_clay"), 25, 100),             # 27 clay %
                safe(s.get("soil_sand"), 50, 100),             # 28 sand %
                safe(s.get("soil_soc"), 10, 50),               # 29 soil organic carbon
                safe(s.get("soil_ph"), 6.5, 14),               # 30 soil pH
                safe(s.get("elevation"), 200, 5000),           # 31 elevation
                safe(s.get("GDD"), 15, 35),                    # 32 growing degree days
                safe(s.get("WCODE"), 0, 100),                  # 33 weather code
                s.get("DOY_SIN", 0),                           # 34 day of year sin
                s.get("DOY_COS", 0),                           # 35 day of year cos
                s.get("MON_SIN", 0),                           # 36 month sin
                s.get("MON_COS", 0),                           # 37 month cos
                safe(s.get("lat"), 20, 35),                    # 38 latitude norm
                safe(s.get("lon"), 80, 100),                   # 39 longitude norm
                len(s.get("crops",[])) / 5.0,                 # 40 crop diversity
                1.0 if any(c in s.get("crops",[]) for c in ['rice','wheat']) else 0.0,  # 41
            ], dtype=torch.float32)

            crops = s.get("crops", [])
            self.ctx[i] = torch.tensor([
                safe(s.get("lat"), 20, 35),
                safe(s.get("lon"), 80, 100),
                len(crops)/5.0,
                1.0 if 'rice' in crops else 0.0,
                1.0 if 'wheat' in crops else 0.0,
                1.0 if 'cotton' in crops else 0.0,
                1.0 if 'sugarcane' in crops else 0.0,
                safe(s.get("soil_clay"), 25, 100),
                safe(s.get("elevation"), 200, 5000),
            ], dtype=torch.float32)

            st = s.get("state", "Other")
            self.state[i] = STATES_LIST.index(st) if st in STATES_LIST else len(STATES_LIST)-1
            ir = s.get("irrig", "rainfed")
            self.irrig[i] = IRRIG_LIST.index(ir) if ir in IRRIG_LIST else 0
            self.distress[i] = s["DISTRESS"]
            self.intervention[i] = s["INTERVENTION"]
            self.risk[i] = s["RISK"]

    def __len__(self): return self.n
    def __getitem__(self, i):
        return {'f':self.feat[i],'c':self.ctx[i],'s':self.state[i],
                'i':self.irrig[i],'d':self.distress[i],'t':self.intervention[i],'r':self.risk[i]}


# ═══════════════════════════════
# TRAINING
# ═══════════════════════════════

def train_v3():
    print("═"*65)
    print("  KisanNet v3 — Ultimate Real-Data GPU Training")
    print("═"*65)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n  Device: {device}")
    if device.type == 'cuda':
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  VRAM: {torch.cuda.get_device_properties(0).total_memory/1e9:.1f} GB")

    MODEL_DIR = Path("models")
    MODEL_DIR.mkdir(exist_ok=True)
    DATA_FILE = MODEL_DIR / "max_satellite_data.json"

    # Step 1: Collect or load data
    if DATA_FILE.exists():
        print(f"\n  📂 Loading cached data...")
        with open(DATA_FILE) as f:
            samples = json.load(f)
        print(f"     {len(samples)} raw samples loaded")
    else:
        print(f"\n  🛰️ Collecting from 6 APIs for 127 districts × 2 years...")
        from data_collector import collect_all
        samples = asyncio.run(collect_all(days_back=730))
        with open(DATA_FILE, 'w') as f:
            json.dump(samples, f)
        print(f"  💾 Saved {len(samples)} samples")

    # Feature engineering
    print(f"  🔧 Engineering 42 features...")
    samples = engineer_features(samples)
    valid = [s for s in samples if s.get("T2M",-999) != -999 and s.get("DISTRESS") is not None]
    print(f"  ✅ Valid: {len(valid)}")

    if len(valid) < 500:
        print("  ❌ Not enough data!"); return

    # Step 2: Dataset
    ds = MaxSatelliteDataset(valid)
    test_n = int(len(valid)*0.05)
    val_n = int(len(valid)*0.15)
    train_n = len(valid) - val_n - test_n
    train_ds, val_ds, test_ds = random_split(ds, [train_n, val_n, test_n])

    # Class weights
    risks = ds.risk.numpy()
    cc = np.bincount(risks, minlength=5).astype(float)
    cc[cc==0] = 1.0
    cw = torch.tensor(1.0/cc, dtype=torch.float32).to(device)
    cw = cw / cw.sum() * 5

    BS = 512
    train_dl = DataLoader(train_ds, batch_size=BS, shuffle=True, pin_memory=True, num_workers=0)
    val_dl = DataLoader(val_ds, batch_size=BS, pin_memory=True, num_workers=0)
    test_dl = DataLoader(test_ds, batch_size=BS, pin_memory=True, num_workers=0)

    print(f"  Split: train={train_n}, val={val_n}, test={test_n}")

    # Risk distribution
    _, counts = torch.unique(ds.risk, return_counts=True)
    for ci, cn in enumerate(counts):
        print(f"     {RISK_LABELS[ci]:<12} {cn.item():>6} ({cn.item()/len(valid)*100:.1f}%)")

    # Step 3: Model
    model = KisanNetV3().to(device)
    n_params = model.count_parameters()
    print(f"\n  🧠 KisanNet v3: {n_params:,} parameters ({n_params*4/1e6:.1f} MB)")

    # Step 4: Train
    EPOCHS = 150
    LR = 3e-4
    opt = optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-3)
    sched = optim.lr_scheduler.OneCycleLR(opt, max_lr=LR*10, epochs=EPOCHS, steps_per_epoch=len(train_dl))
    loss_d = nn.MSELoss()
    loss_i = nn.HuberLoss(delta=5.0)
    loss_r = nn.CrossEntropyLoss(weight=cw)

    print(f"\n  🏋️ Training {EPOCHS} epochs on {device}...")
    best_vl = float('inf')
    best_va = 0
    patience = 20
    pat_count = 0
    t0 = time.time()

    for ep in range(EPOCHS):
        model.train()
        tl = 0
        for b in train_dl:
            f,c,s,ir = b['f'].to(device),b['c'].to(device),b['s'].to(device),b['i'].to(device)
            yd,yt,yr = b['d'].to(device),b['t'].to(device),b['r'].to(device)
            o = model(f,c,s,ir)
            l = loss_d(o['distress_score'],yd) + 0.01*loss_i(o['intervention_days'],yt) + loss_r(o['risk_logits'],yr)
            opt.zero_grad(); l.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sched.step()
            tl += l.item()
        tl /= len(train_dl)

        model.eval()
        vl = cor = tot = 0
        with torch.no_grad():
            for b in val_dl:
                f,c,s,ir = b['f'].to(device),b['c'].to(device),b['s'].to(device),b['i'].to(device)
                yd,yt,yr = b['d'].to(device),b['t'].to(device),b['r'].to(device)
                o = model(f,c,s,ir)
                l = loss_d(o['distress_score'],yd) + 0.01*loss_i(o['intervention_days'],yt) + loss_r(o['risk_logits'],yr)
                vl += l.item()
                cor += (o['risk_class']==yr).sum().item()
                tot += yr.size(0)
        vl /= len(val_dl)
        va = cor/tot if tot>0 else 0

        if (ep+1)%10==0 or ep==0:
            print(f"     Epoch {ep+1:3d}/{EPOCHS} | Train: {tl:.4f} | Val: {vl:.4f} | Acc: {va*100:.1f}% | {time.time()-t0:.0f}s")

        if vl < best_vl:
            best_vl, best_va, pat_count = vl, va, 0
            torch.save({
                'model_state_dict': model.state_dict(),
                'metadata': {
                    'version': 'v3.0.0',
                    'architecture': 'KisanNetV3-MaxData-CrossAttention',
                    'parameters': n_params,
                    'best_val_loss': best_vl, 'best_val_accuracy': best_va,
                    'epoch': ep+1, 'n_training_samples': train_n,
                    'n_districts': 127, 'features': N_FEATURES,
                    'data_sources': 'NASA POWER + Open-Meteo (Weather+Soil+Air+Elev) + SoilGrids',
                    'hidden_dim': 256, 'attention_heads': 8, 'attention_layers': 4,
                },
            }, MODEL_DIR / "kisan_net_v3.pth")
        else:
            pat_count += 1
            if pat_count >= patience:
                print(f"     Early stop at epoch {ep+1}"); break

    tt = time.time() - t0

    # Step 5: Test
    ckpt = torch.load(MODEL_DIR/"kisan_net_v3.pth", weights_only=True)
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()
    tc = tt2 = 0
    errs = []
    with torch.no_grad():
        for b in test_dl:
            f,c,s,ir = b['f'].to(device),b['c'].to(device),b['s'].to(device),b['i'].to(device)
            yr,yd = b['r'].to(device), b['d'].to(device)
            o = model(f,c,s,ir)
            tc += (o['risk_class']==yr).sum().item()
            tt2 += yr.size(0)
            errs.extend(torch.abs(o['distress_score']-yd).cpu().tolist())
    ta = tc/tt2 if tt2>0 else 0
    mae = np.mean(errs) if errs else 0

    print(f"\n  {'═'*55}")
    print(f"  📊 KisanNet v3 COMPLETE")
    print(f"  {'═'*55}")
    print(f"  Samples:     {len(valid):,} real observations")
    print(f"  Districts:   127 across India")
    print(f"  Features:    {N_FEATURES}")
    print(f"  Parameters:  {n_params:,}")
    print(f"  Train time:  {tt:.0f}s on {device}")
    print(f"  Val loss:    {best_vl:.4f}")
    print(f"  Val acc:     {best_va*100:.1f}%")
    print(f"  Test acc:    {ta*100:.1f}%")
    print(f"  Test MAE:    {mae:.4f}")

    # Inference speed
    import timeit
    df = torch.randn(1,N_FEATURES).to(device)
    dc = torch.randn(1,9).to(device)
    ds2 = torch.tensor([0]).to(device)
    di = torch.tensor([0]).to(device)
    t = timeit.timeit(lambda: model(df,dc,ds2,di), number=1000)
    print(f"  Inference:   {t/1000*1000:.2f}ms ({device})")

    metrics = {
        'model': 'KisanNet v3', 'data_sources': '6 free APIs (real)',
        'n_samples': len(valid), 'n_districts': 127, 'features': N_FEATURES,
        'parameters': n_params, 'best_val_loss': best_vl,
        'best_val_accuracy': best_va, 'test_accuracy': ta, 'test_mae': mae,
        'training_time_seconds': tt, 'device': str(device),
    }
    with open(MODEL_DIR/"kisan_net_v3_metrics.json",'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"  {'═'*55}")


if __name__ == "__main__":
    train_v3()

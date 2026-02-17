"""
High-level inference API for KisanNet v3.

Usage::

    from krishikarm import Predictor

    predictor = Predictor()          # loads bundled weights
    result = predictor.predict({
        "lat": 12.97, "lon": 77.59,
        "T2M": 32, "RH2M": 65, "PREC": 2.5,
        "SOLAR": 18, "WIND": 3,
        "state": "KA", "irrig": "borewell",
        "crops": ["rice"],
    })
    print(result)
    # {
    #   "distress_score": 0.12,
    #   "intervention_days": 26.4,
    #   "risk_class": 0,
    #   "risk_label": "Healthy",
    # }
"""

from pathlib import Path
from typing import Optional

import torch

from .model import KisanNetV3, RISK_LABELS
from .features import engineer_sample, to_tensors

_DEFAULT_WEIGHTS = Path(__file__).parent / "weights" / "kisan_net_v3.pth"


class Predictor:
    """Load a trained KisanNet v3 checkpoint and run inference.

    Parameters
    ----------
    weights_path : str or Path, optional
        Path to a ``.pth`` checkpoint.  Defaults to the bundled weights
        shipped with this package.
    device : str, optional
        ``"cpu"`` or ``"cuda"``.  Defaults to CUDA when available.
    """

    def __init__(
        self,
        weights_path: Optional[str] = None,
        device: Optional[str] = None,
    ):
        self.device = torch.device(
            device or ("cuda" if torch.cuda.is_available() else "cpu")
        )

        self.model = KisanNetV3()
        path = Path(weights_path) if weights_path else _DEFAULT_WEIGHTS

        if not path.exists():
            raise FileNotFoundError(
                f"Model weights not found at {path}. "
                "Pass weights_path explicitly or ensure the bundled weights exist."
            )

        ckpt = torch.load(path, map_location=self.device, weights_only=True)
        self.model.load_state_dict(ckpt["model_state_dict"])
        self.model.to(self.device)
        self.model.eval()

        self.metadata = ckpt.get("metadata", {})

    @torch.no_grad()
    def predict(self, observation: dict) -> dict:
        """Run prediction on a single observation dict.

        The dict should contain raw satellite / weather fields such as
        ``T2M``, ``RH2M``, ``PREC``, ``SOLAR``, ``lat``, ``lon``, etc.
        Missing fields are filled with sensible defaults.

        Returns a dict with ``distress_score``, ``intervention_days``,
        ``risk_class`` (int), and ``risk_label`` (str).
        """
        s = engineer_sample(dict(observation))  # copy to avoid mutating caller
        feat, ctx, state_idx, irrig_idx = to_tensors(s)

        feat = feat.to(self.device)
        ctx = ctx.to(self.device)
        state_idx = state_idx.to(self.device)
        irrig_idx = irrig_idx.to(self.device)

        out = self.model(feat, ctx, state_idx, irrig_idx)

        risk_class = int(out["risk_class"].item())
        return {
            "distress_score": round(float(out["distress_score"].item()), 4),
            "intervention_days": round(float(out["intervention_days"].item()), 1),
            "risk_class": risk_class,
            "risk_label": RISK_LABELS[risk_class],
        }

    @torch.no_grad()
    def predict_batch(self, observations: list[dict]) -> list[dict]:
        """Run prediction on a list of observation dicts."""
        return [self.predict(obs) for obs in observations]

    def info(self) -> dict:
        """Return model metadata from the checkpoint."""
        return {
            "parameters": self.model.count_parameters(),
            "device": str(self.device),
            **self.metadata,
        }

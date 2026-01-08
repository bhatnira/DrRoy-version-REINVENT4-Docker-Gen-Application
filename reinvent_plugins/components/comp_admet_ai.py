import json
from typing import List, Optional

from pydantic import BaseModel, Field

try:
    from admet_ai import ADMETModel
except ImportError:  # pragma: no cover
    ADMETModel = None

from reinvent_plugins.normalize import normalize_smiles
from reinvent.scoring.component_results import ComponentResults
from reinvent.scoring.utils import add_tag


SUPPORTED_ENDPOINTS = {
    # Key: human-friendly name used in configs; Value: ADMET-AI column key
    "solubility": "Solubility",
    "hepatic_clearance": "Hepatic Clearance",
    "bioavailability": "Bioavailability",
    "clinical_toxicity": "Clinical Toxicity",
}


class ADMETAIParams(BaseModel):
    # Endpoint to score; one of SUPPORTED_ENDPOINTS keys
    endpoint: str = Field(..., description=f"Endpoint to predict: {list(SUPPORTED_ENDPOINTS.keys())}")
    # Optional model init kwargs if needed; kept flexible
    model_kwargs: Optional[dict] = Field(default=None, description="Optional kwargs for ADMETModel() initialization")
    # Optional batch size for prediction
    batch_size: int = Field(default=256, ge=1, description="Batch size for ADMET-AI prediction")


class ADMETAIComponent:
    """
    Native component that uses admet-ai to predict a single selected endpoint per call.
    Returns raw numeric values; use transforms in TOML to convert to [0,1] rewards.
    """

    def __init__(self, params: ADMETAIParams, **kwargs):
        self.params = params
        self.endpoint_key = SUPPORTED_ENDPOINTS.get(self.params.endpoint.lower())
        if self.endpoint_key is None:
            raise ValueError(f"Unsupported endpoint '{self.params.endpoint}'. Supported: {list(SUPPORTED_ENDPOINTS.keys())}")

        if ADMETModel is None:
            raise ImportError(
                "admet-ai is not installed. Please add 'admet-ai' to requirements and install it before running."
            )
        # Initialize ADMET-AI model
        self.model = ADMETModel(**(self.params.model_kwargs or {}))

    def __call__(self, smiles: List[str]) -> ComponentResults:
        # Normalize SMILES; invalid become None
        canon = [normalize_smiles(s) for s in smiles]
        valid_idx = [i for i, s in enumerate(canon) if s is not None]
        valid_smiles = [canon[i] for i in valid_idx]

        raw_values = [float("nan")] * len(smiles)

        if valid_smiles:
            # Predict with ADMET-AI; returns DataFrame with columns including endpoint_key
            df = self.model.predict(valid_smiles, batch_size=self.params.batch_size)
            if self.endpoint_key not in df.columns:
                raise RuntimeError(
                    f"Endpoint column '{self.endpoint_key}' not found in ADMET-AI output. Available: {list(df.columns)}"
                )
            preds = df[self.endpoint_key].tolist()
            for j, i in enumerate(valid_idx):
                try:
                    raw_values[i] = float(preds[j])
                except Exception:
                    raw_values[i] = float("nan")

        results = ComponentResults(
            total_scores=raw_values,
            # Keep per_smiles to aid debugging/analysis
            per_smiles={"endpoint": self.params.endpoint, "values": raw_values},
        )
        add_tag(results, f"admet_ai_{self.params.endpoint}")
        return results


# Helper to expose params schema for validation/serialization in configs
SCHEMA = json.dumps(ADMETAIParams.model_json_schema())

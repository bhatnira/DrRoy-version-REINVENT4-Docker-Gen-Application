"""GPR-based activity prediction scoring component

Loads a trained GPR model, feature scaler, and feature column list, then
predicts activity from SMILES via Morgan fingerprints and returns a score array.

TOML usage example:

[[stage.scoring.component]]
[stage.scoring.component.GPRActivity]
[[stage.scoring.component.GPRActivity.endpoint]]
name = "Activity (GPR)"
weight = 0.35
params.model_file = "final_gpr.pkl"
params.scaler_file = "scaler.pkl"
params.feature_cols_file = "x_cols.csv"
params.radius = 2
params.nBits = 1024
params.log10_target = true
transform.type = "sigmoid"
transform.low = 5.0
transform.high = 8.0
transform.k = 0.4
"""

from __future__ import annotations

from typing import List
import json
import logging
import pickle
import numpy as np
import pandas as pd
from pydantic.dataclasses import dataclass
from rdkit import Chem
from rdkit.Chem import AllChem

from reinvent_plugins.component_results import ComponentResults
from reinvent_plugins.add_tag import add_tag
from reinvent_plugins.normalize import normalize_smiles

logger = logging.getLogger("reinvent")


def _morgan_fp(smiles: str, radius: int, nBits: int) -> np.ndarray:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.full(nBits, np.nan)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=nBits)
    arr = np.zeros((nBits,), dtype=int)
    # Convert to numpy
    AllChem.DataStructs.ConvertToNumpyArray(fp, arr)  # type: ignore[attr-defined]
    return arr


def _load_feature_cols(path: str) -> List[str]:
    # Supports CSV (one column per feature) or JSON list
    try:
        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as jf:
                cols = json.load(jf)
                if isinstance(cols, dict) and "columns" in cols:
                    return list(cols["columns"])
                return list(cols)
        # assume CSV with a single row or header
        df = pd.read_csv(path)
        if df.shape[1] == 1:
            return df.iloc[:, 0].astype(str).tolist()
        # if the CSV is the original training feature frame, take its columns
        return df.columns.astype(str).tolist()
    except Exception as e:
        logger.warning(f"Failed to read feature columns from {path}: {e}")
        raise


@add_tag("__parameters")
@dataclass
class Parameters:
    model_file: List[str]
    scaler_file: List[str]
    feature_cols_file: List[str]
    radius: List[int]
    nBits: List[int]
    log10_target: List[bool]


@add_tag("__component")
class GPRActivity:
    """GPR activity predictor component"""

    def __init__(self, params: Parameters):
        # Only single endpoint supported per instance; lists follow plugin API
        self.model_file = params.model_file[0]
        self.scaler_file = params.scaler_file[0]
        self.feature_cols_file = params.feature_cols_file[0]
        self.radius = int(params.radius[0])
        self.nBits = int(params.nBits[0])
        self.log10_target = bool(params.log10_target[0])

        # needed in the normalize_smiles decorator
        self.smiles_type = "rdkit_smiles"

        # Load artifacts
        with open(self.model_file, "rb") as mf:
            self.model = pickle.load(mf)
        with open(self.scaler_file, "rb") as sf:
            self.scaler = pickle.load(sf)
        self.feature_cols = _load_feature_cols(self.feature_cols_file)

        logger.info(
            f"Loaded GPRActivity model={self.model_file}, scaler={self.scaler_file}, "
            f"features={len(self.feature_cols)}"
        )

        self.number_of_endpoints = 1

    @normalize_smiles
    def __call__(self, smilies: List[str]) -> np.ndarray:
        # Compute fingerprints
        fps = [
            _morgan_fp(smi, radius=self.radius, nBits=self.nBits) for smi in smilies
        ]
        X = pd.DataFrame(fps, columns=[f"FP_{i}" for i in range(self.nBits)])

        # Reorder/select columns to match training feature set
        try:
            X = X[self.feature_cols]
        except KeyError:
            # Some bits may be missing; add zeros for missing, drop extras
            for c in self.feature_cols:
                if c not in X.columns:
                    X[c] = 0
            X = X[self.feature_cols]

        # Scale
        X_scaled = self.scaler.transform(X.values)
        # Predict
        preds = self.model.predict(X_scaled)

        # If target was log10 during training, convert back to original scale (optional)
        if self.log10_target:
            try:
                preds = np.power(10.0, preds)
            except Exception:
                logger.warning("Failed to inverse log10; returning log-scale predictions")

        # Return as ComponentResults (single endpoint)
        return ComponentResults([np.array(preds, dtype=float)])

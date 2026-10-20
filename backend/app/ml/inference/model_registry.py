import os
import json
import joblib
from typing import Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.core.logging import logger

class ModelRegistry:
    def __init__(self, artifact_dir: str = settings.MODEL_ARTIFACT_DIR):
        self.artifact_dir = artifact_dir
        self._models: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def get_artifact_path(self, model_key: str) -> str:
        return os.path.join(self.artifact_dir, f"{model_key}.pkl")

    def get_metadata_path(self, model_key: str) -> str:
        # e.g., credit_card_metadata.json
        prefix = model_key.replace("_model", "")
        return os.path.join(self.artifact_dir, f"{prefix}_metadata.json")

    def load_model(self, model_key: str):
        if model_key in self._models:
            return self._models[model_key]

        path = self.get_artifact_path(model_key)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model artifact for '{model_key}' does not exist at {path}. Retrain or bootstrap models first.")

        try:
            model = joblib.load(path)
            self._models[model_key] = model
            logger.info(f"Loaded ML model '{model_key}' from {path}")
            return model
        except Exception as e:
            logger.error(f"Failed loading model artifact {path}: {e}")
            raise

    def get_metadata(self, model_key: str) -> Optional[Dict[str, Any]]:
        if model_key in self._metadata:
            return self._metadata[model_key]

        path = self.get_metadata_path(model_key)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    self._metadata[model_key] = data
                    return data
            except Exception as e:
                logger.error(f"Failed to read metadata at {path}: {e}")
        return None

    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        keys = ["credit_card_model", "url_fraud_model", "trust_score_model"]
        status = {}
        for k in keys:
            path = self.get_artifact_path(k)
            meta = self.get_metadata(k)
            exists = os.path.exists(path)
            status[k] = {
                "model_key": k,
                "is_trained": exists,
                "artifact_path": path,
                "metadata": meta
            }
        return status

model_registry = ModelRegistry()

from typing import List
from fastapi import APIRouter
from backend.app.ml.inference.model_registry import model_registry
from backend.app.schemas.all_schemas import ModelMetadataResponse

router = APIRouter()

@router.get("/status", response_model=List[ModelMetadataResponse])
async def get_models_status():
    """Retrieve training and artifact availability status for all ML models."""
    status_dict = model_registry.get_all_status()
    responses = []
    for k, v in status_dict.items():
        meta = v.get("metadata") or {}
        responses.append(ModelMetadataResponse(
            model_name=meta.get("model_name", k),
            is_trained=v["is_trained"],
            version=meta.get("version"),
            trained_at=meta.get("trained_at"),
            algorithm=meta.get("algorithm"),
            sample_count=meta.get("sample_count"),
            metrics=meta.get("metrics"),
            provenance=meta.get("provenance")
        ))
    return responses

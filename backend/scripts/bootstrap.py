import os
import sys
from backend.app.core.logging import logger
from backend.app.core.config import settings
from backend.app.db.session import engine, Base
from backend.scripts.generate_synthetic_data import (
    generate_credit_card_data, generate_url_fraud_data, generate_trust_score_data
)
from backend.app.ml.training.train_credit_card import train_credit_card_model
from backend.app.ml.training.train_url_fraud import train_url_fraud_model
from backend.app.ml.training.train_trust_model import train_trust_score_model
from backend.app.ml.inference.model_registry import model_registry

def bootstrap_system():
    logger.info("=== Starting FinoAddWise-X Bootstrap Workflow ===")

    # 1. Prepare directories
    logger.info("1. Creating required storage and artifact directories...")
    os.makedirs(settings.MODEL_ARTIFACT_DIR, exist_ok=True)
    os.makedirs(settings.DOCUMENT_STORAGE_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    os.makedirs("data/synthetic", exist_ok=True)

    # 2. Initialize Database tables
    logger.info("2. Initializing SQLite / Postgres database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema initialized successfully.")

    # 3. Generate synthetic data if configured
    logger.info("3. Checking synthetic datasets...")
    generate_credit_card_data()
    generate_url_fraud_data()
    generate_trust_score_data()

    # 4. Train ML Models and persist .pkl artifacts
    logger.info("4. Training ML models and serializing artifacts...")
    train_credit_card_model(artifact_dir=settings.MODEL_ARTIFACT_DIR)
    train_url_fraud_model(artifact_dir=settings.MODEL_ARTIFACT_DIR)
    train_trust_score_model(artifact_dir=settings.MODEL_ARTIFACT_DIR)

    # 5. Verify Artifact Loading
    logger.info("5. Verifying ML model artifact loading in registry...")
    status = model_registry.get_all_status()
    all_ready = True
    for key, info in status.items():
        if not info["is_trained"]:
            logger.error(f"Model '{key}' failed to train or serialize artifact!")
            all_ready = False
        else:
            logger.info(f"Verified artifact: {key} (Algorithm: {info['metadata'].get('algorithm')})")

    if not all_ready:
        logger.error("Bootstrap failed: Not all models were verified.")
        sys.exit(1)

    logger.info("=== FinoAddWise-X Bootstrap Completed Successfully! ===")

if __name__ == "__main__":
    bootstrap_system()

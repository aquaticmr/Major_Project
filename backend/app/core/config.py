import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    PROJECT_NAME: str = "FinoAddWise-X"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./finoaddwise.db"
    
    # Clerk Authentication
    CLERK_ISSUER_URL: str = "https://clerk.your-domain.com"
    CLERK_JWKS_URL: str = "https://clerk.your-domain.com/.well-known/jwks.json"
    CLERK_SECRET_KEY: str = ""
    CLERK_AUDIENCE: str = ""
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["http://localhost:5173", "http://localhost:3000"]
        
    # Storage paths
    MODEL_ARTIFACT_DIR: str = os.path.join("backend", "app", "ml", "artifacts")
    DOCUMENT_STORAGE_DIR: str = os.path.join("storage", "documents")
    CHROMA_PERSIST_DIR: str = os.path.join("storage", "chroma")
    
    # LLM & RAG
    LLM_PROVIDER: str = "local"
    LLM_API_KEY: str = ""
    LLM_MODEL_NAME: str = "local-deterministic"
    EMBEDDING_PROVIDER: str = "fastembed"
    RAG_HYBRID_ALPHA: float = 0.5
    
    # Evidence quality formula weights (alpha + beta + gamma = 1.0)
    EVIDENCE_ALPHA: float = 0.40
    EVIDENCE_BETA: float = 0.35
    EVIDENCE_GAMMA: float = 0.25
    
    # Thresholds
    URL_FRAUD_THRESHOLD: float = 0.70
    ENABLE_SYNTHETIC_TRAINING_DATA: bool = True
    
    # Cryptography
    ENCRYPTION_SECRET_KEY: str = "k8Q_Z2-0q1XjF5F6Vv3k8eG2x9zQ4L1m0vW5N8yP3sU="

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

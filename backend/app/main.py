from fastapi import FastAPI
from fastapi.middleware.cors import CORSMouter, CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.session import engine, Base
from backend.app.api.v1 import (
    auth, documents, rag, advisory, credit_cards, fraud, trust, evaluation, alerts, models_status
)

# Auto-create tables on startup (or via Alembic migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FinoAddWise-X GenAI-Powered Financial Co-Pilot API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public Health Check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.APP_ENV
    }

# API v1 Routers
api_v1 = settings.API_V1_STR
app.include_router(auth.router, prefix=f"{api_v1}/auth", tags=["Authentication"])
app.include_router(documents.router, prefix=f"{api_v1}/documents", tags=["Document Intelligence"])
app.include_router(rag.router, prefix=f"{api_v1}/rag", tags=["Low-Hallucination RAG"])
app.include_router(advisory.router, prefix=f"{api_v1}/advisory", tags=["Financial Advisory & Calculations"])
app.include_router(credit_cards.router, prefix=f"{api_v1}/credit-cards", tags=["Credit Card Recommendations"])
app.include_router(fraud.router, prefix=f"{api_v1}/fraud", tags=["URL Fraud Threat Intelligence"])
app.include_router(trust.router, prefix=f"{api_v1}/trust", tags=["Alternative Data Trust Scoring"])
app.include_router(evaluation.router, prefix=f"{api_v1}/evaluation", tags=["RAGAS Evaluation"])
app.include_router(alerts.router, prefix=f"{api_v1}/alerts", tags=["Alerts & Notifications"])
app.include_router(models_status.router, prefix=f"{api_v1}/models", tags=["Model Registry"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

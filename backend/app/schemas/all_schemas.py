from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

# User schemas
class UserBase(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    role: str = "user"

class UserResponse(UserBase):
    id: str
    clerk_user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Document schemas
class DocumentChunkResponse(BaseModel):
    id: str
    page_number: int
    clause_id: Optional[str]
    chunk_index: int
    content: str
    
    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    page_count: int
    status: str
    extraction_method: str
    chunk_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# RAG & Verification schemas
class Citation(BaseModel):
    document_id: str
    document_name: str
    page_number: int
    clause_id: Optional[str] = None
    excerpt: str

class RAGQueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    document_ids: Optional[List[str]] = None

class RAGQueryResponse(BaseModel):
    session_id: str
    answer: str
    citations: List[Citation]
    evidence_score: float
    verification_status: str # "VERIFIED", "PARTIALLY_SUPPORTED", "INSUFFICIENT_EVIDENCE"
    numerical_check_passed: bool
    requires_human_review: bool
    evidence_breakdown: Dict[str, float]

class RAGSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Financial Advisory & Calculation schemas
class FinancialProfileCreate(BaseModel):
    monthly_income: Decimal
    monthly_expenses: Decimal
    dining_spend: Decimal = Decimal(0)
    travel_spend: Decimal = Decimal(0)
    grocery_spend: Decimal = Decimal(0)
    fuel_spend: Decimal = Decimal(0)
    other_spend: Decimal = Decimal(0)
    annual_fee_willingness: Decimal = Decimal(0)
    preferred_reward_type: str = "cashback"
    debt_amount: Decimal = Decimal(0)

class AdvisoryAnalysisRequest(BaseModel):
    profile: FinancialProfileCreate
    loan_principal: Optional[Decimal] = None
    annual_interest_rate_pct: Optional[Decimal] = None
    loan_term_months: Optional[int] = None

class AdvisoryAnalysisResponse(BaseModel):
    monthly_surplus: Decimal
    savings_rate_pct: Decimal
    debt_to_income_ratio: Decimal
    emi: Optional[Decimal] = None
    budget_breakdown: Dict[str, Decimal]
    recommendations: List[str]
    disclaimer: str

# Credit Card recommendation schemas
class CardRecommendationRequest(BaseModel):
    profile: FinancialProfileCreate

class RankedCard(BaseModel):
    card_id: str
    card_name: str
    issuer: str
    annual_fee: Decimal
    estimated_annual_rewards: Decimal
    estimated_net_rewards: Decimal
    model_score: float
    eligibility_status: str
    key_perks: List[str]

class CardRecommendationResponse(BaseModel):
    ranked_cards: List[RankedCard]
    model_version: str
    disclaimer: str

# URL Fraud schemas
class URLFraudRequest(BaseModel):
    url: str

class URLFraudResponse(BaseModel):
    url: str
    risk_score: float
    is_malicious: bool
    risk_level: str # LOW, MEDIUM, HIGH
    explanation_factors: List[str]
    model_version: str
    disclaimer: str

class FraudAssessmentResponse(BaseModel):
    id: str
    url: str
    risk_score: float
    is_malicious: bool
    explanation_factors: List[str]
    model_version: str
    created_at: datetime

    class Config:
        from_attributes = True

# Trust score schemas
class TrustScoreRequest(BaseModel):
    payment_regularity_pct: float = Field(..., ge=0, le=100) # 0 to 100% on-time payments
    income_stability_months: int = Field(..., ge=0)
    monthly_dti_pct: float = Field(..., ge=0)
    savings_consistency_score: float = Field(..., ge=0, le=1) # 0 to 1
    account_age_years: float = Field(..., ge=0)

class TrustScoreResponse(BaseModel):
    trust_score: float
    risk_category: str # "PRIME", "NEAR_PRIME", "SUBPRIME"
    calibrated: bool
    contributing_factors: List[str]
    model_version: str
    disclaimer: str

# Alerts & Notifications schemas
class AlertResponse(BaseModel):
    id: str
    title: str
    message: str
    alert_type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# RAGAS Evaluation schemas
class EvaluationRunRequest(BaseModel):
    dataset_name: str = "financial_rag_benchmark"

class EvaluationRunResponse(BaseModel):
    id: str
    dataset_name: str
    faithfulness: Optional[float]
    answer_relevancy: Optional[float]
    context_precision: Optional[float]
    context_recall: Optional[float]
    sample_count: int
    status: str
    details: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

# Model status schemas
class ModelMetadataResponse(BaseModel):
    model_name: str
    is_trained: bool
    version: Optional[str] = None
    trained_at: Optional[str] = None
    algorithm: Optional[str] = None
    sample_count: Optional[int] = None
    metrics: Optional[Dict[str, Any]] = None
    provenance: Optional[str] = None

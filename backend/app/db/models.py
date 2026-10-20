import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON, Numeric
)
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clerk_user_id = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=True)
    display_name = Column(String(255), nullable=True)
    role = Column(String(50), default="user", nullable=False) # "user", "admin"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    rag_sessions = relationship("RAGSession", back_populates="user", cascade="all, delete-orphan")
    financial_profiles = relationship("FinancialProfile", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("CardRecommendationResult", back_populates="user", cascade="all, delete-orphan")
    fraud_assessments = relationship("FraudAssessment", back_populates="user", cascade="all, delete-orphan")
    trust_scores = relationship("TrustScoreAssessment", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("AlertNotification", back_populates="user", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    page_count = Column(Integer, default=1)
    status = Column(String(50), default="pending", nullable=False) # pending, processing, indexed, failed
    extraction_method = Column(String(100), default="standard_pdf")
    is_encrypted = Column(Boolean, default=True)
    chunk_count = Column(Integer, default=0)
    meta_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    page_number = Column(Integer, default=1)
    clause_id = Column(String(100), nullable=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    extraction_method = Column(String(100), default="standard")
    meta_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="chunks")


class RAGSession(Base):
    __tablename__ = "rag_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), default="Financial Consultation")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="rag_sessions")
    messages = relationship("RAGMessage", back_populates="session", cascade="all, delete-orphan")


class RAGMessage(Base):
    __tablename__ = "rag_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("rag_sessions.id"), nullable=False, index=True)
    sender = Column(String(20), nullable=False) # "user", "assistant"
    content = Column(Text, nullable=False)
    evidence_score = Column(Float, nullable=True)
    verification_status = Column(String(50), nullable=True)
    citations = Column(JSON, default=list) # [{doc_id, page, clause, excerpt}]
    meta_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("RAGSession", back_populates="messages")


class FinancialProfile(Base):
    __tablename__ = "financial_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    monthly_income = Column(Numeric(12, 2), nullable=False)
    monthly_expenses = Column(Numeric(12, 2), nullable=False)
    dining_spend = Column(Numeric(12, 2), default=0)
    travel_spend = Column(Numeric(12, 2), default=0)
    grocery_spend = Column(Numeric(12, 2), default=0)
    fuel_spend = Column(Numeric(12, 2), default=0)
    other_spend = Column(Numeric(12, 2), default=0)
    annual_fee_willingness = Column(Numeric(12, 2), default=0)
    preferred_reward_type = Column(String(50), default="cashback") # cashback, travel, points, lounge
    debt_amount = Column(Numeric(12, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="financial_profiles")


class CardCatalog(Base):
    __tablename__ = "card_catalog"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    card_name = Column(String(255), nullable=False)
    issuer = Column(String(100), nullable=False)
    annual_fee = Column(Numeric(10, 2), nullable=False)
    min_income_requirement = Column(Numeric(12, 2), default=0)
    cashback_rate = Column(Float, default=0.01)
    dining_multiplier = Column(Float, default=1.0)
    travel_multiplier = Column(Float, default=1.0)
    grocery_multiplier = Column(Float, default=1.0)
    fuel_multiplier = Column(Float, default=1.0)
    welcome_bonus_value = Column(Numeric(10, 2), default=0)
    features = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CardRecommendationResult(Base):
    __tablename__ = "card_recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    ranked_cards = Column(JSON, nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="recommendations")


class FraudAssessment(Base):
    __tablename__ = "fraud_assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    url = Column(String(1000), nullable=False)
    risk_score = Column(Float, nullable=False)
    is_malicious = Column(Boolean, nullable=False)
    explanation_factors = Column(JSON, default=list)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="fraud_assessments")


class TrustScoreAssessment(Base):
    __tablename__ = "trust_score_assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    trust_score = Column(Float, nullable=False)
    risk_category = Column(String(50), nullable=False)
    factors = Column(JSON, default=list)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="trust_scores")


class RAGASEvaluationRun(Base):
    __tablename__ = "ragas_evaluation_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_name = Column(String(100), nullable=False)
    faithfulness = Column(Float, nullable=True)
    answer_relevancy = Column(Float, nullable=True)
    context_precision = Column(Float, nullable=True)
    context_recall = Column(Float, nullable=True)
    sample_count = Column(Integer, default=0)
    details = Column(JSON, default=dict)
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AlertNotification(Base):
    __tablename__ = "alert_notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), default="info") # info, warning, danger, success
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="alerts")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100), nullable=True)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="audit_events")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from backend.app.core.config import settings
from backend.app.db.session import Base, get_db
from backend.app.schemas.all_schemas import FinancialProfileCreate, AdvisoryAnalysisRequest
from backend.app.services.advisory_service import advisory_service
from decimal import Decimal

# Test database
TEST_DB_URL = "sqlite:///./test_finoaddwise.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == settings.PROJECT_NAME

def test_unauthenticated_protected_endpoint():
    # Attempt to access protected endpoint without Bearer token
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert "Missing Bearer authentication token" in response.text

def test_authenticated_user_isolation():
    # Use mock test tokens
    headers_alice = {"Authorization": "Bearer test_token_alice_123"}
    headers_bob = {"Authorization": "Bearer test_token_bob_456"}

    # Alice's profile
    res_a = client.get("/api/v1/auth/me", headers=headers_alice)
    assert res_a.status_code == 200
    user_a = res_a.json()
    assert user_a["clerk_user_id"] == "alice_123"

    # Bob's profile
    res_b = client.get("/api/v1/auth/me", headers=headers_bob)
    assert res_b.status_code == 200
    user_b = res_b.json()
    assert user_b["clerk_user_id"] == "bob_456"
    assert user_a["id"] != user_b["id"]

def test_financial_calculations():
    # Test EMI calculation
    principal = Decimal("100000.00")
    rate = Decimal("8.5")
    months = 120
    emi = advisory_service.calculate_emi(principal, rate, months)
    assert emi > Decimal("1200.00")
    assert emi < Decimal("1300.00")

    # Advisory surplus & savings rate
    prof = FinancialProfileCreate(
        monthly_income=Decimal("8000.00"),
        monthly_expenses=Decimal("5000.00"),
        dining_spend=Decimal("600.00"),
        travel_spend=Decimal("400.00"),
        grocery_spend=Decimal("800.00"),
        fuel_spend=Decimal("200.00"),
        other_spend=Decimal("500.00"),
        annual_fee_willingness=Decimal("250.00"),
        preferred_reward_type="cashback",
        debt_amount=Decimal("1500.00")
    )
    req = AdvisoryAnalysisRequest(profile=prof)
    res = advisory_service.analyze_finances(req)
    assert res.monthly_surplus == Decimal("3000.00")
    assert res.savings_rate_pct == Decimal("37.5")
    assert len(res.recommendations) > 0

def test_url_fraud_inference():
    headers = {"Authorization": "Bearer test_token_alice_123"}
    # Safe URL
    res_safe = client.post("/api/v1/fraud/analyze-url", json={"url": "https://www.chase.com/personal/banking"}, headers=headers)
    assert res_safe.status_code == 200
    data_safe = res_safe.json()
    assert "risk_score" in data_safe
    assert data_safe["risk_level"] in ["LOW", "MEDIUM"]

    # Phishing IP URL
    res_phish = client.post("/api/v1/fraud/analyze-url", json={"url": "http://192.168.1.100/chase-bank-verify-account/login.php"}, headers=headers)
    assert res_phish.status_code == 200
    data_phish = res_phish.json()
    assert data_phish["risk_score"] > data_safe["risk_score"]
    assert any("direct IP" in f for f in data_phish["explanation_factors"])

def test_trust_score_inference():
    headers = {"Authorization": "Bearer test_token_alice_123"}
    payload = {
        "payment_regularity_pct": 98.5,
        "income_stability_months": 48,
        "monthly_dti_pct": 22.0,
        "savings_consistency_score": 0.85,
        "account_age_years": 8.0
    }
    res = client.post("/api/v1/trust/score", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["trust_score"] >= 650
    assert data["risk_category"] in ["PRIME", "NEAR_PRIME"]
    assert len(data["contributing_factors"]) > 0

def test_model_registry_status():
    res = client.get("/api/v1/models/status")
    assert res.status_code == 200
    models = res.json()
    assert len(models) == 3
    for m in models:
        assert m["is_trained"] is True
        assert m["algorithm"] is not None

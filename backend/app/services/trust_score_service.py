import pandas as pd
from typing import List
from backend.app.ml.inference.model_registry import model_registry
from backend.app.schemas.all_schemas import TrustScoreRequest, TrustScoreResponse

class TrustScoreService:
    def calculate_score(self, req: TrustScoreRequest) -> TrustScoreResponse:
        model = model_registry.load_model("trust_score_model")
        metadata = model_registry.get_metadata("trust_score_model") or {}
        version = metadata.get("version", "1.0.0")

        input_df = pd.DataFrame([{
            "payment_regularity_pct": req.payment_regularity_pct,
            "income_stability_months": req.income_stability_months,
            "monthly_dti_pct": req.monthly_dti_pct,
            "savings_consistency_score": req.savings_consistency_score,
            "account_age_years": req.account_age_years
        }])

        # Predict calibrated probability of trustworthiness
        calibrated_prob = float(model.predict_proba(input_df)[0][1])

        # Map probability to representative score range (e.g. 300 - 850)
        scaled_score = round(300 + (calibrated_prob * 550), 1)

        factors: List[str] = []
        if req.payment_regularity_pct >= 95:
            factors.append("Exceptional on-time payment regularity (>=95%).")
        elif req.payment_regularity_pct < 80:
            factors.append("Payment regularity under 80% negatively impacts trust score.")

        if req.income_stability_months >= 24:
            factors.append("Demonstrated multi-year income continuity (>24 months).")

        if req.monthly_dti_pct > 40:
            factors.append("Elevated debt-to-income ratio reduces disposable debt buffer.")

        if req.savings_consistency_score >= 0.7:
            factors.append("High monthly savings consistency positively reinforces score.")

        category = "PRIME" if scaled_score >= 720 else ("NEAR_PRIME" if scaled_score >= 620 else "SUBPRIME")

        return TrustScoreResponse(
            trust_score=scaled_score,
            risk_category=category,
            calibrated=True,
            contributing_factors=factors,
            model_version=version,
            disclaimer="Alternative trust score is an exploratory behavioral estimate and does not represent an official FICO or credit-bureau score."
        )

trust_score_service = TrustScoreService()

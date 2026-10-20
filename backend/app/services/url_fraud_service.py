from typing import List
from backend.app.ml.inference.model_registry import model_registry
from backend.app.ml.inference.url_feature_extractor import extract_features_df, extract_url_features
from backend.app.schemas.all_schemas import URLFraudResponse
from backend.app.core.config import settings

class URLFraudService:
    def analyze_url(self, url: str) -> URLFraudResponse:
        model = model_registry.load_model("url_fraud_model")
        metadata = model_registry.get_metadata("url_fraud_model") or {}
        version = metadata.get("version", "1.0.0")

        features_df = extract_features_df([url])
        risk_prob = float(model.predict_proba(features_df)[0][1])

        raw_features = extract_url_features(url)
        explanations: List[str] = []

        if raw_features["is_ip"]:
            explanations.append("Hostname utilizes direct IP address rather than a recognized domain.")
        if not raw_features["is_https"]:
            explanations.append("URL does not use encrypted HTTPS transport protocol.")
        if raw_features["num_subdomains"] >= 3:
            explanations.append(f"Excessive subdomain depth ({raw_features['num_subdomains']} subdomains) detected.")
        if raw_features["url_entropy"] > 4.2:
            explanations.append(f"High character entropy ({raw_features['url_entropy']:.2f}) indicates potential randomized/obfuscated path.")
        if raw_features["has_suspicious_kw"]:
            explanations.append("Contains targeted authentication or financial urgency keywords in domain/path.")
        if not explanations:
            explanations.append("Domain and path heuristics conform to typical legitimate URL patterns.")

        is_malicious = risk_prob >= settings.URL_FRAUD_THRESHOLD
        risk_level = "HIGH" if risk_prob >= 0.70 else ("MEDIUM" if risk_prob >= 0.40 else "LOW")

        return URLFraudResponse(
            url=url,
            risk_score=round(risk_prob, 4),
            is_malicious=is_malicious,
            risk_level=risk_level,
            explanation_factors=explanations,
            model_version=version,
            disclaimer="URL risk score is an ML heuristic threat indicator. Model outputs may exhibit false positives or false negatives."
        )

url_fraud_service = URLFraudService()

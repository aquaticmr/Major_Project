import os
import json
import joblib
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score

def train_trust_score_model(data_path: str = "data/synthetic/trust_score_data.csv", artifact_dir: str = "backend/app/ml/artifacts"):
    os.makedirs(artifact_dir, exist_ok=True)
    if not os.path.exists(data_path):
        from backend.scripts.generate_synthetic_data import generate_trust_score_data
        generate_trust_score_data(output_path=data_path)

    df = pd.read_csv(data_path)
    X = df.drop(columns=["is_trustworthy"])
    y = df["is_trustworthy"]

    pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(random_state=42, C=1.0))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    accuracy = float(accuracy_score(y_test, y_pred))
    roc_auc = float(roc_auc_score(y_test, y_prob))
    report = classification_report(y_test, y_pred, output_dict=True)

    model_path = os.path.join(artifact_dir, "trust_score_model.pkl")
    meta_path = os.path.join(artifact_dir, "trust_score_metadata.json")

    joblib.dump(pipeline, model_path)

    metadata = {
        "model_name": "Alternative Data Trust Score Model",
        "algorithm": "LogisticRegression (calibrated probabilities)",
        "version": "1.0.0",
        "trained_at": datetime.utcnow().isoformat(),
        "sample_count": len(df),
        "test_accuracy": accuracy,
        "roc_auc": roc_auc,
        "metrics": report,
        "features": list(X.columns),
        "feature_coefficients": {feat: float(coef) for feat, coef in zip(X.columns, pipeline.named_steps["classifier"].coef_[0])},
        "intercept": float(pipeline.named_steps["classifier"].intercept_[0]),
        "provenance": "Synthetic alternative data behavioral credit score dataset excluding protected attributes"
    }
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Trust Score Model trained successfully. Accuracy: {accuracy:.4f}, AUC: {roc_auc:.4f}. Saved to {model_path}")
    return pipeline, metadata

if __name__ == "__main__":
    train_trust_score_model()

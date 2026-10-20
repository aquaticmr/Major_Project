import os
import json
import joblib
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score

def train_credit_card_model(data_path: str = "data/synthetic/credit_card_data.csv", artifact_dir: str = "backend/app/ml/artifacts"):
    os.makedirs(artifact_dir, exist_ok=True)
    if not os.path.exists(data_path):
        from backend.scripts.generate_synthetic_data import generate_credit_card_data
        generate_credit_card_data(output_path=data_path)

    df = pd.read_csv(data_path)
    X = df.drop(columns=["recommended_card_tier"])
    y = df["recommended_card_tier"]

    num_features = ["monthly_income", "dining_spend", "travel_spend", "grocery_spend", "fuel_spend", "annual_fee_willingness", "debt_to_income"]
    cat_features = ["preferred_reward_type"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features)
        ]
    )

    clf = HistGradientBoostingClassifier(random_state=42, max_iter=150)
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", clf)
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = float(accuracy_score(y_test, y_pred))
    report = classification_report(y_test, y_pred, output_dict=True)

    model_path = os.path.join(artifact_dir, "credit_card_model.pkl")
    meta_path = os.path.join(artifact_dir, "credit_card_metadata.json")

    joblib.dump(pipeline, model_path)

    metadata = {
        "model_name": "Credit Card Product Recommender",
        "algorithm": "HistGradientBoostingClassifier",
        "version": "1.0.0",
        "trained_at": datetime.utcnow().isoformat(),
        "sample_count": len(df),
        "test_accuracy": accuracy,
        "metrics": report,
        "features": list(X.columns),
        "target_classes": list(pipeline.classes_),
        "provenance": "Synthetic credit card ranking dataset with documented financial rules"
    }
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Credit Card Model trained successfully. Accuracy: {accuracy:.4f}. Artifact saved to {model_path}")
    return pipeline, metadata

if __name__ == "__main__":
    train_credit_card_model()

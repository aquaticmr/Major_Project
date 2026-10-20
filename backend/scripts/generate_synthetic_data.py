import os
import json
import numpy as np
import pandas as pd

def generate_credit_card_data(n_samples: int = 1500, output_path: str = "data/synthetic/credit_card_data.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.random.seed(42)

    income = np.random.lognormal(mean=10.5, sigma=0.6, size=n_samples) # approx 20k to 150k
    dining = income * np.random.uniform(0.05, 0.20, size=n_samples) / 12
    travel = income * np.random.uniform(0.02, 0.25, size=n_samples) / 12
    grocery = income * np.random.uniform(0.08, 0.22, size=n_samples) / 12
    fuel = income * np.random.uniform(0.02, 0.08, size=n_samples) / 12
    fee_willingness = np.random.choice([0, 95, 250, 495, 695], size=n_samples, p=[0.35, 0.30, 0.20, 0.10, 0.05])
    preferred_reward = np.random.choice(["cashback", "travel", "points", "lounge"], size=n_samples)
    dti = np.random.uniform(0.05, 0.65, size=n_samples)

    # Determine ground-truth suitable card tier
    card_tier = []
    for inc, trav, din, fee, pref in zip(income, travel, dining, fee_willingness, preferred_reward):
        if inc > 100000 and (trav > 500 or fee >= 495):
            card_tier.append("UltraPremium_Travel")
        elif inc > 60000 and (din > 400 or trav > 250):
            card_tier.append("Premium_Rewards")
        elif fee == 0 or inc < 45000:
            card_tier.append("Entry_NoFee_Cashback")
        else:
            card_tier.append("MidTier_Cashback")

    df = pd.DataFrame({
        "monthly_income": np.round(income / 12, 2),
        "dining_spend": np.round(dining, 2),
        "travel_spend": np.round(travel, 2),
        "grocery_spend": np.round(grocery, 2),
        "fuel_spend": np.round(fuel, 2),
        "annual_fee_willingness": fee_willingness,
        "preferred_reward_type": preferred_reward,
        "debt_to_income": np.round(dti, 3),
        "recommended_card_tier": card_tier
    })
    df.to_csv(output_path, index=False)
    print(f"Generated synthetic credit card training data at {output_path} ({n_samples} samples)")
    return df

def generate_url_fraud_data(n_samples: int = 2000, output_path: str = "data/synthetic/url_fraud_data.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.random.seed(42)

    legit_domains = ["google.com", "bankofamerica.com", "chase.com", "fidelity.com", "github.com", "amazon.com", "nytimes.com", "irs.gov"]
    fraud_keywords = ["secure-login", "verify-account", "update-kyc", "free-crypto", "banking-alert", "claim-bonus", "paypal-support"]

    urls = []
    labels = [] # 1 = fraud/malicious, 0 = legitimate

    for _ in range(n_samples // 2):
        # Legitimate URL
        dom = np.random.choice(legit_domains)
        path = np.random.choice(["", "/account", "/portal/dashboard", "/help/article/102", "/investments/funds"])
        urls.append(f"https://www.{dom}{path}")
        labels.append(0)

    for _ in range(n_samples // 2):
        # Suspicious / Malicious URL
        kw = np.random.choice(fraud_keywords)
        suspicious_tld = np.random.choice([".xyz", ".top", ".club", ".ru", ".tk", ".work", ".info"])
        has_ip = np.random.rand() > 0.7
        if has_ip:
            ip = f"{np.random.randint(11,250)}.{np.random.randint(0,255)}.{np.random.randint(0,255)}.{np.random.randint(1,254)}"
            urls.append(f"http://{ip}/{kw}/login.php?session={np.random.randint(100000, 999999)}")
        else:
            urls.append(f"http://chase-bank-{kw}{suspicious_tld}/auth?user_redirect=verify&ref={np.random.randint(1000,9999)}")
        labels.append(1)

    df = pd.DataFrame({"url": urls, "is_malicious": labels})
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(output_path, index=False)
    print(f"Generated synthetic URL fraud data at {output_path} ({n_samples} samples)")
    return df

def generate_trust_score_data(n_samples: int = 1500, output_path: str = "data/synthetic/trust_score_data.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.random.seed(42)

    payment_regularity = np.random.uniform(50, 100, size=n_samples) # % on-time
    income_stability = np.random.randint(3, 120, size=n_samples) # months at current employment/income
    dti = np.random.uniform(5, 75, size=n_samples) # %
    savings_consistency = np.random.uniform(0.1, 1.0, size=n_samples) # 0 to 1
    account_age = np.random.uniform(0.5, 20.0, size=n_samples) # years

    # Latent trust propensity
    latent = (
        0.03 * payment_regularity
        + 0.015 * income_stability
        - 0.025 * dti
        + 2.0 * savings_consistency
        + 0.1 * account_age
        + np.random.normal(0, 0.5, size=n_samples)
    )
    # Binary creditworthy target (1 = High Trust / Prime, 0 = Subprime/High Risk)
    prob = 1 / (1 + np.exp(-(latent - 3.0)))
    target = (prob > 0.5).astype(int)

    df = pd.DataFrame({
        "payment_regularity_pct": np.round(payment_regularity, 1),
        "income_stability_months": income_stability,
        "monthly_dti_pct": np.round(dti, 1),
        "savings_consistency_score": np.round(savings_consistency, 2),
        "account_age_years": np.round(account_age, 1),
        "is_trustworthy": target
    })
    df.to_csv(output_path, index=False)
    print(f"Generated synthetic trust score data at {output_path} ({n_samples} samples)")
    return df

if __name__ == "__main__":
    generate_credit_card_data()
    generate_url_fraud_data()
    generate_trust_score_data()

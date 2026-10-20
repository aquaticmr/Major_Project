import pandas as pd
from decimal import Decimal
from typing import List
from backend.app.ml.inference.model_registry import model_registry
from backend.app.schemas.all_schemas import FinancialProfileCreate, RankedCard, CardRecommendationResponse

# Default representative card catalog
DEFAULT_CARDS = [
    {
        "card_id": "card_chase_sapphire_res",
        "card_name": "Sapphire Reserve Luxury",
        "issuer": "Chase",
        "tier": "UltraPremium_Travel",
        "annual_fee": Decimal("550.00"),
        "min_income": Decimal("80000.00"),
        "travel_mult": 3.0,
        "dining_mult": 3.0,
        "base_rate": 0.01,
        "welcome_bonus": Decimal("750.00"),
        "key_perks": ["Priority Pass Airport Lounge", "$300 Annual Travel Credit", "Global Entry Credit"]
    },
    {
        "card_id": "card_amex_gold",
        "card_name": "American Express Gold",
        "issuer": "Amex",
        "tier": "Premium_Rewards",
        "annual_fee": Decimal("250.00"),
        "min_income": Decimal("50000.00"),
        "travel_mult": 3.0,
        "dining_mult": 4.0,
        "base_rate": 0.01,
        "welcome_bonus": Decimal("600.00"),
        "key_perks": ["4x Dining Worldwide", "4x US Supermarkets", "$120 Uber Cash"]
    },
    {
        "card_id": "card_citi_double",
        "card_name": "Citi Double Cash",
        "issuer": "Citi",
        "tier": "MidTier_Cashback",
        "annual_fee": Decimal("0.00"),
        "min_income": Decimal("30000.00"),
        "travel_mult": 1.0,
        "dining_mult": 1.0,
        "base_rate": 0.02, # Flat 2%
        "welcome_bonus": Decimal("200.00"),
        "key_perks": ["Flat 2% Cash Back on all purchases", "No Annual Fee", "0% Intro APR"]
    },
    {
        "card_id": "card_capital_one_savor",
        "card_name": "Capital One SavorOne",
        "issuer": "Capital One",
        "tier": "Entry_NoFee_Cashback",
        "annual_fee": Decimal("0.00"),
        "min_income": Decimal("25000.00"),
        "travel_mult": 1.0,
        "dining_mult": 3.0,
        "base_rate": 0.01,
        "welcome_bonus": Decimal("200.00"),
        "key_perks": ["3% on Dining & Entertainment", "3% at Grocery Stores", "No Foreign Transaction Fees"]
    }
]

class CreditCardService:
    def recommend(self, profile: FinancialProfileCreate) -> CardRecommendationResponse:
        model = model_registry.load_model("credit_card_model")
        metadata = model_registry.get_metadata("credit_card_model") or {}
        version = metadata.get("version", "1.0.0")

        # Format input for scikit-learn pipeline
        input_df = pd.DataFrame([{
            "monthly_income": float(profile.monthly_income),
            "dining_spend": float(profile.dining_spend),
            "travel_spend": float(profile.travel_spend),
            "grocery_spend": float(profile.grocery_spend),
            "fuel_spend": float(profile.fuel_spend),
            "annual_fee_willingness": float(profile.annual_fee_willingness),
            "preferred_reward_type": profile.preferred_reward_type,
            "debt_to_income": float(profile.debt_amount / profile.monthly_income) if profile.monthly_income > 0 else 0.0
        }])

        pred_tier = model.predict(input_df)[0]
        pred_probs = model.predict_proba(input_df)[0]
        classes = list(model.classes_)
        prob_dict = {cls: float(prob) for cls, prob in zip(classes, pred_probs)}

        annual_income = profile.monthly_income * Decimal(12)
        annual_dining = profile.dining_spend * Decimal(12)
        annual_travel = profile.travel_spend * Decimal(12)
        annual_grocery = profile.grocery_spend * Decimal(12)
        annual_other = profile.other_spend * Decimal(12)

        ranked: List[RankedCard] = []
        for card in DEFAULT_CARDS:
            tier_match_score = prob_dict.get(card["tier"], 0.1)

            # Explicit rewards calculation
            dining_reward = annual_dining * Decimal(str(card["dining_mult"])) * Decimal("0.01")
            travel_reward = annual_travel * Decimal(str(card["travel_mult"])) * Decimal("0.01")
            grocery_reward = annual_grocery * Decimal(str(card["base_rate"]))
            other_reward = annual_other * Decimal(str(card["base_rate"]))

            total_annual_rewards = (dining_reward + travel_reward + grocery_reward + other_reward).quantize(Decimal("0.01"))
            net_rewards = (total_annual_rewards - card["annual_fee"]).quantize(Decimal("0.01"))

            # Eligibility assessment
            is_eligible = annual_income >= card["min_income"] and profile.annual_fee_willingness >= (card["annual_fee"] * Decimal("0.5"))
            eligibility_str = "Eligible" if is_eligible else "Limited (Income or fee alignment review needed)"

            # Final ranking score combining ML preference and net rewards
            composite_score = float(tier_match_score * 0.6) + float(max(Decimal(0), net_rewards) / Decimal(1000) * Decimal("0.4"))

            ranked.append(RankedCard(
                card_id=card["card_id"],
                card_name=card["card_name"],
                issuer=card["issuer"],
                annual_fee=card["annual_fee"],
                estimated_annual_rewards=total_annual_rewards,
                estimated_net_rewards=net_rewards,
                model_score=round(composite_score, 3),
                eligibility_status=eligibility_str,
                key_perks=card["key_perks"]
            ))

        ranked.sort(key=lambda x: x.model_score, reverse=True)

        return CardRecommendationResponse(
            ranked_cards=ranked,
            model_version=version,
            disclaimer="Rankings are based on ML profile alignment and reward simulation. Not an approval commitment or official underwriting decision."
        )

credit_card_service = CreditCardService()

import os
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List
from backend.app.schemas.all_schemas import AdvisoryAnalysisRequest, AdvisoryAnalysisResponse

class AdvisoryService:
    def calculate_emi(self, principal: Decimal, annual_rate_pct: Decimal, term_months: int) -> Decimal:
        """
        EMI = [P x r x (1+r)^n] / [(1+r)^n - 1]
        """
        if principal <= 0 or term_months <= 0:
            return Decimal(0)
        if annual_rate_pct <= 0:
            return (principal / Decimal(term_months)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Monthly interest rate
        r = (annual_rate_pct / Decimal(100)) / Decimal(12)
        n = Decimal(term_months)

        # (1+r)^n
        compounded = (Decimal(1) + r) ** int(term_months)
        emi = (principal * r * compounded) / (compounded - Decimal(1))
        return emi.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def analyze_finances(self, req: AdvisoryAnalysisRequest) -> AdvisoryAnalysisResponse:
        p = req.profile
        monthly_income = Decimal(str(p.monthly_income))
        monthly_expenses = Decimal(str(p.monthly_expenses))

        surplus = monthly_income - monthly_expenses
        savings_rate = (surplus / monthly_income * Decimal(100)).quantize(Decimal("0.1")) if monthly_income > 0 else Decimal(0)

        # Debt to income: total debt or monthly debt payment / monthly income
        dti = (Decimal(str(p.debt_amount)) / monthly_income).quantize(Decimal("0.001")) if monthly_income > 0 else Decimal(0)

        emi = None
        if req.loan_principal and req.annual_interest_rate_pct and req.loan_term_months:
            emi = self.calculate_emi(
                principal=Decimal(str(req.loan_principal)),
                annual_rate_pct=Decimal(str(req.annual_interest_rate_pct)),
                term_months=req.loan_term_months
            )

        budget_breakdown = {
            "Dining": Decimal(str(p.dining_spend)),
            "Travel": Decimal(str(p.travel_spend)),
            "Grocery": Decimal(str(p.grocery_spend)),
            "Fuel": Decimal(str(p.fuel_spend)),
            "Other": Decimal(str(p.other_spend)),
            "Remaining Savings": max(Decimal(0), surplus)
        }

        recommendations = []
        if savings_rate < 20:
            recommendations.append("Your current savings rate is below the recommended 20% benchmark. Consider reviewing discretionary dining and travel.")
        else:
            recommendations.append(f"Strong savings discipline observed with a {savings_rate}% savings buffer.")

        if dti > Decimal("0.40"):
            recommendations.append("Debt-to-income exceeds 40%. Prioritize debt consolidation or higher amortizations before taking additional credit products.")

        if p.dining_spend > p.travel_spend and p.dining_spend > Decimal(300):
            recommendations.append("High dining expenditure identified; a dining-accelerated rewards card (3x-4x) would maximize annual reward yields.")

        return AdvisoryAnalysisResponse(
            monthly_surplus=surplus.quantize(Decimal("0.01")),
            savings_rate_pct=savings_rate,
            debt_to_income_ratio=dti,
            emi=emi,
            budget_breakdown=budget_breakdown,
            recommendations=recommendations,
            disclaimer="Calculations and insights are for informational simulation purposes only and do not constitute licensed financial underwriting or fiduciary advice."
        )

advisory_service = AdvisoryService()

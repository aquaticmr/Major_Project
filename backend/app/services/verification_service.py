import re
from decimal import Decimal
from typing import List, Dict, Any, Tuple

class VerificationService:
    @staticmethod
    def extract_monetary_values(text: str) -> List[Decimal]:
        # Matches $1,000, 1000 USD, 50.00%, etc.
        patterns = [
            r"\$\s*([0-9,]+(?:\.[0-9]{1,2})?)",
            r"([0-9,]+(?:\.[0-9]{1,2})?)\s*(?:USD|dollars)",
            r"([0-9]+(?:\.[0-9]+)?)\s*%"
        ]
        values = []
        for p in patterns:
            for match in re.finditer(p, text, re.IGNORECASE):
                val_str = match.group(1).replace(",", "")
                try:
                    values.append(Decimal(val_str))
                except Exception:
                    pass
        return values

    def verify_numerical_claims(self, answer: str, source_contexts: List[str]) -> Tuple[bool, List[str]]:
        """Verify whether numbers/percentages quoted in answer appear in the source chunks."""
        answer_nums = self.extract_monetary_values(answer)
        if not answer_nums:
            return True, ["No monetary or numerical percentage claims identified to verify."]

        all_source_text = " ".join(source_contexts)
        source_nums = self.extract_monetary_values(all_source_text)

        unsupported = []
        for num in answer_nums:
            if num not in source_nums:
                unsupported.append(str(num))

        if unsupported:
            return False, [f"Numerical value {u} in answer was not found in retrieved document excerpts." for u in unsupported]

        return True, ["All extracted numerical values match retrieved document sources."]

    def calculate_evidence_score(
        self,
        avg_retrieval_score: float,
        supported_claim_ratio: float,
        consistency_score: float,
        alpha: float = 0.40,
        beta: float = 0.35,
        gamma: float = 0.25
    ) -> float:
        """
        C_evidence = alpha * S_retrieval + beta * E_support + gamma * K_consistency
        """
        # Ensure values in [0, 1]
        s_retrieval = max(0.0, min(1.0, avg_retrieval_score))
        e_support = max(0.0, min(1.0, supported_claim_ratio))
        k_consistency = max(0.0, min(1.0, consistency_score))

        score = (alpha * s_retrieval) + (beta * e_support) + (gamma * k_consistency)
        return round(score, 3)

verification_service = VerificationService()

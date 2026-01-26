# backend/database/models/record_label/popularity.py

from typing import List, Dict, Any

class PopularityMetrics:
    """
    Module 3: Popularity & Scaling Probability Engine
    Predicts the commercial and cultural trajectory of the song.
    """
    def __init__(
        self,
        organic_virality_probability: float,
        best_platforms: List[str],
        cultural_timing: str,
        risk_factors: List[str]
    ):
        self.organic_virality_probability = organic_virality_probability
        self.best_platforms = best_platforms
        self.cultural_timing = cultural_timing
        self.risk_factors = risk_factors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "organic_virality_probability": self.organic_virality_probability,
            "best_platforms": self.best_platforms,
            "cultural_timing": self.cultural_timing,
            "risk_factors": self.risk_factors
        }

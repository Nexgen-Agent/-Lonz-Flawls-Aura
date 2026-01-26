# backend/database/models/record_label/analysis.py

from typing import List, Dict, Any

class EmotionalAnalysis:
    """
    Module 2: Emotional & Reality Analysis
    Detects emotional depth and authenticity.
    """
    def __init__(
        self,
        emotional_bandwidth: List[str],
        emotional_contradictions: List[str],
        authenticity_score: float,
        listener_identification_probability: float,
        sensitive_themes: List[str]
    ):
        self.emotional_bandwidth = emotional_bandwidth
        self.emotional_contradictions = emotional_contradictions
        self.authenticity_score = authenticity_score
        self.listener_identification_probability = listener_identification_probability
        self.sensitive_themes = sensitive_themes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "emotional_bandwidth": self.emotional_bandwidth,
            "emotional_contradictions": self.emotional_contradictions,
            "authenticity_score": self.authenticity_score,
            "listener_identification_probability": self.listener_identification_probability,
            "sensitive_themes": self.sensitive_themes
        }

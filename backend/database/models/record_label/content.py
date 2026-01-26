# backend/database/models/record_label/content.py

from typing import List, Dict, Any

class NarrativeContent:
    """
    Module 5: Narrative & Content Generator
    Generates marketing and narrative framing based on song's DNA.
    """
    def __init__(
        self,
        captions: List[str],
        themes: List[str],
        narrative_angles: List[str],
        framing_options: List[str]
    ):
        self.captions = captions
        self.themes = themes
        self.narrative_angles = narrative_angles
        self.framing_options = framing_options

    def to_dict(self) -> Dict[str, Any]:
        return {
            "captions": self.captions,
            "themes": self.themes,
            "narrative_angles": self.narrative_angles,
            "framing_options": self.framing_options
        }

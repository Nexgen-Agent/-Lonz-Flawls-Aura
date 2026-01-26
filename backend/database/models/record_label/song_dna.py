# backend/database/models/record_label/song_dna.py

from typing import Dict, Any

class SongDNA:
    """
    Module 1: Song Ingestion & DNA Creation
    Represents the foundational elements of a song.
    """
    def __init__(
        self,
        frequency_spectrum: Dict[str, float],
        tempo: float,
        rhythm: str,
        energy: float,
        lyrical_messaging: str,
        emotional_polarity: float,  # -1.0 to 1.0
        pride_vs_regret: float,     # -1.0 to 1.0
        chaos_vs_control: float      # -1.0 to 1.0
    ):
        self.frequency_spectrum = frequency_spectrum
        self.tempo = tempo
        self.rhythm = rhythm
        self.energy = energy
        self.lyrical_messaging = lyrical_messaging
        self.emotional_polarity = emotional_polarity
        self.pride_vs_regret = pride_vs_regret
        self.chaos_vs_control = chaos_vs_control

    def to_dict(self) -> Dict[str, Any]:
        return {
            "frequency_spectrum": self.frequency_spectrum,
            "tempo": self.tempo,
            "rhythm": self.rhythm,
            "energy": self.energy,
            "lyrical_messaging": self.lyrical_messaging,
            "emotional_polarity": self.emotional_polarity,
            "pride_vs_regret": self.pride_vs_regret,
            "chaos_vs_control": self.chaos_vs_control
        }

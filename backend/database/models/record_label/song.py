# backend/database/models/record_label/song.py

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from .song_dna import SongDNA
from .analysis import EmotionalAnalysis
from .popularity import PopularityMetrics
from .improvement import ArtisticImprovement
from .content import NarrativeContent

class SongRecord:
    """
    The central record for a song within the AI Record Label system.
    """
    def __init__(
        self,
        song_id: str,
        title: str,
        artist_id: str,
        audio_url: str,
        lyrics: Optional[str] = None,
        dna: Optional[SongDNA] = None,
        analysis: Optional[EmotionalAnalysis] = None,
        popularity: Optional[PopularityMetrics] = None,
        improvement: Optional[ArtisticImprovement] = None,
        content: Optional[NarrativeContent] = None,
        status: str = "ingested",
        created_at: Optional[datetime] = None
    ):
        self.song_id = song_id
        self.title = title
        self.artist_id = artist_id
        self.audio_url = audio_url
        self.lyrics = lyrics
        self.dna = dna
        self.analysis = analysis
        self.popularity = popularity
        self.improvement = improvement
        self.content = content
        self.status = status
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "song_id": self.song_id,
            "title": self.title,
            "artist_id": self.artist_id,
            "audio_url": self.audio_url,
            "lyrics": self.lyrics,
            "dna": self.dna.to_dict() if self.dna else None,
            "analysis": self.analysis.to_dict() if self.analysis else None,
            "popularity": self.popularity.to_dict() if self.popularity else None,
            "improvement": self.improvement.to_dict() if self.improvement else None,
            "content": self.content.to_dict() if self.content else None,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }

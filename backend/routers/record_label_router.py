# backend/routers/record_label_router.py

from typing import Dict, Any, List, Optional
from backend.services.record_label_service import RecordLabelService

class RecordLabelRouter:
    """
    API router for the Record Label domain.
    Exposes endpoints for song ingestion, analysis, and report generation.
    """
    def __init__(self, record_label_service: RecordLabelService):
        self.record_label_service = record_label_service

    def ingest_song(self, song_data: Dict[str, Any]) -> Dict[str, Any]:
        """Endpoint to ingest a new song and create its DNA."""
        song_id = self.record_label_service.ingest_song(
            title=song_data["title"],
            artist_id=song_data["artist_id"],
            audio_url=song_data["audio_url"],
            lyrics=song_data.get("lyrics")
        )
        return {"message": "Song ingested and DNA created.", "song_id": song_id}

    def analyze_song(self, song_id: str) -> Dict[str, Any]:
        """Endpoint to trigger full emotional and commercial analysis."""
        emotional_analysis = self.record_label_service.analyze_emotional_depth(song_id)
        popularity_metrics = self.record_label_service.assess_commercial_potential(song_id)
        artistic_suggestions = self.record_label_service.get_artistic_suggestions(song_id)
        marketing_assets = self.record_label_service.generate_marketing_assets(song_id)

        return {
            "message": "Full AI analysis complete.",
            "song_id": song_id,
            "analysis_summary": {
                "authenticity_score": emotional_analysis.get("authenticity_score"),
                "virality_probability": popularity_metrics.get("organic_virality_probability"),
                "suggestion_count": len(artistic_suggestions.get("suggestions", []))
            }
        }

    def get_report(self, song_id: str) -> Dict[str, Any]:
        """Endpoint to retrieve the full Song DNA report."""
        report = self.record_label_service.get_full_song_report(song_id)
        return {"song_id": song_id, "report": report}

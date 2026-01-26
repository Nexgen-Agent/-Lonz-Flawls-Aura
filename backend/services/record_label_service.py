# backend/services/record_label_service.py

from typing import Dict, Any, List, Optional
from backend.ai.record_label.engine import RecordLabelAIEngine
from backend.database.models.record_label import (
    SongRecord, SongDNA, EmotionalAnalysis,
    PopularityMetrics, ArtisticImprovement, NarrativeContent
)

class RecordLabelService:
    """
    Orchestrates the record label's AI modules and manages song records.
    It acts as the primary interface for processing songs through the AI pipeline.
    """
    def __init__(self, db_connection: Any):
        self.db_connection = db_connection
        self.songs_collection = db_connection.songs
        self.ai_engine = RecordLabelAIEngine()

    def ingest_song(self, title: str, artist_id: str, audio_url: str, lyrics: Optional[str] = None) -> str:
        """
        Module 1: Song Ingestion & DNA Creation
        Accepts song details, analyzes them, and stores the initial DNA.
        """
        song_id = f"song-{self.songs_collection.count_documents({}) + 1}"

        # Perform DNA analysis
        audio_data = {"tempo": 124.0} # Mock extracted audio properties
        dna_data = self.ai_engine.analyze_song_dna(audio_data, lyrics)
        dna = SongDNA(**dna_data)

        song_record = SongRecord(
            song_id=song_id,
            title=title,
            artist_id=artist_id,
            audio_url=audio_url,
            lyrics=lyrics,
            dna=dna,
            status="dna_created"
        )

        self.songs_collection.insert_one(song_record.to_dict())
        return song_id

    def analyze_emotional_depth(self, song_id: str) -> Dict[str, Any]:
        """
        Module 2: Emotional & Reality Analysis
        Processes the song DNA to understand emotional impact and authenticity.
        """
        song_data = self.songs_collection.find_one({"song_id": song_id})
        if not song_data:
            return {"error": "Song not found"}

        dna_data = song_data.get("dna")
        analysis_data = self.ai_engine.perform_emotional_analysis(dna_data)
        analysis = EmotionalAnalysis(**analysis_data)

        self.songs_collection.update_one(
            {"song_id": song_id},
            {"$set": {"analysis": analysis.to_dict(), "status": "analyzed"}}
        )
        return analysis.to_dict()

    def assess_commercial_potential(self, song_id: str) -> Dict[str, Any]:
        """
        Module 3: Popularity & Scaling Probability Engine
        Evaluates the song's market fit and virality probability.
        """
        song_data = self.songs_collection.find_one({"song_id": song_id})
        if not song_data:
            return {"error": "Song not found"}

        dna_data = song_data.get("dna")
        analysis_data = song_data.get("analysis")

        popularity_data = self.ai_engine.predict_popularity(dna_data, analysis_data)
        popularity = PopularityMetrics(**popularity_data)

        self.songs_collection.update_one(
            {"song_id": song_id},
            {"$set": {"popularity": popularity.to_dict(), "status": "assessed"}}
        )
        return popularity.to_dict()

    def get_artistic_suggestions(self, song_id: str) -> Dict[str, Any]:
        """
        Module 4: Artistic Improvement Without Sabotage
        Provides structural and technical suggestions to enhance the song.
        """
        song_data = self.songs_collection.find_one({"song_id": song_id})
        if not song_data:
            return {"error": "Song not found"}

        dna_data = song_data.get("dna")
        improvement_data = self.ai_engine.suggest_artistic_improvements(dna_data)
        improvement = ArtisticImprovement(**improvement_data)

        self.songs_collection.update_one(
            {"song_id": song_id},
            {"$set": {"improvement": improvement.to_dict()}}
        )
        return improvement.to_dict()

    def generate_marketing_assets(self, song_id: str) -> Dict[str, Any]:
        """
        Module 5: Narrative & Content Generator
        Generates narrative-aligned captions and themes for marketing.
        """
        song_data = self.songs_collection.find_one({"song_id": song_id})
        if not song_data:
            return {"error": "Song not found"}

        dna_data = song_data.get("dna")
        analysis_data = song_data.get("analysis")

        content_data = self.ai_engine.generate_narrative_content(dna_data, analysis_data)
        content = NarrativeContent(**content_data)

        self.songs_collection.update_one(
            {"song_id": song_id},
            {"$set": {"content": content.to_dict()}}
        )
        return content.to_dict()

    def get_full_song_report(self, song_id: str) -> Dict[str, Any]:
        """
        Retrieves the complete Song DNA and all associated AI analysis.
        """
        song_data = self.songs_collection.find_one({"song_id": song_id}, {"_id": 0})
        return song_data or {"error": "Song not found"}

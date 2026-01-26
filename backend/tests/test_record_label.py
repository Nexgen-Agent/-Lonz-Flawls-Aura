# backend/tests/test_record_label.py

import unittest
import sys
import os

# Ensure the backend directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.services.record_label_service import RecordLabelService
from backend.routers.record_label_router import RecordLabelRouter
from backend.database.mock_connection import get_db

class TestRecordLabelSystem(unittest.TestCase):
    def setUp(self):
        self.db = get_db()
        self.service = RecordLabelService(db_connection=self.db)
        self.router = RecordLabelRouter(record_label_service=self.service)

    def test_full_pipeline(self):
        """Tests the entire song ingestion and analysis pipeline."""
        # 1. Ingest
        song_data = {
            "title": "Midnight Reflections",
            "artist_id": "artist-456",
            "audio_url": "https://storage.aura.inc/audio/midnight_reflections.wav",
            "lyrics": "Walking through the rain, memories calling my name..."
        }
        res = self.router.ingest_song(song_data)
        self.assertEqual(res["message"], "Song ingested and DNA created.")
        song_id = res["song_id"]

        # 2. Analyze
        analysis_res = self.router.analyze_song(song_id)
        self.assertEqual(analysis_res["message"], "Full AI analysis complete.")
        self.assertGreater(analysis_res["analysis_summary"]["authenticity_score"], 0)

        # 3. Report
        report_res = self.router.get_report(song_id)
        report = report_res["report"]
        self.assertEqual(report["title"], "Midnight Reflections")
        self.assertIsNotNone(report["dna"])
        self.assertIsNotNone(report["analysis"])
        self.assertIsNotNone(report["popularity"])
        self.assertIsNotNone(report["improvement"])
        self.assertIsNotNone(report["content"])
        self.assertEqual(report["status"], "assessed")

if __name__ == "__main__":
    unittest.main()

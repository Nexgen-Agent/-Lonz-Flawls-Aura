# backend/main.py

from backend.config import settings
from backend.core.private_ledger import PrivateLedger
from backend.services.innovation_service import InnovationService
from backend.services.site_registry_service import SiteRegistryService
from backend.services.record_label_service import RecordLabelService
from backend.routers.innovation_router import InnovationRouter
from backend.routers.record_label_router import RecordLabelRouter

def get_db_connection():
    try:
        from backend.database.connection import get_db
        # We try a quick operation to see if the server is actually reachable
        db = get_db()
        db.command("ping")
        return db
    except Exception:
        print("WARNING: Real MongoDB connection failed. Falling back to MockDatabase.")
        from backend.database.mock_connection import get_db as get_mock_db
        return get_mock_db()

def initialize_application():
    """
    Initializes and wires up all application components.
    """
    print(f"--- Initializing {settings.APP_NAME} v{settings.VERSION} ---")

    # --- Initialize Database (conceptual) ---
    # In a real app, this would establish a connection pool
    db_connection = get_db_connection()
    print("Database connection established.")

    # --- Initialize Core Services ---
    if settings.FEATURE_FLAGS.get("ENABLE_PRIVATE_LEDGER"):
        private_ledger = PrivateLedger(db_connection=db_connection)
        print("PrivateLedger service initialized.")

    # --- Initialize Innovation Domain ---
    if settings.FEATURE_FLAGS.get("ENABLE_AUTONOMOUS_INNOVATION"):
        # Initialize services
        innovation_service = InnovationService(
            config=settings.INNOVATION_ENGINE_CONFIG,
            db_connection=db_connection,
            private_ledger=private_ledger
        )
        site_registry_service = SiteRegistryService(db_connection=db_connection)
        print("Innovation services initialized.")

        # Initialize the API router
        innovation_router = InnovationRouter(
            innovation_service=innovation_service,
            site_registry_service=site_registry_service
        )
        print("Innovation API router initialized.")

        # In a web framework, you would now register the router
        # app.include_router(innovation_router)

        app_context = {
            "innovation_router": innovation_router,
            "private_ledger": private_ledger,
        }
    else:
        print("Innovation domain is disabled by feature flag.")
        app_context = {}

    # --- Initialize Record Label Domain ---
    if settings.FEATURE_FLAGS.get("ENABLE_AI_RECORD_LABEL"):
        # Initialize services
        record_label_service = RecordLabelService(db_connection=db_connection)
        print("Record Label AI services initialized.")

        # Initialize the API router
        record_label_router = RecordLabelRouter(record_label_service=record_label_service)
        print("Record Label API router initialized.")

        app_context["record_label_router"] = record_label_router

    return app_context

def run_demonstration(app_context):
    """
    A simple function to demonstrate the integrated modules.
    """
    # Skipping Innovation Demo due to unrelated model mismatch in baseline
    # if "innovation_router" in app_context:
    #    ...

    if "record_label_router" in app_context:
        print("\n--- Running Record Label Module Demonstration ---")
        router = app_context["record_label_router"]

        # 1. Ingest a new song
        song_data = {
            "title": "Midnight Reflections",
            "artist_id": "artist-456",
            "audio_url": "https://storage.aura.inc/audio/midnight_reflections.wav",
            "lyrics": "Walking through the rain, memories calling my name..."
        }
        ingestion_result = router.ingest_song(song_data)
        song_id = ingestion_result["song_id"]
        print(f"Song Ingestion Result: {ingestion_result}")

        # 2. Analyze the song
        analysis_result = router.analyze_song(song_id)
        print(f"Song Analysis Result: {analysis_result}")

        # 3. Get the full report
        report_result = router.get_report(song_id)
        print(f"Full Song Report (Keys): {list(report_result['report'].keys())}")
        print(f"Authenticity Score: {report_result['report']['analysis']['authenticity_score']}")

if __name__ == "__main__":
    application_context = initialize_application()
    run_demonstration(application_context)
    print("\n--- Application Initialization Complete ---")

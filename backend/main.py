# backend/main.py

from backend.config import settings
from backend.core.private_ledger import PrivateLedger
from backend.services.innovation_service import InnovationService
from backend.services.site_registry_service import SiteRegistryService
from backend.routers.innovation_router import InnovationRouter
from backend.database.connection import get_db

def initialize_application():
    """
    Initializes and wires up all application components.
    """
    print(f"--- Initializing {settings.APP_NAME} v{settings.VERSION} ---")

    # --- Initialize Database (conceptual) ---
    # In a real app, this would establish a connection pool
    db_connection = get_db()
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

        return {
            "innovation_router": innovation_router,
            "private_ledger": private_ledger,
        }
    else:
        print("Innovation domain is disabled by feature flag.")
        return {}

def run_demonstration(app_context):
    """
    A simple function to demonstrate the integrated innovation module.
    """
    if "innovation_router" in app_context:
        print("\n--- Running Innovation Module Demonstration ---")
        router = app_context["innovation_router"]

        # 1. Register a new site
        site_data = {"name": "Aura Client Portal", "url": "https://portal.aura.inc"}
        registration_result = router.register_site(site_data)
        print(f"Site Registration Result: {registration_result}")

        # 2. List active sites
        active_sites = router.list_sites()
        print(f"Active Sites: {active_sites}")

        # 3. Trigger proposal creation
        proposal_result = router.create_proposal()
        print(f"Proposal Creation Result: {proposal_result}")

        # 4. Approve a (mock) proposal
        approval_result = router.approve_proposal("prop-123")
        print(f"Proposal Approval Result: {approval_result}")

if __name__ == "__main__":
    application_context = initialize_application()
    run_demonstration(application_context)
    print("\n--- Application Initialization Complete ---")

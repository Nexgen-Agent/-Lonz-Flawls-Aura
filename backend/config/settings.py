# backend/config/settings.py

# --- General Application Settings ---
APP_NAME = "Aura Autonomous Backend"
VERSION = "1.0.0"
DEBUG_MODE = True # Set to False in production

# --- Database Configuration ---
# In a real application, use environment variables for sensitive data
DATABASE_URL = "mongodb://localhost:27017/aura_main"

import os

# --- Cryptography Settings ---
# This key should be loaded securely, e.g., from a secret manager
MASTER_ENCRYPTION_KEY = os.getenv("MASTER_ENCRYPTION_KEY", "default-insecure-key-for-dev")

# --- Innovation Engine Settings ---
INNOVATION_ENGINE_CONFIG = {
    "enabled": True,
    "opportunity_scan_interval_hours": 24,
    "proposal_generation_model": "gpt-4-turbo",
    "max_active_proposals": 10,
}

# --- Service-Specific Settings ---
SITE_REGISTRY_SERVICE = {
    "cache_ttl_seconds": 3600,
}

# --- Record Label AI Settings ---
RECORD_LABEL_CONFIG = {
    "enabled": True,
    "min_authenticity_threshold": 0.7,
    "virality_model_version": "v1.2",
}

# --- Feature Flags ---
FEATURE_FLAGS = {
    "ENABLE_AUTONOMOUS_INNOVATION": True,
    "ENABLE_PRIVATE_LEDGER": True,
    "ENABLE_INNOVATION_RECRUITER": True,
    "ENABLE_AI_RECORD_LABEL": True,
}

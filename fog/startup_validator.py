import os
import sys

def validate_startup():
    """
    Validates essential environment variables at startup.
    """
    print("--- FOG STARTUP VALIDATION ---")

    # REQUIRED section
    REQUIRED = [
        "MASTER_ENCRYPTION_KEY"
    ]

    missing_required = []
    for var in REQUIRED:
        if not os.getenv(var):
            print(f"  ✖ {var} not set")
            missing_required.append(var)

    if missing_required:
        print("\nCRITICAL: Missing required environment variables. Exiting.")
        sys.exit(1)

    print("REQUIRED checks passed.\n")

    # INTEGRATION CHECKS section
    INTEGRATIONS = {
        "RENDER_API_KEY": "Render integration disabled",
        "RENDER_SERVICE_ID": "Render integration disabled",
        "VERCEL_TOKEN": "Vercel integration disabled",
        "VERCEL_PROJECT_ID": "Vercel integration disabled",
        "NEON_API_KEY": "Neon integration disabled",
        "NEON_PROJECT_ID": "Neon integration disabled",
        "JULES_API_KEY": "Jules direct API disabled",
        "GITHUB_TOKEN": "GitHub integration disabled",
        "JULES_DEFAULT_REPO": "Jules repo integration disabled",
        "TAVILY_API_KEY": "Tavily integration disabled",
        "PERPLEXITY_API_KEY": "Perplexity integration disabled"
    }

    print("CHECKING INTEGRATIONS...")
    for var, message in INTEGRATIONS.items():
        if not os.getenv(var):
            print(f"  ⚠ {var} not set — {message}")

if __name__ == "__main__":
    validate_startup()

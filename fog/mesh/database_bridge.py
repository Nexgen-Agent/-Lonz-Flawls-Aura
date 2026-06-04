import os
import requests

class DatabaseBridge:
    """
    Bridge for communicating with the UEOS environment.
    """
    def __init__(self):
        self.db_url = os.getenv("UEOS_DATABASE_URL")

    def ping_ueos(self):
        """
        Pings the UEOS REST API to check health.
        """
        api_url = os.getenv("UEOS_API_URL")
        admin_key = os.getenv("UEOS_PLATFORM_ADMIN_KEY")

        if not api_url or not admin_key:
            return {"status": "unreachable", "error": "Missing UEOS configuration"}

        url = f"{api_url.rstrip('/')}/health"
        headers = {"Authorization": f"Bearer {admin_key}"}

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            return {
                "status": "connected",
                "ueos_version": data.get("version", "unknown")
            }
        except Exception as e:
            return {"status": "unreachable", "error": str(e)}

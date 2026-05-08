from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/jules/status")
async def get_jules_status():
    """
    Returns the status of the Jules integration.
    """
    jules_api_key = os.getenv("JULES_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    return {
        "status": "online",
        "jules_api_key": "configured" if jules_api_key else "missing",
        "jules_github_token": "configured" if github_token else "missing"
    }

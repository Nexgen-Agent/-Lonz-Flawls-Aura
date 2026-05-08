from fastapi import FastAPI
import os
from fog.mesh.database_bridge import DatabaseBridge

app = FastAPI()

@app.get("/health")
async def health_check():
    bridge = DatabaseBridge()
    ueos_status = bridge.ping_ueos()

    return {
        "status": "ok",
        "ueos_connection": ueos_status
    }

import os
from fastapi import FastAPI, Request, HTTPException, Query
import requests
from dotenv import load_dotenv
import uuid

load_dotenv()

API_PASSWORD = os.getenv("API_PASSWORD")

app = FastAPI(title="Earthquake Data API")

SOURCE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

@app.get("/earthquakes")
async def get_earthquakes(
    request: Request,
    start_time: str = Query(..., description="Start time (example, 2023-01-01)"),
    end_time: str = Query(..., description="End time (example, 2023-01-02)"),
    latitude: float = Query(..., description="Latitude (example, 37.7749)"),
    longitude: float = Query(..., description="Longitude (example, -122.4194)"),
    max_radius_km: float = Query(..., description="Maximum radius in km"),
    min_magnitude: float = Query(..., description="Minimal magnitude")
):
    api_key = request.headers.get("X-API-Key")
    if api_key != API_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized: Wrong API key")

    params = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": end_time,
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": max_radius_km,
        "minmagnitude": min_magnitude
    }

    try:
        response = requests.get(SOURCE_URL, headers={"Accept": "application/json"}, params=params)
        response.raise_for_status() 
        data = response.json()

        results = [
            {
                "id": str(uuid.uuid4()),
                "place": feature["properties"]["place"],
                "magnitude": feature["properties"]["mag"]
            }
            for feature in data["features"]
        ]

        return results

    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Request error to USGS API: {str(e)}")
import os
import httpx
from fastapi import HTTPException

COURSE_CATALOG_URL = os.getenv("COURSE_CATALOG_URL", "http://localhost:8001")

def fetch_course(course_id: int) -> dict:
    try:
        response = httpx.get(
            f"{COURSE_CATALOG_URL.rstrip('/')}/courses/{course_id}",
            timeout=3.0,
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Course Catalog Service is unavailable",
        )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Course does not exist")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Course Catalog returned an unexpected response")
    return response.json()

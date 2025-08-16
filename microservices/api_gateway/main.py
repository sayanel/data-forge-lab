import json
import httpx
from redis.asyncio import Redis
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware


CACHE_TTL = 120  # seconds
CACHEABLE_SERVICES = {"persons", "habits", "habit_events"}

RATE_LIMIT = 20  # requests
RATE_WINDOW = 1  # second

app = FastAPI(title="Data Forge Lab Gateway")
redis_client = Redis(host="localhost", port=6379, db=0)
httpx_client = httpx.AsyncClient(timeout=10.0)


@app.on_event("startup")
async def startup_event():
    global httpx_client
    httpx_client = httpx.AsyncClient(timeout=10.0)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Target base URLs for backend services
BACKEND_ROUTES = {
    "persons": "http://localhost:5000/api/persons",
    "habits": "http://localhost:5000/api/habits",
    "habit_events": "http://localhost:5000/api/habit_events",
    "analytics": "http://localhost:5000/api/analytics",
    "system": "http://localhost:5000/api/system",
}


@app.api_route("/api/{service}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, request: Request, path: Optional[str] = ""):
    if service not in BACKEND_ROUTES:
        return JSONResponse(status_code=404, content={"detail": f"Unknown service '{service}'"})

    target_url = BACKEND_ROUTES[service]
    if path:
        target_url += f"/{path}"

    query_params = request.url.query
    if query_params:
        target_url += f"?{query_params}"

    try:
        response = await httpx_client.request(
            method=request.method,
            url=target_url,
            headers=dict(request.headers),
            content=await request.body(),
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type"),
        )

    except httpx.RequestError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.middleware("http")
async def redis_rate_limiter(request: Request, call_next):
    # Use X-Forwarded-For if behind a proxy, otherwise fall back to client.host
    client_ip = request.headers.get("X-Forwarded-For", request.client.host)
    key = f"rate_limit:{client_ip}"

    try:
        # Async incr and expire
        current_count = await redis_client.incr(key)
        if current_count == 1:
            await redis_client.expire(key, RATE_WINDOW)
        if current_count > RATE_LIMIT:
            print(f"[Rate limit] Exceeded for IP: {client_ip}")
            return PlainTextResponse("Too many requests", status_code=429)
    except Exception as e:
        print(f"[Rate limit] Error for IP {client_ip}: {e}")

    # Proceed to the next middleware/route
    response = await call_next(request)
    return response

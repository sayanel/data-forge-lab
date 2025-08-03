import httpx
import redis
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware


RATE_LIMIT = 20  # requests
RATE_WINDOW = 1  # second


redis_client = redis.Redis(host="localhost", port=6379, db=0)


app = FastAPI(title="Data Forge Lab Gateway")

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

    print(f"Proxying to: {target_url}")

    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=10.0
            )
            return JSONResponse(status_code=response.status_code, content=response.json())
        except httpx.RequestError as e:
            return JSONResponse(status_code=500, content={"error": str(e)})


@app.middleware("http")
async def redis_rate_limiter(request: Request, call_next):
    client_ip = request.client.host
    key = f"rate_limit: {client_ip}"

    try:
        current_count = redis_client.incr(key)
        if current_count == 1:
            redis_client.expire(key, RATE_WINDOW)

        if current_count > RATE_LIMIT:
            return PlainTextResponse("Too many requests", status_code=429)

    except redis.RedisError as e:
        print(f"Redis error: {e}")
        # Let the request through on Redis failure
        pass

    response = await call_next(request)
    return response

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langserve import add_routes
from redis import Redis

from helpers import get_chain
from settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, API_ACCESS_KEY

API_KEY_HEADER = "X-API-KEY"

app = FastAPI()

redis = Redis(
  host=REDIS_HOST,
  port=REDIS_PORT,
  password=REDIS_PASSWORD,
  ssl=True
)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host

    rate_limit = 5
    rate_window = 60 # seconds
    api_key = request.headers.get(API_KEY_HEADER)
    rate_limit_key = f"rate_limit:{client_ip}"
    access_total_key = f"api_access:{client_ip}"

    if api_key is None:
        return JSONResponse(status_code=400, content={"detail": "Invalid API key"})

    if api_key != API_ACCESS_KEY:
        return JSONResponse(status_code=400, content={"detail": "Invalid API key"})
   
    rl_current_value = redis.get(rate_limit_key)

    if rl_current_value is None:
        redis.set(rate_limit_key, 1, rate_window)
    else:
        redis.incr(rate_limit_key)
    
    final_value = redis.get(rate_limit_key)

    try:
        if int(final_value) > rate_limit:
            return JSONResponse(status_code=429, content={"error": "Slow down, you are making too many requests."})
    except ValueError:
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    access_current_val = redis.get(access_total_key)

    if access_current_val is None:
        redis.set(access_total_key, 1)
    else:
        redis.incr(access_total_key)

    response = await call_next(request)
    return response

@app.get("/")
def home_page():
    return {"hello": "world"}

chain = get_chain()

add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
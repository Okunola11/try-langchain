import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langserve import add_routes

from helpers import get_chain

app = FastAPI()

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
    uvicorn.run(app, host="localhost", port=8100)
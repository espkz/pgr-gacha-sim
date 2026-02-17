from fastapi import FastAPI
from app.routers import pull

app = FastAPI()

app.include_router(pull.router)

@app.get("/")
def root():
    return{"message" : "PGR Gacha API running"}
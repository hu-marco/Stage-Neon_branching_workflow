from fastapi import FastAPI
from routers import database

app = FastAPI(
    title="E-commerce"
)

@app.get("/")
def root():
    return {"Hello":"World"}

app.include_router(database.router)
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.mongo import connectDB
from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())

app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"]
)
connection = connectDB()
db = connection.challenge

@app.get("/")
async def root():
    return {"message": "Server running..."}

from routers.product import *
from routers.money import *
from routers.payment import *

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=int(os.getenv('FASTAPI_PORT')), reload=True)
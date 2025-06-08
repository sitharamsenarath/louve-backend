from fastapi import FastAPI
from app.api.api_v1 import router as api_v1_router
from fastapi.middleware.cors import CORSMiddleware
from app.core import firebase

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/v1")
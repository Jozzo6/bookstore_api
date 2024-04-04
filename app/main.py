import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import user_router, book_router, auth_router
from app.middleware.auth import jwt_auth_middleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.middleware("http")(jwt_auth_middleware)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(book_router.router)

@app.get("/health", response_class=PlainTextResponse)
def healthcheck():
    return "200"

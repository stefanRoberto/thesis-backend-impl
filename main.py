from fastapi import FastAPI
import models
from database import engine, SessionLocal

app = FastAPI()

# TODO: Add API routes
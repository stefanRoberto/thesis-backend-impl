from fastapi import FastAPI
import database
from routes import router

app = FastAPI()

database.create_database()

app.include_router(router=router, prefix='/api')

from fastapi import FastAPI
from app.api.routes import router
from app.models.price import Base
from app.core.config import DATABASE_URL
from sqlalchemy import create_engine

app = FastAPI(title="Market Data Service")
app.include_router(router)

# Initialize database
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Market Data Service running"}
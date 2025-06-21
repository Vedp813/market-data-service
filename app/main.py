import logging
import threading
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from app.api.routes import router
from app.models.price import Base
from app.core.config import DATABASE_URL
from app.kafka_consumer import consume_market_data

# Configure logging for visibility in production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database engine and sessionmaker for DB connections
engine = create_engine(DATABASE_URL, pool_pre_ping=True)  # pool_pre_ping avoids stale DB connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="Market Data Service")

# Include API router from app/api/routes.py
app.include_router(router)

def init_db():
    """Create all tables if they don't exist."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created or verified.")
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        # You might want to re-raise or handle more gracefully in prod

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Market Data Service running"}

@app.on_event("startup")
async def startup_event():
    """
    Startup event handler to initialize DB and start Kafka consumer thread.
    The consumer runs in a daemon thread so it won't block server shutdown.
    """
    logger.info("Starting up Market Data Service...")
    init_db()

    kafka_thread = threading.Thread(target=consume_market_data, daemon=True)
    kafka_thread.start()
    logger.info("Kafka consumer thread started.")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler, use if you need to cleanup resources."""
    logger.info("Shutting down Market Data Service...")
    # If consume_market_data uses a graceful shutdown, signal it here


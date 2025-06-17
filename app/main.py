from fastapi import FastAPI

app = FastAPI(title="Market Data Service")

@app.get("/")
def root():
    return {"message": "Market Data Service running"}

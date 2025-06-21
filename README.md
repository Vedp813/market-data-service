# Market Data Service – Project Setup Documentation

## Stage 1: Environment & Docker Infrastructure Setup

### 1.1 Project Structure
```
market-data-service/
├── app/                  # FastAPI application code
├── Dockerfile            # Dockerfile for FastAPI API
├── docker-compose.yml    # Multi-container setup for API, PostgreSQL, Kafka, Adminer
├── test
└──  requirements.txt           
```

### 1.2 Python Virtual Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
---

## Stage 2: Docker Compose & Service Orchestration

### 2.1 Docker Services
`docker-compose.yml` defines the following services:

- **api** – FastAPI backend (on port `8000`)
- **postgres** – PostgreSQL DB (on port `5432`)
- **zookeeper** – Kafka dependency
- **kafka** – Message broker (on port `9092`)
- **adminer** – Web-based DB GUI (on port `8080`)

### 2.2 PostgreSQL Configuration
- Username: `postgres`
- Password: `postgres`
- Database: `marketdata`

### 2.3 Running the Stack
```bash
docker-compose up --build
```

### 2.4 Accessing Adminer (PostgreSQL GUI)
- URL: [http://localhost:8080](http://localhost:8080)
- System: PostgreSQL
- Server: `postgres`
- Username: `postgres`
- Password: `postgres`
- Database: `marketdata`

---

## Stage 3: Kafka Streaming Pipeline Integration

In this stage, the system streams market data through a Kafka pipeline to compute and store moving averages in real time.

---

### Data Flow Overview

1. `GET /prices/latest?symbol=AAPL` is called.
2. The FastAPI service:
   - Fetches the latest price using Yahoo Finance (`yfinance`)
   - Stores the price in the `prices` table
   - Publishes a Kafka message to `price-events` topic
3. Kafka consumer:
   - Listens for new events from `price-events`
   - Fetches the last 5 prices for the symbol
   - Calculates the 5-point moving average
   - Upserts the result into `symbol_averages`

### Kafka Message Schema

Each price event message sent to Kafka has the following format:

```json
{
  "symbol": "AAPL",
  "price": 196.58,
  "timestamp": "2025-06-19T22:05:53.620194",
  "provider": "yahoo_finance",
  "raw_response_id": "uuid-here"
}
```
---

# Market Data Service - Stage 4

## Overview

This project implements a **real-time market data microservice** using **FastAPI**, **Kafka**, **PostgreSQL**, and **SQLAlchemy**.

### Stage 4 Goals:
- Kafka consumer subscribes to the `price-events` topic.
- Processes incoming stock price messages in real-time.
- Computes a 5-point **moving average** for each stock symbol.
- Stores the computed averages in a PostgreSQL database.
- Exposes a REST API to fetch the latest moving average for a symbol.

---

## Technologies Used

| Tool           | Purpose                                      |
|----------------|----------------------------------------------|
| **FastAPI**    | Building REST APIs                           |
| **Kafka**      | Streaming price events                       |
| **PostgreSQL** | Relational database                          |
| **SQLAlchemy** | ORM for database access                      |
| **Docker**     | Containerized Kafka and PostgreSQL setup     |
| **Pydantic**   | Schema validation                            |


## Environment Configuration

Create a `.env` file in the root directory of the project with the following content:

```env
# .env

# Postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=marketdata
POSTGRES_PORT=5433

# API
DATABASE_URL=postgresql://postgres:postgres@localhost:${POSTGRES_PORT}/marketdata

# Kafka
KAFKA_BROKER=localhost:9092

```
---
## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/market-data-service.git
   cd market-data-service

2. **Create and Activate a Python Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install Python Dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Start Kafka and PostgreSQL with Docker:**

   ```bash
   docker-compose up --build

5. ** Start the FastAPI Backend:**

   ```bash
   uvicorn app.main:app --reload

6. ** Fetch the Moving Average and Latest price via API:**

   ```bash
   curl "http://localhost:8000/prices/movingaverage?symbol=AAPL"
   curl "http://localhost:8000/prices/latest?symbol=AAPL"







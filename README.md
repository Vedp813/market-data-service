# Market Data Service – Project Setup Documentation

## Stage 1: Environment & Docker Infrastructure Setup

### 1.1 Project Structure
```
market-data-service/
├── app/                  # FastAPI application code
├── Dockerfile            # Dockerfile for FastAPI API
├── docker-compose.yml    # Multi-container setup for API, PostgreSQL, Kafka, Adminer
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

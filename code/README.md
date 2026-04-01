# QuantumNest Capital

Advanced financial platform with AI-powered analytics, portfolio management, and blockchain integration.

---

## Quick Start (Docker)

```bash
# 1. Clone / unzip the project
cd quantumnest

# 2. Create your environment file
cp .env.example .env
#    → Open .env and set SECRET_KEY, API_SECRET_KEY (and POSTGRES_PASSWORD for prod)

# 3. Start all services
docker compose up -d

# 4. (First run only) initialise the database
docker compose --profile migrate run --rm migrate

# 5. Open the API docs
open http://localhost:8000/docs
```

### With the blockchain node (optional)

```bash
docker compose --profile blockchain up -d
```

### Development mode (live reload)

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

## Manual Setup (without Docker)

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ **or** SQLite (dev only)
- Redis 7+
- Node.js 20+ (blockchain only)

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env              # edit values as needed

# Run development server
python run_flask.py
# → API available at http://localhost:8000
# → Docs at         http://localhost:8000/docs
```

### Blockchain (optional)

```bash
cd blockchain
npm install
npx hardhat node                  # local Ethereum node on :8545
npx hardhat run scripts/deploy.js --network localhost
```

---

## Project Structure

```
code/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers (users, portfolio, market, ai, blockchain, admin)
│   │   ├── auth/         # JWT authentication & RBAC
│   │   ├── ai/           # LSTM, GARCH, fraud detection, portfolio optimisation
│   │   ├── core/         # Config, logging, security manager
│   │   ├── db/           # SQLAlchemy engine, session, database manager
│   │   ├── middleware/    # Rate-limiting & security headers
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Market data, risk management, trading
│   │   └── workers/      # Background task queue
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── blockchain/
│   ├── contracts/        # Solidity smart contracts
│   ├── scripts/          # Hardhat deployment scripts
│   ├── Dockerfile
│   └── hardhat.config.js
├── scripts/
│   └── init.sql          # PostgreSQL bootstrap
├── docker-compose.yml
├── docker-compose.dev.yml
└── .env.example
```

---

## API Overview

| Prefix        | Description                            |
| ------------- | -------------------------------------- |
| `GET /`       | Welcome + version                      |
| `GET /health` | Health check                           |
| `POST /token` | OAuth2 password flow — get JWT         |
| `/users`      | User registration, profile, management |
| `/portfolio`  | Portfolio CRUD, assets, performance    |
| `/market`     | Assets, prices, market data, news      |
| `/ai`         | Predictions, optimisation, sentiment   |
| `/blockchain` | Smart contracts, wallets, tokenisation |
| `/admin`      | Dashboard, user admin, system logs     |
| `GET /docs`   | Interactive Swagger UI                 |

---

## Running Tests

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Environment Variables

See `backend/.env.example` for the full list. Key variables:

| Variable          | Required | Description                      |
| ----------------- | -------- | -------------------------------- |
| `SECRET_KEY`      | ✅       | JWT signing key (min 32 chars)   |
| `API_SECRET_KEY`  | ✅       | API key signing secret           |
| `DATABASE_URL`    |          | SQLite (dev) or PostgreSQL URL   |
| `REDIS_URL`       |          | Redis connection URL             |
| `ALLOWED_ORIGINS` |          | Comma-separated CORS origins     |
| `OPENAI_API_KEY`  |          | For AI financial advisor feature |

---

## Security Notes

- Never commit `.env` files to version control
- In production, set `ENVIRONMENT=production` and provide an explicit `SECRET_KEY`
- The `ALLOWED_ORIGINS=*` default is **only** acceptable in local development
- The blockchain `PRIVATE_KEY` in `.env.example` is the well-known Hardhat test account — never use it on mainnet

---

## Tech Stack

**Backend:** FastAPI · SQLAlchemy 2 · Pydantic v2 · PostgreSQL / SQLite · Redis  
**AI / ML:** scikit-learn · NumPy · Pandas · statsmodels · CVXPY  
**Blockchain:** Hardhat · Solidity 0.8.19 · Web3.py  
**Infrastructure:** Docker · Docker Compose · Gunicorn + Uvicorn workers

"""Development entry-point for the FastAPI application."""

import os

# Must be set before importing the app so Settings picks them up.
os.environ.setdefault("DATABASE_URL", "sqlite:///./quantumnest.db")
os.environ.setdefault(
    "SECRET_KEY", "dev-secret-key-min-32-characters-long-for-security-only"
)
os.environ.setdefault("API_SECRET_KEY", "dev-api-secret-key-min-32-characters-here")
os.environ.setdefault("ENVIRONMENT", "development")

if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("QuantumNest Capital API – Development Server")
    print("=" * 60)
    print("Docs:   http://127.0.0.1:8000/docs")
    print("Health: http://127.0.0.1:8000/health")
    print("=" * 60 + "\n")

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )

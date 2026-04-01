from datetime import datetime, timedelta
from typing import Any, List, Optional

from app.db.database import get_db
from app.main import get_current_active_user
from app.models import models
from app.schemas import schemas
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/assets/", response_model=List[schemas.Asset])
def get_assets(
    skip: int = 0,
    limit: int = 100,
    asset_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    query = db.query(models.Asset).filter(models.Asset.is_active == True)
    if asset_type:
        query = query.filter(models.Asset.asset_type == asset_type)
    if search:
        query = query.filter(
            models.Asset.symbol.ilike(f"%{search}%")
            | models.Asset.name.ilike(f"%{search}%")
        )
    assets = query.offset(skip).limit(limit).all()
    return assets


@router.post("/assets/", response_model=schemas.Asset, status_code=201)
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    existing = (
        db.query(models.Asset)
        .filter(models.Asset.symbol == asset.symbol.upper())
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409, detail="Asset with this symbol already exists"
        )
    db_asset = models.Asset(
        symbol=asset.symbol.upper(),
        name=asset.name,
        asset_type=asset.asset_type,
        description=asset.description,
        exchange=asset.exchange,
        currency=asset.currency or "USD",
        sector=asset.sector,
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.get("/assets/{asset_id}", response_model=schemas.Asset)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset


@router.get("/assets/symbol/{symbol}", response_model=schemas.Asset)
def get_asset_by_symbol(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    db_asset = (
        db.query(models.Asset).filter(models.Asset.symbol == symbol.upper()).first()
    )
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset


@router.get("/assets/{asset_id}/price")
def get_asset_price(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    latest_price = (
        db.query(models.AssetPrice)
        .filter(models.AssetPrice.asset_id == asset_id)
        .order_by(models.AssetPrice.timestamp.desc())
        .first()
    )
    current_price = (
        float(latest_price.price)
        if latest_price
        else float(db_asset.current_price or 0)
    )
    return {
        "asset_id": asset_id,
        "symbol": db_asset.symbol,
        "name": db_asset.name,
        "price": current_price,
        "currency": db_asset.currency,
        "timestamp": latest_price.timestamp if latest_price else datetime.utcnow(),
    }


@router.get("/assets/{asset_id}/price_history")
def get_asset_price_history(
    asset_id: int,
    period: str = Query("1m", regex="^(1d|1w|1m|3m|6m|1y)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    period_map = {
        "1d": timedelta(days=1),
        "1w": timedelta(weeks=1),
        "1m": timedelta(days=30),
        "3m": timedelta(days=90),
        "6m": timedelta(days=180),
        "1y": timedelta(days=365),
    }
    end_date = datetime.utcnow()
    start_date = end_date - period_map.get(period, timedelta(days=30))

    price_history = (
        db.query(models.AssetPrice)
        .filter(
            models.AssetPrice.asset_id == asset_id,
            models.AssetPrice.timestamp >= start_date,
            models.AssetPrice.timestamp <= end_date,
        )
        .order_by(models.AssetPrice.timestamp.asc())
        .all()
    )
    return {
        "asset_id": asset_id,
        "symbol": db_asset.symbol,
        "name": db_asset.name,
        "period": period,
        "count": len(price_history),
        "data": [
            {
                "timestamp": price.timestamp.isoformat(),
                "price": float(price.price),
                "open": float(price.open_price) if price.open_price else None,
                "high": float(price.high_price) if price.high_price else None,
                "low": float(price.low_price) if price.low_price else None,
                "close": float(price.close_price) if price.close_price else None,
                "volume": float(price.volume) if price.volume else None,
            }
            for price in price_history
        ],
    }


@router.post(
    "/assets/{asset_id}/price", response_model=schemas.AssetPrice, status_code=201
)
def add_asset_price(
    asset_id: int,
    price_data: schemas.AssetPriceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    db_price = models.AssetPrice(
        asset_id=asset_id,
        price=price_data.price,
        open_price=price_data.open_price,
        high_price=price_data.high_price,
        low_price=price_data.low_price,
        close_price=price_data.close_price,
        volume=price_data.volume,
    )
    db.add(db_price)
    db_asset.current_price = price_data.price
    db_asset.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_price)
    return db_price


@router.get("/market_summary")
def get_market_summary(
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    return {
        "indices": [
            {
                "name": "S&P 500",
                "value": 5350.24,
                "change": 30.12,
                "change_percent": 0.57,
            },
            {
                "name": "NASDAQ",
                "value": 18200.75,
                "change": 50.45,
                "change_percent": 0.28,
            },
            {
                "name": "Dow Jones",
                "value": 38900.18,
                "change": 45.32,
                "change_percent": 0.12,
            },
        ],
        "sectors": [
            {"name": "Technology", "change_percent": 0.85},
            {"name": "Healthcare", "change_percent": 0.52},
            {"name": "Finance", "change_percent": 0.37},
            {"name": "Energy", "change_percent": -0.21},
            {"name": "Consumer", "change_percent": 0.43},
        ],
        "economic_indicators": [
            {"name": "GDP Growth", "value": 3.2, "previous": 2.8},
            {"name": "Inflation Rate", "value": 2.5, "previous": 2.7},
            {"name": "Unemployment", "value": 3.8, "previous": 4.0},
            {"name": "Interest Rate", "value": 2.0, "previous": 1.75},
        ],
        "market_sentiment": {"bullish": 61, "neutral": 23, "bearish": 16},
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/market_news")
def get_market_news(
    limit: int = Query(5, ge=1, le=50),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    market_news = [
        {
            "id": 1,
            "title": "Fed Signals Potential Rate Cut in Q3",
            "source": "Financial Times",
            "time": "2 hours ago",
            "summary": "Federal Reserve officials hinted at a possible interest rate cut in the third quarter as inflation pressures ease.",
            "sentiment": "neutral",
        },
        {
            "id": 2,
            "title": "Tech Stocks Rally on AI Breakthrough",
            "source": "Wall Street Journal",
            "time": "4 hours ago",
            "summary": "Major technology companies saw significant gains following announcements of new artificial intelligence capabilities.",
            "sentiment": "bullish",
        },
        {
            "id": 3,
            "title": "Global Supply Chain Improvements Boost Manufacturing",
            "source": "Bloomberg",
            "time": "6 hours ago",
            "summary": "Manufacturing indices show improvement as global supply chain disruptions continue to resolve.",
            "sentiment": "bullish",
        },
        {
            "id": 4,
            "title": "Energy Sector Faces Pressure Amid Renewable Push",
            "source": "Reuters",
            "time": "8 hours ago",
            "summary": "Traditional energy companies face challenges as governments worldwide accelerate renewable energy initiatives.",
            "sentiment": "bearish",
        },
        {
            "id": 5,
            "title": "Consumer Spending Remains Strong Despite Inflation",
            "source": "CNBC",
            "time": "10 hours ago",
            "summary": "Retail sales data indicates robust consumer spending despite ongoing inflation concerns.",
            "sentiment": "bullish",
        },
    ]
    return {"count": min(limit, len(market_news)), "data": market_news[:limit]}


@router.get("/sector_performance")
def get_sector_performance(
    period: str = Query("ytd", regex="^(1d|1w|1m|3m|6m|1y|ytd)$"),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    sector_performance = [
        {"name": "Technology", "value": 8.5},
        {"name": "Healthcare", "value": 5.2},
        {"name": "Finance", "value": 3.7},
        {"name": "Energy", "value": -2.1},
        {"name": "Consumer", "value": 4.3},
        {"name": "Utilities", "value": 1.8},
        {"name": "Materials", "value": 2.9},
        {"name": "Real Estate", "value": -1.5},
        {"name": "Industrials", "value": 3.2},
        {"name": "Telecom", "value": 2.5},
    ]
    return {
        "period": period,
        "data": sector_performance,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/transactions/", response_model=List[schemas.Transaction])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    transactions = (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == current_user.id)
        .order_by(models.Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return transactions


@router.post("/transactions/", response_model=schemas.Transaction, status_code=201)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    db_transaction = models.Transaction(
        user_id=current_user.id,
        asset_id=transaction.asset_id,
        portfolio_id=transaction.portfolio_id,
        transaction_type=transaction.transaction_type.value,
        amount=transaction.amount,
        quantity=transaction.quantity,
        price=transaction.price,
        fees=transaction.fees or 0,
        currency=transaction.currency or "USD",
        notes=transaction.notes,
        status="pending",
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

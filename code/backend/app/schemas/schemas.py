from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, field_validator


# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    PORTFOLIO_MANAGER = "portfolio_manager"
    ANALYST = "analyst"
    USER = "user"
    API_USER = "api_user"


class UserTier(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    INSTITUTIONAL = "institutional"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    DIVIDEND = "dividend"
    SPLIT = "split"
    MERGER = "merger"
    TRANSFER = "transfer"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class RiskLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""


class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.USER
    tier: Optional[UserTier] = UserTier.BASIC

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserResponse(UserBase):
    id: int
    role: UserRole
    tier: UserTier
    status: UserStatus
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    tier: Optional[UserTier] = None
    is_active: Optional[bool] = None


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: Optional[int] = None


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: Optional[str]
    email: str
    role: str


# Portfolio schemas
class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None
    risk_level: Optional[RiskLevel] = RiskLevel.MODERATE
    investment_strategy: Optional[str] = None
    base_currency: Optional[str] = "USD"


class PortfolioCreate(PortfolioBase):
    pass


class Portfolio(PortfolioBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# Asset schemas
class AssetBase(BaseModel):
    symbol: str
    name: str
    asset_type: str
    description: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = "USD"
    sector: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class Asset(AssetBase):
    id: int
    current_price: Optional[float] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# Portfolio Asset schemas
class PortfolioAssetBase(BaseModel):
    portfolio_id: int
    asset_id: int
    quantity: float
    purchase_price: float
    purchase_date: Optional[datetime] = None
    target_weight: Optional[float] = None


class PortfolioAssetCreate(PortfolioAssetBase):
    pass


class PortfolioAsset(PortfolioAssetBase):
    id: int
    current_price: Optional[float] = None
    current_value: Optional[float] = None
    unrealized_pnl: Optional[float] = None
    unrealized_pnl_pct: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# Portfolio with assets
class PortfolioWithAssets(Portfolio):
    assets: List[PortfolioAsset] = []


# Asset Price schemas
class AssetPriceBase(BaseModel):
    asset_id: int
    price: float
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    volume: Optional[float] = None


class AssetPriceCreate(AssetPriceBase):
    pass


class AssetPrice(AssetPriceBase):
    id: int
    timestamp: datetime

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# Transaction schemas
class TransactionBase(BaseModel):
    user_id: int
    asset_id: Optional[int] = None
    portfolio_id: Optional[int] = None
    transaction_type: TransactionType
    amount: float
    quantity: Optional[float] = None
    price: Optional[float] = None
    fees: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    status: TransactionStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# AI Model schemas
class AIModelBase(BaseModel):
    name: str
    description: Optional[str] = None
    model_type: str
    accuracy: Optional[float] = None


class AIModelCreate(AIModelBase):
    pass


class AIModel(AIModelBase):
    id: int
    version: str
    is_active: bool
    is_trained: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# AI Prediction schemas
class AIPredictionBase(BaseModel):
    model_id: int
    asset_id: Optional[int] = None
    prediction_type: str
    prediction_value: float
    confidence: float
    target_date: Optional[datetime] = None
    prediction_horizon: Optional[str] = None


class AIPredictionCreate(AIPredictionBase):
    pass


class AIPrediction(AIPredictionBase):
    id: int
    timestamp: datetime

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# Smart Contract schemas
class SmartContractBase(BaseModel):
    address: str
    name: str
    contract_type: str
    network: str
    abi: Optional[Any] = None
    bytecode: Optional[str] = None


class SmartContractCreate(SmartContractBase):
    pass


class SmartContract(SmartContractBase):
    id: int
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# Blockchain Transaction schemas
class BlockchainTransactionBase(BaseModel):
    tx_hash: str
    from_address: str
    to_address: str
    contract_id: Optional[int] = None
    value: float
    gas_used: Optional[int] = None
    status: str
    network: str


class BlockchainTransactionCreate(BlockchainTransactionBase):
    pass


class BlockchainTransaction(BlockchainTransactionBase):
    id: int
    block_number: Optional[int] = None
    confirmations: int
    timestamp: datetime

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# System Log schemas
class SystemLogBase(BaseModel):
    log_level: str
    component: str
    message: str
    request_id: Optional[str] = None
    user_id: Optional[int] = None


class SystemLogCreate(SystemLogBase):
    pass


class SystemLog(SystemLogBase):
    id: int
    timestamp: datetime

    model_config = __import__("pydantic").ConfigDict(from_attributes=True)


# User with portfolios (extended schema)
class UserWithPortfolios(UserResponse):
    portfolios: List[Portfolio] = []


# Pagination schema
class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[Any]

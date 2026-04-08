import enum
import uuid

from sqlalchemy import (
    DECIMAL,
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


# Enums
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    PORTFOLIO_MANAGER = "portfolio_manager"
    ANALYST = "analyst"
    USER = "user"
    API_USER = "api_user"


class UserTier(str, enum.Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    INSTITUTIONAL = "institutional"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class AssetType(str, enum.Enum):
    STOCK = "stock"
    BOND = "bond"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    FOREX = "forex"
    DERIVATIVE = "derivative"
    ETF = "etf"
    MUTUAL_FUND = "mutual_fund"
    REAL_ESTATE = "real_estate"
    ALTERNATIVE = "alternative"


class TransactionType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    DIVIDEND = "dividend"
    SPLIT = "split"
    MERGER = "merger"
    TRANSFER = "transfer"


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class RiskLevel(str, enum.Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class AlertType(str, enum.Enum):
    PRICE_ALERT = "price_alert"
    VOLUME_ALERT = "volume_alert"
    NEWS_ALERT = "news_alert"
    RISK_ALERT = "risk_alert"
    COMPLIANCE_ALERT = "compliance_alert"


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNDER_REVIEW = "under_review"
    EXEMPT = "exempt"


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False, default="")
    last_name = Column(String, nullable=False, default="")
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    tier = Column(Enum(UserTier), default=UserTier.BASIC, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Profile
    phone_number = Column(String)
    date_of_birth = Column(DateTime)
    country = Column(String)
    timezone = Column(String, default="UTC")
    profile_picture_url = Column(String)

    # Security
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String)
    last_login = Column(DateTime)
    last_password_change = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)

    # Compliance
    kyc_verified = Column(Boolean, default=False)
    kyc_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.UNDER_REVIEW)
    kyc_documents = Column(JSON)
    aml_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.UNDER_REVIEW)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    portfolios = relationship(
        "Portfolio", back_populates="owner", cascade="all, delete-orphan"
    )
    transactions = relationship("Transaction", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    api_keys = relationship(
        "APIKey", back_populates="user", cascade="all, delete-orphan"
    )
    login_attempts = relationship("LoginAttempt", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key_hash = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    permissions = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    last_used = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="api_keys")


class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    email = Column(String, nullable=True)
    ip_address = Column(String)
    user_agent = Column(String)
    success = Column(Boolean, default=False)
    failure_reason = Column(String)
    details = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="login_attempts")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_fingerprint = Column(String)
    ip_address = Column(String)
    user_agent = Column(String)
    status = Column(String, default="active")
    risk_score = Column(DECIMAL(5, 4), default=0.0)
    location = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="sessions")


# Portfolio Model
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, default=lambda: str(uuid.uuid4()), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)

    # Portfolio configuration
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.MODERATE)
    investment_strategy = Column(String)
    benchmark = Column(String, default="SPY")
    base_currency = Column(String, default="USD")
    target_allocation = Column(JSON)
    rebalancing_frequency = Column(String, default="quarterly")

    # Portfolio metrics
    total_value = Column(DECIMAL(15, 2), default=0)
    total_cost = Column(DECIMAL(15, 2), default=0)
    total_return = Column(DECIMAL(10, 4))
    total_return_pct = Column(DECIMAL(10, 4))
    daily_change = Column(DECIMAL(15, 2))
    daily_change_pct = Column(DECIMAL(10, 4))

    # Status
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="portfolios")
    assets = relationship(
        "PortfolioAsset", back_populates="portfolio", cascade="all, delete-orphan"
    )
    performance_history = relationship(
        "PortfolioPerformance", back_populates="portfolio", cascade="all, delete-orphan"
    )
    rebalancing_history = relationship(
        "RebalancingEvent", back_populates="portfolio", cascade="all, delete-orphan"
    )


# Asset Model
class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)
    description = Column(Text)

    # Asset details
    exchange = Column(String)
    currency = Column(String, default="USD")
    country = Column(String)
    sector = Column(String)
    industry = Column(String)
    isin = Column(String)
    cusip = Column(String)

    # Current market data
    current_price = Column(DECIMAL(15, 6))
    market_cap = Column(DECIMAL(20, 2))
    volume_24h = Column(DECIMAL(20, 2))
    price_change_24h = Column(DECIMAL(10, 4))
    price_change_7d = Column(DECIMAL(10, 4))

    # Status
    is_active = Column(Boolean, default=True)
    is_tradable = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    portfolio_assets = relationship("PortfolioAsset", back_populates="asset")
    price_history = relationship("AssetPrice", back_populates="asset")
    fundamental_data = relationship("FundamentalData", back_populates="asset")
    news = relationship("NewsItem", back_populates="asset")


class PortfolioAsset(Base):
    __tablename__ = "portfolio_assets"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)

    # Position details
    quantity = Column(DECIMAL(20, 8), nullable=False)
    purchase_price = Column(DECIMAL(15, 6), nullable=False)
    purchase_date = Column(DateTime(timezone=True))
    current_price = Column(DECIMAL(15, 6))
    current_value = Column(DECIMAL(15, 2))
    cost_basis = Column(DECIMAL(15, 2))

    # Returns
    unrealized_pnl = Column(DECIMAL(15, 2))
    unrealized_pnl_pct = Column(DECIMAL(10, 4))
    realized_pnl = Column(DECIMAL(15, 2))

    # Weight in portfolio
    target_weight = Column(DECIMAL(5, 4))
    actual_weight = Column(DECIMAL(5, 4))

    # Risk metrics
    beta = Column(DECIMAL(8, 4))
    volatility = Column(DECIMAL(8, 4))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (UniqueConstraint("portfolio_id", "asset_id"),)

    portfolio = relationship("Portfolio", back_populates="assets")
    asset = relationship("Asset", back_populates="portfolio_assets")


class AssetPrice(Base):
    __tablename__ = "asset_prices"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    price = Column(DECIMAL(15, 6), nullable=False)
    open_price = Column(DECIMAL(15, 6))
    high_price = Column(DECIMAL(15, 6))
    low_price = Column(DECIMAL(15, 6))
    close_price = Column(DECIMAL(15, 6))
    volume = Column(DECIMAL(20, 2))
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (Index("idx_asset_price_timestamp", "asset_id", "timestamp"),)

    asset = relationship("Asset", back_populates="price_history")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))

    # Transaction details
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(DECIMAL(20, 8))
    price = Column(DECIMAL(15, 6))
    amount = Column(DECIMAL(15, 2), nullable=False)
    fees = Column(DECIMAL(15, 6), default=0)
    currency = Column(String, default="USD")

    # Status
    status = Column(
        Enum(TransactionStatus),
        default=TransactionStatus.PENDING,
        nullable=False,
    )
    notes = Column(Text)
    reference_id = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime)

    user = relationship("User", back_populates="transactions")
    asset = relationship("Asset")
    portfolio = relationship("Portfolio")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    alert_type = Column(Enum(AlertType), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text)
    threshold_value = Column(DECIMAL(15, 6))
    current_value = Column(DECIMAL(15, 6))
    is_triggered = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    triggered_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    asset = relationship("Asset")


class PortfolioPerformance(Base):
    __tablename__ = "portfolio_performance"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    total_value = Column(DECIMAL(15, 2))
    daily_return = Column(DECIMAL(10, 6))
    cumulative_return = Column(DECIMAL(10, 6))
    benchmark_return = Column(DECIMAL(10, 6))
    alpha = Column(DECIMAL(10, 6))
    beta = Column(DECIMAL(10, 6))
    sharpe_ratio = Column(DECIMAL(10, 6))
    max_drawdown = Column(DECIMAL(10, 6))
    volatility = Column(DECIMAL(10, 6))

    portfolio = relationship("Portfolio", back_populates="performance_history")


class RebalancingEvent(Base):
    __tablename__ = "rebalancing_events"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    trigger = Column(String)
    old_allocation = Column(JSON)
    new_allocation = Column(JSON)
    trades_executed = Column(JSON)
    total_cost = Column(DECIMAL(15, 2))
    status = Column(String, default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime)

    portfolio = relationship("Portfolio", back_populates="rebalancing_history")


class FundamentalData(Base):
    __tablename__ = "fundamental_data"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    pe_ratio = Column(DECIMAL(10, 4))
    pb_ratio = Column(DECIMAL(10, 4))
    ps_ratio = Column(DECIMAL(10, 4))
    ev_ebitda = Column(DECIMAL(10, 4))
    dividend_yield = Column(DECIMAL(8, 4))
    earnings_per_share = Column(DECIMAL(15, 4))
    revenue = Column(DECIMAL(20, 2))
    net_income = Column(DECIMAL(20, 2))
    total_assets = Column(DECIMAL(20, 2))
    total_debt = Column(DECIMAL(20, 2))
    free_cash_flow = Column(DECIMAL(20, 2))
    return_on_equity = Column(DECIMAL(10, 4))
    return_on_assets = Column(DECIMAL(10, 4))
    debt_to_equity = Column(DECIMAL(10, 4))
    current_ratio = Column(DECIMAL(10, 4))
    gross_margin = Column(DECIMAL(10, 4))
    operating_margin = Column(DECIMAL(10, 4))
    net_margin = Column(DECIMAL(10, 4))
    report_date = Column(DateTime)
    period = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    asset = relationship("Asset", back_populates="fundamental_data")


class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    title = Column(String, nullable=False)
    content = Column(Text)
    url = Column(String)
    source = Column(String)
    author = Column(String)
    sentiment_score = Column(DECIMAL(5, 4))
    sentiment_label = Column(String)
    published_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    asset = relationship("Asset", back_populates="news")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    resource_type = Column(String)
    resource_id = Column(String)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    endpoint = Column(String)
    request_id = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="audit_logs")


# AI and ML Models
class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    model_type = Column(String, nullable=False)
    version = Column(String, default="1.0")
    parameters = Column(JSON)
    hyperparameters = Column(JSON)
    training_data_period = Column(String)
    accuracy = Column(DECIMAL(5, 4))
    precision = Column(DECIMAL(5, 4))
    recall = Column(DECIMAL(5, 4))
    f1_score = Column(DECIMAL(5, 4))
    mse = Column(DECIMAL(15, 8))
    mae = Column(DECIMAL(15, 8))
    is_active = Column(Boolean, default=True)
    is_trained = Column(Boolean, default=False)
    last_trained = Column(DateTime)
    next_training = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    predictions = relationship("AIPrediction", back_populates="model")


class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ai_models.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    prediction_type = Column(String, nullable=False)
    prediction_value = Column(DECIMAL(15, 6))
    confidence = Column(DECIMAL(5, 4))
    probability_distribution = Column(JSON)
    prediction_horizon = Column(String)
    target_date = Column(DateTime(timezone=True))
    actual_value = Column(DECIMAL(15, 6))
    accuracy_score = Column(DECIMAL(5, 4))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    model = relationship("AIModel", back_populates="predictions")
    asset = relationship("Asset")


# Blockchain Models
class SmartContract(Base):
    __tablename__ = "smart_contracts"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    contract_type = Column(String, nullable=False)
    abi = Column(JSON)
    bytecode = Column(Text)
    source_code = Column(Text)
    compiler_version = Column(String)
    network = Column(String, nullable=False)
    chain_id = Column(Integer)
    deployment_tx_hash = Column(String)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    transactions = relationship("BlockchainTransaction", back_populates="contract")


class BlockchainTransaction(Base):
    __tablename__ = "blockchain_transactions"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, unique=True, index=True, nullable=False)
    contract_id = Column(Integer, ForeignKey("smart_contracts.id"))
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    value = Column(DECIMAL(30, 18))
    gas_limit = Column(Integer)
    gas_used = Column(Integer)
    gas_price = Column(DECIMAL(30, 18))
    block_number = Column(BigInteger)
    block_hash = Column(String)
    transaction_index = Column(Integer)
    status = Column(String, nullable=False)
    confirmations = Column(Integer, default=0)
    network = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    block_timestamp = Column(DateTime(timezone=True))

    contract = relationship("SmartContract", back_populates="transactions")


# System and Monitoring Models
class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_level = Column(String, nullable=False, index=True)
    component = Column(String, nullable=False, index=True)
    message = Column(Text, nullable=False)
    request_id = Column(String)
    user_id = Column(Integer)
    session_id = Column(String)
    log_metadata = Column(JSON)
    stack_trace = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index("idx_log_level_timestamp", "log_level", "timestamp"),
        Index("idx_component_timestamp", "component", "timestamp"),
    )


class SystemMetric(Base):
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, nullable=False, index=True)
    metric_value = Column(DECIMAL(15, 6), nullable=False)
    metric_type = Column(String)
    labels = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (Index("idx_metric_name_timestamp", "metric_name", "timestamp"),)

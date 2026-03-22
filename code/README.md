# QuantumNest

## Overview

QuantumNest Capital is a comprehensive financial technology platform designed for institutional and retail investors. This version includes advanced AI capabilities, robust security features, and enterprise-grade financial services suitable for investor presentation and production deployment.

## Key Features

### Financial Services

- **Advanced Trading Engine**: High-performance trading system with real-time market data
- **Portfolio Management**: Sophisticated portfolio optimization and risk management
- **Risk Assessment**: Multi-layered risk analysis and compliance monitoring
- **Market Data Integration**: Real-time and historical market data from multiple sources

### AI & Machine Learning

- **Fraud Detection**: Advanced ML-based fraud detection system
- **Portfolio Optimization**: AI-powered portfolio optimization using modern portfolio theory
- **Predictive Analytics**: LSTM-based price prediction and market forecasting
- **Sentiment Analysis**: News and social media sentiment analysis for market insights
- **Risk Profiling**: AI-driven investor risk profiling and recommendations

### Security & Compliance

- **Multi-Factor Authentication**: Advanced 2FA with TOTP support
- **Role-Based Access Control**: Granular permission system
- **Data Encryption**: End-to-end encryption for sensitive data
- **API Security**: Rate limiting, request signing, and comprehensive security middleware
- **Audit Logging**: Complete audit trail for compliance

### Enterprise Features

- **Scalable Architecture**: Microservices-ready design
- **High Availability**: Redis caching and session management
- **Monitoring & Logging**: Comprehensive logging and health checks
- **Testing Framework**: Extensive unit and integration tests

## 🛠 Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Node.js 18+ (for frontend)

### Backend Setup

1. **Clone and navigate to backend directory**:

   ```bash
   cd code/backend
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file in the backend directory:

   ```env
   # Database
   DATABASE_URL=postgresql://username:password@localhost:5432/quantumnest

   # Redis
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_PASSWORD=

   # Security
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   API_SECRET_KEY=your-api-secret-key-here
   API_KEY=your-api-key-here

   # Features
   ENABLE_REQUEST_SIGNING=true
   ENABLE_IP_FILTERING=false
   ENABLE_CSRF_PROTECTION=true

   # External APIs
   ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
   OPENAI_API_KEY=your-openai-key

   # Allowed Origins
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
   ```

5. **Database Setup**:

   ```bash
   # Create database
   createdb quantumnest

   # Initialize database (using Flask app)
   python -c "from app.main_flask import app; app.app_context().push(); from app.models.models import db; db.create_all()"
   ```

6. **Run the application**:

   ```bash
   # Using Flask (recommended for enhanced features)
   python app/main_flask.py

   # Or using FastAPI (original)
   python app/main.py
   ```

## Testing

Run the comprehensive test suite:

```bash
cd code/backend

# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --syntax    # Syntax checking
python run_tests.py --imports   # Import validation
python run_tests.py --security  # Security checks
python run_tests.py --quality   # Code quality checks
```

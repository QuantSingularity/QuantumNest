"""Flask-SQLAlchemy database instance - kept for Flask app compatibility"""

try:
    from flask_sqlalchemy import SQLAlchemy

    db = SQLAlchemy()
except ImportError:
    db = None

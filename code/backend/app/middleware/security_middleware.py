import ipaddress
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp


@dataclass
class SecurityConfig:
    enable_rate_limiting: bool = True
    enable_request_signing: bool = False
    enable_ip_filtering: bool = False
    enable_cors: bool = True
    enable_csrf_protection: bool = False  # handled by CORS in API-only mode
    max_request_size: int = 10 * 1024 * 1024  # 10 MB
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    allowed_ips: List[str] = field(default_factory=list)
    blocked_ips: List[str] = field(default_factory=list)
    api_secret_key: Optional[str] = None
    trusted_hosts: List[str] = field(default_factory=lambda: ["*"])


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Lightweight security middleware for FastAPI / Starlette.

    Provides:
      - Per-IP rate limiting (sliding window, in-process)
      - Optional IP allowlist / blocklist
      - Request size guard
      - Basic security response headers
    """

    def __init__(self, app: ASGIApp, config: Optional[SecurityConfig] = None) -> None:
        super().__init__(app)
        self.config = config or SecurityConfig()
        # {ip: [timestamp, ...]}
        self._rate_store: Dict[str, List[float]] = {}

    # ── Middleware entry-point ─────────────────────────────────────────────────

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = self._get_client_ip(request)

        # 1. IP filtering
        if self.config.enable_ip_filtering:
            if self._is_blocked(client_ip):
                return JSONResponse({"detail": "Access denied"}, status_code=403)
            if self.config.allowed_ips and not self._is_allowed(client_ip):
                return JSONResponse({"detail": "Access denied"}, status_code=403)

        # 2. Rate limiting
        if self.config.enable_rate_limiting:
            if not self._check_rate_limit(client_ip):
                return JSONResponse(
                    {"detail": "Rate limit exceeded. Try again later."},
                    status_code=429,
                    headers={"Retry-After": str(self.config.rate_limit_window)},
                )

        # 3. Request size guard (skip streaming bodies)
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.config.max_request_size:
            return JSONResponse({"detail": "Request body too large"}, status_code=413)

        # 4. Process request
        try:
            response = await call_next(request)
        except Exception:
            return JSONResponse({"detail": "Internal server error"}, status_code=500)

        # 5. Add security headers
        self._add_security_headers(response)
        return response

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _get_client_ip(self, request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"

    def _check_rate_limit(self, ip: str) -> bool:
        now = time.monotonic()
        window_start = now - self.config.rate_limit_window
        timestamps = self._rate_store.get(ip, [])
        # Prune old timestamps
        timestamps = [t for t in timestamps if t > window_start]
        if len(timestamps) >= self.config.rate_limit_requests:
            self._rate_store[ip] = timestamps
            return False
        timestamps.append(now)
        self._rate_store[ip] = timestamps
        return True

    def _is_blocked(self, ip: str) -> bool:
        for blocked in self.config.blocked_ips:
            try:
                if ipaddress.ip_address(ip) in ipaddress.ip_network(
                    blocked, strict=False
                ):
                    return True
            except ValueError:
                if ip == blocked:
                    return True
        return False

    def _is_allowed(self, ip: str) -> bool:
        for allowed in self.config.allowed_ips:
            try:
                if ipaddress.ip_address(ip) in ipaddress.ip_network(
                    allowed, strict=False
                ):
                    return True
            except ValueError:
                if ip == allowed:
                    return True
        return False

    @staticmethod
    def _add_security_headers(response: Response) -> None:
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

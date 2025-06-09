import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class HealthStatus:
    """Health check status representation."""

    service_name: str
    is_healthy: bool
    response_time_ms: Optional[float]
    error_message: Optional[str]
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None


class HealthCheckService:
    """
    Infrastructure service for HTTP health checks using requests library.
    Provides comprehensive health monitoring for external services.
    """

    def __init__(self, timeout: int = 5):
        """
        Initialize health check service.

        :param timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        # Set default headers for all requests
        self.session.headers.update(
            {
                "User-Agent": "ShopList-HealthCheck/1.0",
                "Accept": "application/json, text/plain, */*",
            }
        )

    def check_http_endpoint(self, url: str, expected_status: int = 200) -> HealthStatus:
        """
        Check HTTP endpoint health.

        :param url: URL to check
        :param expected_status: Expected HTTP status code
        :return: Health status
        """
        service_name = self._extract_service_name(url)
        start_time = datetime.now()

        try:
            response = self.session.get(url, timeout=self.timeout)
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            is_healthy = response.status_code == expected_status
            error_message = None if is_healthy else f"HTTP {response.status_code}"

            details = {
                "status_code": response.status_code,
                "response_size": len(response.content),
                "headers": dict(response.headers),
            }

            # Try to parse JSON response for additional details
            try:
                if response.headers.get("content-type", "").startswith(
                    "application/json"
                ):
                    details["response_data"] = response.json()
            except Exception:
                pass  # Ignore JSON parsing errors

            return HealthStatus(
                service_name=service_name,
                is_healthy=is_healthy,
                response_time_ms=response_time,
                error_message=error_message,
                timestamp=end_time,
                details=details,
            )

        except requests.exceptions.Timeout:
            return HealthStatus(
                service_name=service_name,
                is_healthy=False,
                response_time_ms=None,
                error_message=f"Timeout after {self.timeout}s",
                timestamp=datetime.now(),
            )
        except requests.exceptions.ConnectionError as e:
            return HealthStatus(
                service_name=service_name,
                is_healthy=False,
                response_time_ms=None,
                error_message=f"Connection error: {str(e)}",
                timestamp=datetime.now(),
            )
        except requests.exceptions.RequestException as e:
            return HealthStatus(
                service_name=service_name,
                is_healthy=False,
                response_time_ms=None,
                error_message=f"Request error: {str(e)}",
                timestamp=datetime.now(),
            )

    def check_api_endpoint(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> HealthStatus:
        """
        Check API endpoint with custom method and payload.

        :param url: API endpoint URL
        :param method: HTTP method (GET, POST, PUT, etc.)
        :param headers: Additional headers
        :param payload: Request payload for POST/PUT requests
        :return: Health status
        """
        service_name = self._extract_service_name(url)
        start_time = datetime.now()

        try:
            # Prepare request arguments with proper typing
            if payload and method.upper() in ["POST", "PUT", "PATCH"]:
                response = self.session.request(
                    method.upper(),
                    url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout,
                )
            else:
                response = self.session.request(
                    method.upper(), url, headers=headers, timeout=self.timeout
                )
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            is_healthy = 200 <= response.status_code < 300
            error_message = None if is_healthy else f"HTTP {response.status_code}"

            details = {
                "method": method.upper(),
                "status_code": response.status_code,
                "response_size": len(response.content),
            }

            return HealthStatus(
                service_name=service_name,
                is_healthy=is_healthy,
                response_time_ms=response_time,
                error_message=error_message,
                timestamp=end_time,
                details=details,
            )

        except Exception as e:
            return HealthStatus(
                service_name=service_name,
                is_healthy=False,
                response_time_ms=None,
                error_message=f"Error: {str(e)}",
                timestamp=datetime.now(),
            )

    def check_multiple_endpoints(
        self, endpoints: Dict[str, str]
    ) -> Dict[str, HealthStatus]:
        """
        Check multiple endpoints concurrently.

        :param endpoints: Dictionary of service_name -> url
        :return: Dictionary of service_name -> health_status
        """
        results = {}
        for service_name, url in endpoints.items():
            status = self.check_http_endpoint(url)
            status.service_name = service_name  # Override with custom name
            results[service_name] = status
        return results

    def _extract_service_name(self, url: str) -> str:
        """Extract service name from URL."""
        try:
            from urllib.parse import urlparse

            parsed = urlparse(url)
            return f"{parsed.netloc}{parsed.path}"
        except Exception:
            return url

    def close(self):
        """Close the requests session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

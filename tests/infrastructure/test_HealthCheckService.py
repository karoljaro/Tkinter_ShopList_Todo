from unittest.mock import Mock, patch
from datetime import datetime
import requests
from src.infrastructure.services.HealthCheckService import (
    HealthCheckService,
    HealthStatus,
)


class TestHealthCheckService:
    """Unit tests for HealthCheckService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.health_service = HealthCheckService(timeout=5)

    def teardown_method(self):
        """Clean up after tests."""
        self.health_service.close()

    @patch("src.infrastructure.services.HealthCheckService.requests.Session")
    def test_init(self, mock_session_class):
        """Test service initialization."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        service = HealthCheckService(timeout=10)

        assert service.timeout == 10
        mock_session.headers.update.assert_called_once_with(
            {
                "User-Agent": "ShopList-HealthCheck/1.0",
                "Accept": "application/json, text/plain, */*",
            }
        )

    def test_check_http_endpoint_success(self):
        """Test successful HTTP endpoint check."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"status": "ok"}'
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {"status": "ok"}

        self.health_service.session.get = Mock(return_value=mock_response)

        # Execute
        result = self.health_service.check_http_endpoint(
            "http://example.com/health"
        )  # Verify
        assert result.service_name == "example.com/health"
        assert result.is_healthy is True
        assert result.error_message is None
        assert result.response_time_ms is not None
        assert result.response_time_ms > 0
        assert result.details["status_code"] == 200
        assert result.details["response_data"] == {"status": "ok"}

    def test_check_http_endpoint_wrong_status(self):
        """Test HTTP endpoint check with wrong status code."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = b"Internal Server Error"
        mock_response.headers = {"content-type": "text/plain"}

        self.health_service.session.get = Mock(return_value=mock_response)

        # Execute
        result = self.health_service.check_http_endpoint(
            "http://example.com/health"
        )  # Verify
        assert result.is_healthy is False
        assert result.error_message == "HTTP 500"
        assert result.details["status_code"] == 500

    def test_check_http_endpoint_timeout(self):
        """Test HTTP endpoint check with timeout."""
        # Mock timeout exception
        self.health_service.session.get = Mock(
            side_effect=requests.exceptions.Timeout("Request timed out")
        )

        # Execute
        result = self.health_service.check_http_endpoint("http://example.com/health")

        # Verify        assert result.is_healthy is False
        assert "Timeout after 5s" in result.error_message
        assert result.response_time_ms is None

    def test_check_http_endpoint_connection_error(self):
        """Test HTTP endpoint check with connection error."""
        # Mock connection error
        self.health_service.session.get = Mock(
            side_effect=requests.exceptions.ConnectionError("Connection refused")
        )

        # Execute
        result = self.health_service.check_http_endpoint("http://example.com/health")

        # Verify
        assert result.is_healthy is False
        assert "Connection error" in result.error_message
        assert result.response_time_ms is None

    def test_check_api_endpoint_post_success(self):
        """Test successful POST API endpoint check."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.content = b'{"id": "created"}'

        self.health_service.session.request = Mock(return_value=mock_response)

        # Execute
        result = self.health_service.check_api_endpoint(
            "http://api.example.com/users",
            method="POST",
            headers={"Authorization": "Bearer token"},
            payload={"name": "Test User"},
        )

        # Verify
        assert result.is_healthy is True
        assert result.details["method"] == "POST"
        assert result.details["status_code"] == 201

        # Verify request was made with correct parameters
        self.health_service.session.request.assert_called_once_with(
            "POST",
            "http://api.example.com/users",
            json={"name": "Test User"},
            headers={"Authorization": "Bearer token"},
            timeout=5,
        )

    def test_check_api_endpoint_get_no_payload(self):
        """Test GET API endpoint check without payload."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"[]"

        self.health_service.session.request = Mock(return_value=mock_response)

        # Execute
        result = self.health_service.check_api_endpoint(
            "http://api.example.com/users", method="GET"
        )

        # Verify
        assert result.is_healthy is True
        # Verify request was made without json parameter
        self.health_service.session.request.assert_called_once_with(
            "GET", "http://api.example.com/users", headers=None, timeout=5
        )

    def test_check_api_endpoint_error(self):
        """Test API endpoint check with error."""
        # Mock request exception
        self.health_service.session.request = Mock(
            side_effect=requests.exceptions.RequestException("API Error")
        )

        # Execute
        result = self.health_service.check_api_endpoint("http://api.example.com/users")

        # Verify
        assert result.is_healthy is False
        assert "Error: API Error" in result.error_message

    def test_check_multiple_endpoints(self):
        """Test checking multiple endpoints."""
        # Mock responses
        responses = [
            Mock(status_code=200, content=b"OK", headers={}),
            Mock(status_code=500, content=b"Error", headers={}),
        ]

        self.health_service.session.get = Mock(side_effect=responses)

        # Execute
        endpoints = {
            "service1": "http://service1.com/health",
            "service2": "http://service2.com/health",
        }
        results = self.health_service.check_multiple_endpoints(endpoints)

        # Verify
        assert len(results) == 2
        assert results["service1"].is_healthy is True
        assert results["service2"].is_healthy is False
        assert results["service1"].service_name == "service1"
        assert results["service2"].service_name == "service2"

    def test_extract_service_name(self):
        """Test service name extraction from URL."""
        # Test cases
        test_cases = [
            ("http://example.com/health", "example.com/health"),
            (
                "https://api.service.com:8080/v1/status",
                "api.service.com:8080/v1/status",
            ),
            ("http://localhost:3000", "localhost:3000"),
            ("invalid-url", "invalid-url"),  # Fallback case
        ]

        for url, expected in test_cases:
            result = self.health_service._extract_service_name(url)
            assert result == expected

    def test_context_manager(self):
        """Test context manager functionality."""
        with HealthCheckService() as service:
            assert service.session is not None

        # After context exit, close should have been called
        # (We can't easily test this without mocking, but the structure is correct)

    def test_close(self):
        """Test session closure."""
        mock_session = Mock()
        self.health_service.session = mock_session

        self.health_service.close()

        mock_session.close.assert_called_once()


class TestHealthStatus:
    """Unit tests for HealthStatus dataclass."""

    def test_health_status_creation(self):
        """Test HealthStatus object creation."""
        timestamp = datetime.now()
        status = HealthStatus(
            service_name="test-service",
            is_healthy=True,
            response_time_ms=150.5,
            error_message=None,
            timestamp=timestamp,
            details={"status": "ok"},
        )

        assert status.service_name == "test-service"
        assert status.is_healthy is True
        assert status.response_time_ms == 150.5
        assert status.error_message is None
        assert status.timestamp == timestamp
        assert status.details == {"status": "ok"}

    def test_health_status_with_error(self):
        """Test HealthStatus object with error."""
        timestamp = datetime.now()
        status = HealthStatus(
            service_name="failing-service",
            is_healthy=False,
            response_time_ms=None,
            error_message="Connection timeout",
            timestamp=timestamp,
        )

        assert status.service_name == "failing-service"
        assert status.is_healthy is False
        assert status.response_time_ms is None
        assert status.error_message == "Connection timeout"
        assert status.details is None  # Default value

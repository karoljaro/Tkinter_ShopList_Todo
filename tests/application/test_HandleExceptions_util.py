import pytest
from src.application.utils.errorHandlerDecorator import handle_exceptions

@handle_exceptions
def function_that_raises():
    raise ValueError("Test error")

def test_handle_exceptions():
    with pytest.raises(ValueError, match="Test error"):
        function_that_raises()
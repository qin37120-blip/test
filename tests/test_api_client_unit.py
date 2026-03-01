from unittest.mock import Mock

from utils.http_client import APIClient


def test_api_client_should_call_session_request_with_expected_arguments() -> None:
    mock_session = Mock()
    mock_response = Mock(status_code=200)
    mock_session.request.return_value = mock_response

    client = APIClient(base_url="https://example.com", timeout=5, session=mock_session)
    response = client.get("/users", params={"page": 1})

    assert response is mock_response
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://example.com/users",
        headers=None,
        timeout=5,
        params={"page": 1},
    )

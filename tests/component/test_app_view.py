import pytest
import requests

HOST = 'localhost'
PORT = 8000
PATH = 'api/'


class TestAppView:

    @pytest.fixture
    def url(self):
        return f'http://{HOST}:{PORT}/{PATH}'

    def test_get(self, url):
        response = requests.get(url)
        actual_response_message = response.text

        expect_response_message = 'Your Application is up and running!'

        assert actual_response_message == expect_response_message, 'Result was not as expected'

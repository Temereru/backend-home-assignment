from pytest import fixture

from notraffic.app.views.app_view import AppView


class TestAppView:
    @fixture
    def view(self):
        yield AppView()

    def test_get(self, view):
        actual_response = view.get(None)
        actual_response_message = actual_response.content.decode("utf-8")
        expect_response_message = 'Your Application is up and running!'

        assert actual_response_message == expect_response_message, 'Result was not as expected'

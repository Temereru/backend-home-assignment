import pytest
import requests
import json

HOST = 'localhost'
PORT = 8000
PATH = 'api/zone'


class TestZonesView:

    @pytest.fixture
    def url(self):
        return f'http://{HOST}:{PORT}/{PATH}'

    # @pytest.fixture
    # def csrf(self):
    #     response = requests.post(f'http://{HOST}:{PORT}/admin')
    #     print(f'csrf: {response.headers.get("Set-Cookie")}, {response.cookies}')
    #     return response.headers.get('Set-Cookie')

    def test_delete_zones(self, url):
        response = requests.delete(url)

        assert response.status_code == 200, 'Result was not as expected'

    def test_post_single_zone(self, url):
        response = requests.post(url, json={'xmin': 1, 'xmax': 3, 'ymin': 2, 'ymax': 4, 'name': 'First'})

        json_response = response.json()

        assert json_response.xmin == 1, 'xmin result was not as expected'
        assert json_response.xmax == 3, 'xmax result was not as expected'
        assert json_response.ymin == 2, 'ymin result was not as expected'
        assert json_response.ymax == 4, 'ymax result was not as expected'
        assert json_response.name == 'First', 'name result was not as expected'

    def test_get_zones(self, url):
        response = requests.get(url)
        json_response = response.json()

        assert isinstance(json_response, list)
        assert json_response[0].xmin == 1, 'xmin result was not as expected'
        assert json_response[0].xmax == 3, 'xmax result was not as expected'
        assert json_response[0].ymin == 2, 'ymin result was not as expected'
        assert json_response[0].ymax == 4, 'ymax result was not as expected'
        assert json_response[0].name == 'First', 'name result was not as expected'

    def test_get_specific_zone(self, url):
        assert False

    def test_get_specific_zones(self, url):
        assert False

    def test_get_wrong_zone(self):
        assert False

    def test_get_wrong_zone_in_list(self):
        assert False

    def test_update_zones(self, url):
        '''
        This test should verify the update zones API
        '''
        response = requests.put(url, json={"test": 3})
        actual_response_message = response.text

        expect_response_message = 'Your Application is up and running!'

        assert actual_response_message == expect_response_message, 'Result was not as expected'

    def test_update_specific_zone(self, url):
        assert False

    def test_update_wrong_zone(self, url):
        assert False

    def test_update_wrong_zone_in_list(self, url):
        assert False

    def test_update_wrong_xmin_type(self, url):
        assert False

    def test_update_wrong_ymin_type(self, url):
        assert False

    def test_update_wrong_xmax_type(self, url):
        assert False

    def test_update_wrong_ymax_type(self, url):
        assert False

    def test_update_xmin_larger_than_xmax(self, url):
        assert False

    def test_update_ymin_larger_than_ymax(self, url):
        assert False

    def test_update_name_not_string(self, url):
        assert False

    def test_delete_specific_zone(self, url):
        assert False

    def test_delete_wrong_zone(self, url):
        assert False

    def test_delete_wrong_zone_in_list(self, url):
        assert False

    def test_post_zones(self, url):
        '''
        This test should verify the post zones API
        '''
        response = requests.post(url, json={"test": 4})
        actual_response_message = response.text

        expect_response_message = 'Your Application is up and running!'

        assert actual_response_message == actual_response_message, 'Result was not as expected'

    def test_post_wrong_xmin_type(self, url):
        assert False

    def test_post_wrong_ymin_type(self, url):
        assert False

    def test_post_wrong_xmax_type(self, url):
        assert False

    def test_post_wrong_ymax_type(self, url):
        assert False

    def test_post_xmin_larger_than_xmax(self, url):
        assert False

    def test_post_ymin_larger_than_ymax(self, url):
        assert False

    def test_post_name_not_string(self, url):
        assert False

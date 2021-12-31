import pytest
import requests
import json

HOST = 'localhost'
PORT = 8000
PATH = 'api/zone'

key_errors = 'errors'
key_data = 'data'
key_id = 'id'
key_name = 'name'
key_min_x = 'min_x'
key_min_y = 'min_y'
key_max_x = 'max_x'
key_max_y = 'max_y'

assertion_error_expected_to_contain = 'Expected {0}} to contain the key "{1}", it did not'
assertion_error_key_incorrect_type = 'Expected response "{0}" key to contain a {1}, instead it contains a {2}'
assertion_error_list_not_empty = 'Expected response "{0}" to be an empty list'
assertion_error_list_empty = 'Expected response "{0}" to be a non empty list'
assertion_error_list_incorrect_length = 'Expected response "{0}" to be a non empty list of length {1}, instead it\'s length is {2}'
assertion_value_not_matching = 'Expected value of {0} to match {1}, instead it was {2}'
assertion_value_not_none = 'Expected {0} to be None, instead it was {1}'
assertion_got_wrong_error = 'Error not as Expected'
assertion_ids_not_matching = 'updated zone id: {0} not matching expected id: {1}'
assertion_wrong_response_status = 'Expected response status to be {0} instead got {1}'

validation_error_is_required = '{0} is required'
validation_error_empty_string = '{0} needs to be a non empty string at max length of {1}'
validation_error_wrong_int = '{0} needs to be an integer larger or equal to 0'
validation_error_need_to_be_larger = '{0} needs to be larger than {1}'

api_error_validation_error_for = 'validation error for zone with {0} {1}: {2}'
api_error_not_found = 'item with id: {0} was not found'
api_error_illegal_post_body = 'body needs to be a full zone object'
api_error_illegal_put_body = 'body needs to be a zone updates dictionary, or a list of zone updates dictionaries'
api_error_zone_not_found = 'Zone not found for id: {0}'
api_error_illegal_query_ids = 'ids must be a string of comma separated integers'
api_error_delete_unknown = 'must specify items to delete'


class TestZonesView:

    @pytest.fixture
    def url(self):
        return f'http://{HOST}:{PORT}/{PATH}/'

    @pytest.fixture
    def zone_1(self):
        return {key_name: 'zone_1', key_min_x: 0, key_min_y: 1, key_max_x: 2, key_max_y: 3}

    @pytest.fixture
    def zone_2(self):
        return {key_name: 'zone_2', key_min_x: 4, key_min_y: 5, key_max_x: 6, key_max_y: 7}

    @pytest.fixture
    def zone_3(self):
        return {key_name: 'zone_3', key_min_x: 8, key_min_y: 9, key_max_x: 10, key_max_y: 11}

    @pytest.fixture
    def zone_4(self):
        return {key_name: 'zone_4', key_min_x: 12, key_min_y: 13, key_max_x: 14, key_max_y: 15}

    @pytest.fixture
    def clear_db(self, url):
        requests.delete(f'{url}?all=deleteAll')

    @pytest.fixture
    def setup_create(self, clear_db):
        return 'ready'

    @pytest.fixture
    def setup_single(self, clear_db, url, zone_1):
        response = requests.post(url, json=zone_1)
        return response.json()

    @pytest.fixture
    def setup_multiple(self, clear_db, url, zone_1, zone_2, zone_3):
        response = requests.post(url, json=[zone_1, zone_2, zone_3])
        return response.json()

    def general_assertions(self, response_json, should_have_no_errors=True):
        assert key_errors in response_json, assertion_error_expected_to_contain.format('response_body', key_errors)
        errors = response_json[key_errors]
        assert isinstance(errors, list), assertion_error_key_incorrect_type.format(key_errors, 'list', type(errors))
        if should_have_no_errors:
            assert len(errors) == 0, assertion_error_list_not_empty.format(key_errors)

        assert key_data in response_json, assertion_error_expected_to_contain.format('response_body', key_data)
        data = response_json[key_data]

        return errors, data

    def zone_equality_assertion(self, original_key, zone_to_check, correct_zone, including_id=False):
        assert key_id in zone_to_check, assertion_error_expected_to_contain.format(original_key, key_id)

        assert key_name in zone_to_check, assertion_error_expected_to_contain.format(original_key, key_name)
        assert zone_to_check[key_name] == correct_zone[key_name], \
            assertion_value_not_matching.format(key_name, correct_zone[key_name], zone_to_check[key_name])

        assert key_min_x in zone_to_check, assertion_error_expected_to_contain.format(original_key, key_min_x)
        assert zone_to_check[key_min_x] == correct_zone[key_min_x], \
            assertion_value_not_matching.format(key_min_x, correct_zone[key_min_x], zone_to_check[key_min_x])

        assert key_min_y in zone_to_check, assertion_error_expected_to_contain.format(original_key, key_min_y)
        assert zone_to_check[key_min_y] == correct_zone[key_min_y], \
            assertion_value_not_matching.format(key_min_y, correct_zone[key_min_y], zone_to_check[key_min_y])

        assert key_max_x in zone_to_check, assertion_error_expected_to_contain.format(original_key, key_max_x)
        assert zone_to_check[key_max_x] == correct_zone[key_max_x], \
            assertion_value_not_matching.format(key_max_x, correct_zone[key_max_x], zone_to_check[key_max_x])

        assert key_max_y in zone_to_check, assertion_error_expected_to_contain.format(original_key, key_max_y)
        assert zone_to_check[key_max_y] == correct_zone[key_max_y], \
            assertion_value_not_matching.format(key_max_y, correct_zone[key_max_y], zone_to_check[key_max_y])

        if including_id:
            assert zone_to_check[key_id] == correct_zone[key_id], \
                assertion_value_not_matching.format(key_id, correct_zone[key_id], zone_to_check[key_id])

    # create tests

    def test_post_zone(self, setup_create, url, zone_1):
        response = requests.post(url, json=zone_1)
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert isinstance(data, dict), assertion_error_key_incorrect_type.format(key_data, 'dict', type(data))
        self.zone_equality_assertion(key_data, data, zone_1)

    def test_post_zones(self, setup_create, url, zone_1, zone_2, zone_3):
        zones = [zone_1, zone_2, zone_3]
        response = requests.post(url, json=zones)
        response_json = response.json()

        errors, data = self.general_assertions(response_json)
        assert isinstance(data, list), assertion_error_key_incorrect_type.format(key_data, 'list', type(data))
        assert len(data) > 0, assertion_error_list_empty.format(key_data)
        for idx, zone in enumerate(data):
            self.zone_equality_assertion(f'{key_data}[{idx}]', zone, zones[idx])

    def test_post_wrong_min_x_type(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone[key_min_x] = ''
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_wrong_int.format(key_min_x), assertion_got_wrong_error

    def test_post_wrong_min_y_type(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone[key_min_y] = ''
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_wrong_int.format(key_min_y), assertion_got_wrong_error

    def test_post_wrong_max_x_type(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone[key_max_x] = ''
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_wrong_int.format(key_max_x), assertion_got_wrong_error

    def test_post_wrong_max_y_type(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone[key_max_y] = ''
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_wrong_int.format(key_max_y), assertion_got_wrong_error

    def test_post_x_min_larger_than_x_max(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone[key_min_x] = zone_1[key_max_x] + 1
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_need_to_be_larger.format(key_max_x, key_min_x), assertion_got_wrong_error

    def test_post_y_min_larger_than_y_max(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone[key_min_y] = zone_1[key_max_y] + 1
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_need_to_be_larger.format(key_max_y, key_min_y), assertion_got_wrong_error

    def test_post_name_not_string(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone[key_name] = 1
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_empty_string.format(key_name, 1000), assertion_got_wrong_error

    def test_post_name_missing(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone.pop(key_name, None)
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_is_required.format(key_name), assertion_got_wrong_error

    def test_post_min_x_missing(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone.pop(key_min_x, None)
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_is_required.format(key_min_x), assertion_got_wrong_error

    def test_post_min_y_missing(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone.pop(key_min_y, None)
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_is_required.format(key_min_y), assertion_got_wrong_error

    def test_post_max_x_missing(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone.pop(key_max_x, None)
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_is_required.format(key_max_x), assertion_got_wrong_error

    def test_post_max_y_missing(self, setup_create, url, zone_1):
        incorrect_zone = zone_1
        incorrect_zone.pop(key_max_y, None)
        response = requests.post(url, json=incorrect_zone)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_is_required.format(key_max_y), assertion_got_wrong_error

    # update tests

    def test_update_specific_zone(self, setup_single, url, zone_2):
        zone_to_update = setup_single[key_data]
        zone_to_update[key_name] = zone_2[key_name]
        zone_to_update[key_min_x] = zone_2[key_min_x]
        zone_to_update[key_min_y] = zone_2[key_min_y]
        zone_to_update[key_max_x] = zone_2[key_max_x]
        zone_to_update[key_max_y] = zone_2[key_max_y]

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert isinstance(data, dict), assertion_error_key_incorrect_type.format(key_data, 'dict', type(data))
        assert data[key_id] == setup_single[key_data][key_id]
        self.zone_equality_assertion(key_data, data, zone_2)

    def test_update_multiple_zones(self, setup_multiple, url, zone_3, zone_4):
        zones_to_update = setup_multiple[key_data]
        zones_to_update[0][key_name] = zone_3[key_name]
        zones_to_update[0][key_min_x] = zone_3[key_min_x]
        zones_to_update[0][key_min_y] = zone_3[key_min_y]
        zones_to_update[0][key_max_x] = zone_3[key_max_x]
        zones_to_update[0][key_max_y] = zone_3[key_max_y]
        zones_to_update[1][key_name] = zone_4[key_name]
        zones_to_update[1][key_min_x] = zone_4[key_min_x]
        zones_to_update[1][key_min_y] = zone_4[key_min_y]
        zones_to_update[1][key_max_x] = zone_4[key_max_x]
        zones_to_update[1][key_max_y] = zone_4[key_max_y]
        zones_to_update.pop(2)

        response = requests.put(url, json=zones_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert isinstance(data, list), assertion_error_key_incorrect_type.format(key_data, 'list', type(data))
        assert len(data) == 2, assertion_error_list_incorrect_length.format(key_data, 2, len(data))
        assert data[0][key_id] == setup_multiple[key_data][0][key_id], \
            assertion_ids_not_matching.format(data[0][key_id], setup_multiple[key_data][0][key_id])
        self.zone_equality_assertion(key_data, data[0], zone_3)
        assert data[1][key_id] == setup_multiple[key_data][1][key_id], \
            assertion_ids_not_matching.format(data[1][key_id], setup_multiple[key_data][1][key_id])
        self.zone_equality_assertion(key_data, data[1], zone_4)

    def test_update_wrong_zone(self, setup_single, url):
        zone_to_update = setup_single[key_data]
        wrong_id = zone_to_update[key_id] + 1
        zone_to_update[key_id] = wrong_id

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == api_error_zone_not_found.format(wrong_id), assertion_got_wrong_error

    def test_update_wrong_zone_in_list(self, setup_multiple, url, zone_3, zone_4):
        zones_to_update = setup_multiple[key_data]
        zones_to_update[0][key_name] = zone_3[key_name]
        zones_to_update[0][key_min_x] = zone_3[key_min_x]
        zones_to_update[0][key_min_y] = zone_3[key_min_y]
        zones_to_update[0][key_max_x] = zone_3[key_max_x]
        zones_to_update[0][key_max_y] = zone_3[key_max_y]
        zones_to_update[1][key_id] = -1
        zones_to_update[2][key_name] = zone_4[key_name]
        zones_to_update[2][key_min_x] = zone_4[key_min_x]
        zones_to_update[2][key_min_y] = zone_4[key_min_y]
        zones_to_update[2][key_max_x] = zone_4[key_max_x]
        zones_to_update[2][key_max_y] = zone_4[key_max_y]

        response = requests.put(url, json=zones_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert isinstance(data, list), assertion_error_key_incorrect_type.format(key_data, 'list', type(data))
        assert len(data) == 2, assertion_error_list_incorrect_length.format(key_data, 2, len(data))
        assert data[0][key_id] == setup_multiple[key_data][0][key_id], \
            assertion_ids_not_matching.format(data[0][key_id], setup_multiple[key_data][0][key_id])
        self.zone_equality_assertion(key_data, data[0], zone_3)
        assert data[1][key_id] == setup_multiple[key_data][2][key_id], \
            assertion_ids_not_matching.format(data[1][key_id], setup_multiple[key_data][2][key_id])
        self.zone_equality_assertion(key_data, data[1], zone_4)
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == api_error_zone_not_found.format(-1), assertion_got_wrong_error

    def test_update_wrong_min_x_type(self, setup_single, url):
        zone_to_update = setup_single[key_data]
        zone_to_update[key_min_x] = ''

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_wrong_int.format(key_min_x), assertion_got_wrong_error

    def test_update_wrong_min_y_type(self, setup_single, url):
        zone_to_update = setup_single[key_data]
        zone_to_update[key_min_y] = ''

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_wrong_int.format(key_min_y), assertion_got_wrong_error

    def test_update_wrong_max_x_type(self, setup_single, url):
        zone_to_update = setup_single[key_data]
        zone_to_update[key_max_y] = ''

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_wrong_int.format(key_max_y), assertion_got_wrong_error

    def test_update_wrong_max_y_type(self, setup_single, url):
        zone_to_update = setup_single[key_data]
        zone_to_update[key_max_y] = ''

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_wrong_int.format(key_max_y), assertion_got_wrong_error

    def test_update_min_x_larger_than_max_x(self, setup_single, url):
        zone_to_update = setup_single[key_data]
        zone_to_update[key_min_x] = 10
        zone_to_update[key_max_x] = 1

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_need_to_be_larger.format(key_max_x, key_min_x), assertion_got_wrong_error

    def test_update_min_y_larger_than_max_y(self, setup_single, url):
        zone_to_update = setup_single[key_data]
        zone_to_update[key_min_y] = 10
        zone_to_update[key_max_y] = 1

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_need_to_be_larger.format(key_max_y, key_min_y), assertion_got_wrong_error

    def test_update_name_not_string(self, setup_single, url):
        zone_to_update = setup_single[key_data]
        zone_to_update[key_name] = 1

        response = requests.put(url, json=zone_to_update)
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == validation_error_empty_string.format(key_name, 1000), assertion_got_wrong_error

    # get tests

    def test_get_zones(self, setup_multiple, url):
        zones_to_test = setup_multiple[key_data]

        response = requests.get(url)
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert isinstance(data, list), assertion_error_key_incorrect_type.format(key_data, 'list', type(data))
        assert len(data) == len(zones_to_test), assertion_error_list_incorrect_length.format(key_data,
                                                                                             len(zones_to_test),
                                                                                             len(data))
        for idx, zone in enumerate(zones_to_test):
            self.zone_equality_assertion(f'{key_data}[{idx}]', zone, zones_to_test[idx], True)

    def test_get_specific_zone(self, setup_multiple, url):
        zones_to_test = setup_multiple[key_data]

        response = requests.get(f'{url}?ids={zones_to_test[1][key_id]}')
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert isinstance(data, dict), assertion_error_key_incorrect_type.format(key_data, 'dict', type(data))
        self.zone_equality_assertion(key_data, data, zones_to_test[1], True)

    def test_get_specific_zones(self, setup_multiple, url):
        zones_to_test = setup_multiple[key_data]

        response = requests.get(f'{url}?ids={zones_to_test[1][key_id]},{zones_to_test[2][key_id]}')
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert isinstance(data, list), assertion_error_key_incorrect_type.format(key_data, 'list', type(data))
        assert len(data) == 2, assertion_error_list_incorrect_length.format(key_data, 2, len(data))
        self.zone_equality_assertion(key_data, data[0], zones_to_test[1], True)
        self.zone_equality_assertion(key_data, data[1], zones_to_test[2], True)

    def test_get_wrong_zone(self, setup_single, url):
        zone_to_test = setup_single[key_data]
        wrong_id = zone_to_test[key_id] + 1
        response = requests.get(f'{url}?ids={wrong_id}')
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == api_error_not_found.format(wrong_id), assertion_got_wrong_error

    def test_get_wrong_zone_in_list(self, setup_multiple, url):
        zones_to_test = setup_multiple[key_data]
        wrong_id = zones_to_test[2][key_id] + 1
        query = f'?ids={zones_to_test[0][key_id]},{zones_to_test[1][key_id]},{wrong_id}'
        response = requests.get(f'{url}{query}')
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert isinstance(data, list), assertion_error_key_incorrect_type.format(key_data, 'list', type(data))
        assert len(data) == 2, assertion_error_list_incorrect_length.format(key_data, 2, len(data))
        self.zone_equality_assertion(key_data, data[0], zones_to_test[0], True)
        self.zone_equality_assertion(key_data, data[1], zones_to_test[1], True)

    # delete tests

    def test_delete_zones(self, setup_multiple, url):
        zones_to_test = setup_multiple[key_data]

        response = requests.delete(f'{url}?ids={zones_to_test[0][key_id]},{zones_to_test[2][key_id]}')
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert response.status_code == 200, assertion_wrong_response_status.format(200, response.status_code)

        get_response = requests.get(url)
        get_response_json = get_response.json()

        get_errors, get_data = self.general_assertions(get_response_json)

        assert isinstance(get_data, list), assertion_error_key_incorrect_type.format(key_data, 'list', type(get_data))
        assert len(get_data) == 1, assertion_error_list_incorrect_length.format(key_data, 1, len(errors))
        self.zone_equality_assertion(f'{key_data}[0]', get_data[0], zones_to_test[1], True)

    def test_delete_specific_zone(self, setup_single, url):
        zone_to_delete = setup_single[key_data]
        response = requests.delete(f'{url}?ids={zone_to_delete[key_id]}')
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert response.status_code == 200, assertion_wrong_response_status.format(200, response.status_code)

        get_response = requests.get(f'{url}?ids={zone_to_delete[key_id]}')
        get_response_json = get_response.json()

        get_errors, get_data = self.general_assertions(get_response_json, False)

        assert get_data is None, assertion_value_not_none.format(key_data, type(get_data))
        assert len(get_errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(get_errors))
        assert get_errors[0] == api_error_not_found.format(zone_to_delete[key_id]), assertion_got_wrong_error

    def test_delete_wrong_zone(self, setup_single, url):
        zone_to_delete = setup_single[key_data]
        wrong_id = zone_to_delete[key_id] + 1

        response = requests.delete(f'{url}?ids={wrong_id}')
        response_json = response.json()

        errors, data = self.general_assertions(response_json, False)

        assert data is None, assertion_value_not_none.format(key_data, type(data))
        assert len(errors) == 1, assertion_error_list_incorrect_length.format(key_errors, 1, len(errors))
        assert errors[0] == api_error_not_found.format(wrong_id), assertion_got_wrong_error

    def test_delete_wrong_zone_in_list(self, setup_multiple, url):
        zones_to_test = setup_multiple[key_data]

        wrong_id = zones_to_test[2][key_id] + 1

        response = requests.delete(f'{url}?ids={zones_to_test[0][key_id]},{wrong_id},{zones_to_test[2][key_id]}')
        response_json = response.json()

        errors, data = self.general_assertions(response_json)

        assert response.status_code == 200, assertion_wrong_response_status.format(200, response.status_code)

        get_response = requests.get(url)
        get_response_json = get_response.json()

        get_errors, get_data = self.general_assertions(get_response_json)

        assert isinstance(get_data, list), assertion_error_key_incorrect_type.format(key_data, 'list', type(get_data))
        assert len(get_data) == 1, assertion_error_list_incorrect_length.format(key_data, 1, len(errors))
        self.zone_equality_assertion(f'{key_data}[0]', get_data[0], zones_to_test[1], True)


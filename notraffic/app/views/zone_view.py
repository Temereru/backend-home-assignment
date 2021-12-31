from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from notraffic.app.models.zone import Zone, zone_name_max_length
from ..utils.notraffic_api_response_body import NotrafficApiResponseBody

delete_all_password = 'deleteAll'

json_header = {'Content-Type': 'application/json'}

api_ids = 'ids'
api_id = 'id'
api_name = 'name'
api_min_x = 'min_x'
api_max_x = 'max_x'
api_min_y = 'min_y'
api_max_y = 'max_y'
api_delete_all = 'all'

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


@method_decorator(csrf_exempt, name='dispatch')
class ZoneView(View):
    def get(self, request, *args, **kwargs):
        ids_list = request.GET.get(api_ids, '')

        if ids_list is None or ids_list == '':
            ids_list = []
        else:
            ids_list = ids_list.split(',')

        for got_id in ids_list:
            print(got_id, got_id.isnumeric())
            if not got_id.isnumeric():
                return HttpResponse(NotrafficApiResponseBody(None, [api_error_illegal_query_ids]).to_json(), status=400,
                                    headers=json_header)

        length = len(ids_list)

        if length == 0:
            return HttpResponse(NotrafficApiResponseBody(list(Zone.objects.all()), []).to_json(),
                                headers=json_header)
        elif length == 1:
            try:
                zone = Zone.objects.get(pk=ids_list[0])
                return HttpResponse(NotrafficApiResponseBody(model_to_dict(zone), []).to_json())
            except ObjectDoesNotExist:
                return HttpResponse(NotrafficApiResponseBody(None, [api_error_not_found.format(ids_list[0])]).to_json(),
                                    status=404,
                                    headers=json_header)
        else:
            return HttpResponse(NotrafficApiResponseBody(list(Zone.objects.filter(pk__in=ids_list)), []).to_json(),
                                headers=json_header)

    def create_zone(self, zone):
        zone = Zone(name=zone[api_name], min_x=zone[api_min_x], min_y=zone[api_min_y],
                    max_x=zone[api_max_x], max_y=zone[api_max_y])
        zone.save()

        return model_to_dict(zone)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf8'))

        if isinstance(body, list):
            errors = []
            results = []
            for zone_to_create in body:
                validation_error = self.validate_zone(zone_to_create)
                if validation_error is None:
                    zone = self.create_zone(zone_to_create)
                    results.append(zone)
                else:
                    errors.append(api_error_validation_error_for.format(api_name, zone_to_create[api_name], validation_error))

            status = 400
            if len(results) > 0:
                status = 200

            return HttpResponse(NotrafficApiResponseBody(results, errors).to_json(), status=status, headers=json_header)
        elif isinstance(body, dict):
            validation_error = self.validate_zone(body)
            if validation_error is None:
                zone = self.create_zone(body)
                return HttpResponse(NotrafficApiResponseBody(zone, []).to_json(), headers=json_header)
            else:
                return HttpResponse(NotrafficApiResponseBody(None, [validation_error]).to_json(),
                                    status=400,
                                    headers=json_header)
        else:
            return HttpResponse(NotrafficApiResponseBody(None, [api_error_illegal_post_body]).to_json(),
                                status=400,
                                headers=json_header)

    def update_zone(self, zone_to_edit):
        try:
            zone = Zone.objects.get(pk=zone_to_edit[api_id])

            if api_name in zone_to_edit:
                zone.name = zone_to_edit[api_name]

            if api_min_x in zone_to_edit:
                zone.min_x = zone_to_edit[api_min_x]

            if api_min_y in zone_to_edit:
                zone.min_y = zone_to_edit[api_min_y]

            if api_max_x in zone_to_edit:
                zone.max_x = zone_to_edit[api_max_x]

            if api_max_y in zone_to_edit:
                zone.max_y = zone_to_edit[api_max_y]

            zone.save()

            return model_to_dict(zone), 200
        except ObjectDoesNotExist:
            return api_error_zone_not_found.format(zone_to_edit[api_id]), 404

    def put(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf8'))

        if isinstance(body, list):
            print(1)
            errors = []
            results = []
            for zone_to_update in body:
                validation_error = self.validate_zone(zone_to_update)
                if validation_error is None:
                    result, status = self.update_zone(zone_to_update)
                    if status != 200:
                        errors.append(result)
                    else:
                        results.append(result)
                else:
                    errors.append(api_error_validation_error_for.format(api_id, zone_to_update[api_id], validation_error))

            status = 400
            if len(results) > 0:
                status = 200

            return HttpResponse(NotrafficApiResponseBody(results, errors).to_json(), status=status, headers=json_header)
        elif isinstance(body, dict):
            validation_error = self.validate_zone(body)
            if validation_error is None:
                result, status = self.update_zone(body)

                if status != 200:
                    return HttpResponse(NotrafficApiResponseBody(None, [result]).to_json(), status=status,
                                 headers=json_header)
                else:
                    return HttpResponse(NotrafficApiResponseBody(result, []).to_json(), status=200,
                                 headers=json_header)
            else:
                return HttpResponse(NotrafficApiResponseBody(None, [validation_error]).to_json(), status=400,
                                    headers=json_header)
        else:
            return HttpResponse(NotrafficApiResponseBody(None, [api_error_illegal_put_body]).to_json(), status=400,
                                headers=json_header)

    def delete(self, request, *args, **kwargs):
        if request.GET.get(api_ids, None) == '':
            return HttpResponse(NotrafficApiResponseBody(None, [api_error_illegal_query_ids]).to_json(), status=400,
                                headers=json_header)

        ids_list = request.GET.get(api_ids)

        if ids_list is None:
            ids_list = []
        else:
            ids_list = ids_list.split(',')

        for got_id in ids_list:
            print(got_id, got_id.isnumeric())
            if not got_id.isnumeric():
                return HttpResponse(NotrafficApiResponseBody(None, [api_error_illegal_query_ids]).to_json(), status=400,
                                    headers=json_header)

        length = len(ids_list)

        if length == 0:
            if request.GET.get(api_delete_all, '') == delete_all_password:
                Zone.objects.all().delete()
                return HttpResponse(NotrafficApiResponseBody(None, []).to_json(), headers=json_header)
            else:
                return HttpResponse(NotrafficApiResponseBody(None, [api_error_delete_unknown]).to_json(),
                                    headers=json_header)
        elif length == 1:
            try:
                Zone.objects.get(pk=ids_list[0]).delete()
                return HttpResponse(NotrafficApiResponseBody(None, []).to_json(), headers=json_header)
            except ObjectDoesNotExist:
                return HttpResponse(NotrafficApiResponseBody(None, [api_error_not_found.format(ids_list[0])]).to_json(),
                                    status=404,
                                    headers=json_header)
        else:
            Zone.objects.filter(pk__in=ids_list).delete()
            return HttpResponse(NotrafficApiResponseBody(None, []).to_json(), headers=json_header)


    def validate_zone(self, zone, is_edit=False):
        print(f'validate_zone: {zone}')

        if api_name not in zone and not is_edit:
            return validation_error_is_required.format(api_name)

        if api_name in zone and (not isinstance(zone[api_name], str) or len(zone[api_name]) == 0 or len(
                zone[api_name]) > zone_name_max_length):
            return validation_error_empty_string.format(api_name, zone_name_max_length)

        if api_min_x not in zone and not is_edit:
            return validation_error_is_required.format(api_min_x)

        if api_min_x in zone and (not isinstance(zone[api_min_x], int) or zone[api_min_x] < 0):
            return validation_error_wrong_int.format(api_min_x)

        if api_max_x not in zone and not is_edit:
            return validation_error_is_required.format(api_max_x)

        if api_max_x in zone and (not isinstance(zone[api_max_x], int) or zone[api_max_x] < 0):
            return validation_error_wrong_int.format(api_max_x)

        if api_min_x in zone and api_max_x in zone:
            if zone[api_min_x] >= zone[api_max_x]:
                return validation_error_need_to_be_larger.format(api_max_x, api_min_x)

        if api_min_y not in zone and not is_edit:
            return validation_error_is_required.format(api_min_y)

        if api_min_y in zone and (not isinstance(zone[api_min_y], int) or zone[api_min_y] < 0):
            return validation_error_wrong_int.format(api_min_y)

        if api_max_y not in zone and not is_edit:
            return validation_error_is_required.format(api_max_y)

        if api_max_y in zone and (not isinstance(zone[api_max_y], int) or zone[api_max_y] < 0):
            return validation_error_wrong_int.format(api_max_y)

        if api_min_y in zone and api_max_y in zone:
            if zone[api_min_y] >= zone[api_max_y]:
                return validation_error_need_to_be_larger.format(api_max_y, api_min_y)

        return None

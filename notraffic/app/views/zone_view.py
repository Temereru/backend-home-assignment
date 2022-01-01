from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from notraffic.app.models.zone import Zone, zone_name_max_length
from ..utils.strings.keys import *
from ..utils.strings.errors import *
from ..utils.notraffic_api_response_body import NotrafficApiResponseBody
from ..utils.validations.zone_validations import validate_zone

delete_all_password = 'deleteAll'

json_header = {'Content-Type': 'application/json'}


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
                validation_error = validate_zone(zone_to_create)
                if validation_error is None:
                    zone = self.create_zone(zone_to_create)
                    results.append(zone)
                else:
                    errors.append(api_error_validation_error_for.format(api_name,
                                                                        zone_to_create[api_name],
                                                                        validation_error))

            status = 400
            if len(results) > 0:
                status = 200

            return HttpResponse(NotrafficApiResponseBody(results, errors).to_json(), status=status, headers=json_header)
        elif isinstance(body, dict):
            validation_error = validate_zone(body)
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
                validation_error = validate_zone(zone_to_update)
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
            validation_error = validate_zone(body)
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

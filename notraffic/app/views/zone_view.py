from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from notraffic.app.models.zone import Zone


@method_decorator(csrf_exempt, name='dispatch')
class ZoneView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET, request.GET.getlist('names'))

        names_list = request.GET.getlist('names')
        length = len(names_list)

        if length == 0:
            return HttpResponse(serializers.serialize('json', Zone.objects.all()),
                                headers={'Content-Type': 'application/json'})
        elif length == 1:
            try:
                item = Zone.objects.get(pk=names_list[0])
                return HttpResponse(serializers.serialize('json', [item]))
            except  ObjectDoesNotExist:
                return HttpResponse(status=404)
        else:
            return HttpResponse(serializers.serialize('json', Zone.objects.filter(pk__in=names_list)),
                                headers={'Content-Type': 'application/json'})

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf8'))

        validation = self.validate_zone(body)

        if validation is None:
            zone = Zone(name=body['name'], min_x=body['minx'], min_y=body['miny'], max_x=body['maxx'], max_y=body['maxy'])
            zone.save()

            return HttpResponse(serializers.serialize('json', [zone]))
        else:
            return validation

    def put(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf8'))
        validation = self.validate_zone(body)
        print(json.loads(request.body.decode('utf8')))
        return HttpResponse(request.body)

    def delete(self, request, *args, **kwargs):
        print(request.GET)
        return HttpResponse(json.dumps(request.GET))

    def validate_zone(self, zone, is_edit=False):
        print(f'validate_zone: {zone}')

        if 'name' not in zone and not is_edit:
            return HttpResponse('name is required', status=400)

        if 'name' in zone and (not isinstance(zone['name'], str) or len(zone['name']) == 0):
            return HttpResponse('name needs to be a string of at least 1 character', status=400)

        if 'minx' not in zone and not is_edit:
            return HttpResponse('minx is required', status=400)

        if 'minx' in zone and (not isinstance(zone['minx'], int) or zone['minx'] < 0):
            return HttpResponse('minx needs to be an integer larger or equal to 0', status=400)

        if 'maxx' not in zone and not is_edit:
            return HttpResponse('maxx is required', status=400)

        if 'maxx' in zone and (not isinstance(zone['maxx'], int) or zone['maxx'] < 0):
            return HttpResponse('maxx needs to be an integer larger or equal to 0', status=400)

        if 'minx' in zone and 'maxx' in zone:
            if zone['minx'] >= zone['maxx']:
                return HttpResponse('maxx needs larger than minx', status=400)

        if 'miny' not in zone and not is_edit:
            return HttpResponse('miny is required', status=400)

        if 'miny' in zone and (not isinstance(zone['miny'], int) or zone['miny'] < 0):
            return HttpResponse('miny needs to be an integer larger or equal to 0', status=400)

        if 'maxy' not in zone and not is_edit:
            return HttpResponse('maxy is required', status=400)

        if 'maxy' in zone and (not isinstance(zone['maxy'], int) or zone['maxy'] < 0):
            return HttpResponse('maxy needs to be an integer larger or equal to 0', status=400)

        if 'miny' in zone and 'maxy' in zone:
            if zone['miny'] >= zone['maxy']:
                return HttpResponse('maxy needs larger than miny', status=400)

        return None

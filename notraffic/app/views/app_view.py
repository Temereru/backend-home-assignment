from django.http import HttpResponse
from django.views import View


class AppView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Your Application is up and running!')

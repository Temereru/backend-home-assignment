from django.urls import path

from notraffic.app.views.app_view import AppView
from notraffic.app.views.zone_view import ZoneView

urlpatterns = [
    path('', AppView.as_view()),
    path('zone/', ZoneView.as_view())
]
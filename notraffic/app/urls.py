from django.urls import path

from notraffic.app.views.app_view import AppView

urlpatterns = [
    path('', AppView.as_view()),
]
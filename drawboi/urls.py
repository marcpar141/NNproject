from django.urls import path

from . import views

urlpatterns = [
    path('/start', views.start_screen, name='view start'),
    path('/test', views.start_screen, name='view test'),
    path('/draw', views.start_screen, name='view draw'),
    path('/end', views.start_screen, name='view end'),
]
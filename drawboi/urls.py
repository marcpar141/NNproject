from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda request: redirect('start/', permanent=False)),
    path('start/', views.start_screen, name='view start'),
    path('test/', views.test_me, name='view test'),
    path('draw/', views.draw_screen, name='view draw'),
    path('end/', views.end_screen, name='view end'),
]
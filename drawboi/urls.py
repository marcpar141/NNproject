from django.urls import path

from . import views

urlpatterns = [
    path('start/', views.start_screen, name='view start'),
    path('test/', views.test_me, name='view test'),
    path('draw/', views.draw_screen, name='view draw'),
    path('end/', views.end_screen, name='view end'),
]
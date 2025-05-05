from . import views

from django.urls import path

urlpatterns = [
    path('', views.api_default),
    path('v1.0', views.api_v1_0),
]
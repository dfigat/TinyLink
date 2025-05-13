from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_default),
    path('v1.0/', views.api_v1_0),
    path('v1.0/short/', views.create_tiny_link),
    path('v1.0/short/<str:code>/', views.redirect_by_short_code),
    path('v1.0/all',views.show_all_records),
    path('v1.0/config',views.show_configuration),
    path('v1.0/code/<path:long_link>/', views.show_code),
    path('v1.0/short/delete_old', views.delete_all_by_threshold),
    path('v1.0/short/delete_by_code/<str:code>/', views.delete_by_code)
]
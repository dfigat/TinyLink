from django.urls import path

from . import views
from .config import API_VERSION


urlpatterns = [
    path('', views.api_default),
    path(f'v{API_VERSION}/', views.api_v1_0),
    path(f'v{API_VERSION}/short/', views.create_tiny_link),
    path(f'v{API_VERSION}/short/<str:code>/', views.redirect_by_short_code),
    path(f'v{API_VERSION}/all',views.show_all_records),
    path(f'v{API_VERSION}/get_count_all', views.count_all_records),
    path(f'v{API_VERSION}/config',views.show_configuration),
    path(f'v{API_VERSION}/code/<path:long_link>/', views.show_code),
    path(f'v{API_VERSION}/short/delete_old', views.delete_all_by_threshold),
    path(f'v{API_VERSION}/short/delete_by_code/<str:code>/', views.delete_by_code),
    path(f'v{API_VERSION}/is_alive', views.is_alive),
    path(f'v{API_VERSION}/get_tokens/', views.get_tokens),
    path(f'v{API_VERSION}/refresh_token/', views.refresh_token)
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_default),
    path('v1.0/', views.api_v1_0),
    path('v1.0/short', views.create_tiny_link),
    path('v1.0/short/<str:code>/', views.redirect_by_short_code),
    path('v1.0/all',views.show_all_records)
]
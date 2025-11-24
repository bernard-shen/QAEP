from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.device_list, name='device_list'),
    path('devices/create/', views.device_create, name='device_create'),
    path('devices/<int:device_id>/', views.device_detail, name='device_detail'),
    path('devices/<int:device_id>/update/', views.device_update, name='device_update'),
    path('devices/<int:device_id>/delete/', views.device_delete, name='device_delete'),
    path('devices/<int:device_id>/occupy/', views.device_occupy, name='device_occupy'),
    path('devices/<int:device_id>/apply/', views.device_apply, name='device_apply'),
    path('devices/<int:device_id>/release/', views.device_release, name='device_release'),
    path('devices/applies/', views.apply_list, name='apply_list'),
    path('devices/applies/<int:apply_id>/approve/', views.apply_approve, name='apply_approve'),
] 
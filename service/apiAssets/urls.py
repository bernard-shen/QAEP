from django.urls import path
from . import views

urlpatterns = [
    path('apis/', views.api_list, name='api_list'),
    path('apis/create/', views.api_create, name='api_create'),
    path('apis/<int:api_id>/', views.api_detail, name='api_detail'),
    path('apis/<int:api_id>/update/', views.api_update, name='api_update'),
    path('apis/<int:api_id>/delete/', views.api_delete, name='api_delete'),
] 
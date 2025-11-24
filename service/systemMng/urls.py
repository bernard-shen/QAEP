from django.urls import path
from . import views

urlpatterns = [
    path('menus/', views.menu_list, name='menu_list'),
    path('menus/create/', views.menu_create, name='menu_create'),
    path('menus/<int:menu_id>/update/', views.menu_update, name='menu_update'),
    path('menus/<int:menu_id>/delete/', views.menu_delete, name='menu_delete'),
    path('roles/', views.role_list, name='role_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/<int:role_id>/update/', views.role_update, name='role_update'),
    path('roles/<int:role_id>/delete/', views.role_delete, name='role_delete'),
    path('users/', views.user_list, name='user_list'),
    path('users/menu', views.user_menu, name='user_menu'),

    path('users/detail/', views.user_detail, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<str:uid>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('auth/login/', views.user_login, name='user_login'),
    path('auth/register/', views.register, name='user_register'),
    path('auth/reset-password/', views.reset_password, name='reset_password'),
]  
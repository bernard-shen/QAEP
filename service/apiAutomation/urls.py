from django.urls import path
from . import views

urlpatterns = [
    # Environment URLs
    path('environments/', views.environment_list, name='environment-list'),
    path('environments/<int:env_id>/', views.environment_detail, name='environment-detail'),
    path('environments/create/', views.environment_create, name='environment-create'),
    path('environments/<int:env_id>/update/', views.environment_update, name='environment-update'),
    path('environments/<int:env_id>/delete/', views.environment_delete, name='environment-delete'),
    
    # Account URLs
    path('accounts/', views.account_list, name='account-list'),
    path('accounts/<int:account_id>/', views.account_detail, name='account-detail'),
    path('accounts/create/', views.account_create, name='account-create'),
    path('accounts/<int:account_id>/update/', views.account_update, name='account-update'),
    path('accounts/<int:account_id>/delete/', views.account_delete, name='account-delete'),

    # Test Case URLs
    path('test-cases/', views.test_case_list, name='test-case-list'),
    path('test-cases/<int:case_id>/', views.test_case_detail, name='test-case-detail'),
    path('test-cases/create/', views.test_case_create, name='test-case-create'),
    path('test-cases/<int:case_id>/update/', views.test_case_update, name='test-case-update'),
    path('test-cases/<int:case_id>/delete/', views.test_case_delete, name='test-case-delete'),
] 
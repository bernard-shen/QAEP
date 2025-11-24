from django.urls import path
from . import views

urlpatterns = [
    path('connections/', views.connection_list, name='connection_list'),
    path('connections/check-name/', views.check_connect_name, name='check_connect_name'),
    path('connections/create/', views.add_connection, name='add_connection'),
    path('connections/<str:connect_id>/delete/', views.delete_connection, name='delete_connection'),
    path('connections/<str:connect_id>/update/', views.update_connection, name='update_connection'),
    path('connections/test/', views.test_connection, name='test_connection'),
    path('mock-data/', views.mock_connect_data, name='mock_connect_data'),
    path('db-list/', views.get_db_list_view, name='get_db_list'),
    path('table-list/', views.get_table_list_view, name='get_table_list'),
    path('column-list/', views.get_column_list_view, name='get_column_list'),
    path('secret-list/', views.get_secret_list_view, name='get_secret_list'),
    path('mock-data-file/', views.download_mock_data, name='download_mock_data'),
    path('mock-data-preview/', views.preview_mock_data, name='preview_mock_data'),
] 
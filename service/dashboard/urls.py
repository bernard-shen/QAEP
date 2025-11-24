from .views import get_count_data, get_trend_data, get_api_distribution, get_case_distribution
from django.urls import path


# URL 应该表示资源，而不是操作，所以这里的path建议不要用动词
urlpatterns = [
    path('counts', get_count_data, name='get_home_data'),
    path('trends', get_trend_data, name='get_trend_data'),
    path('api-distribution', get_api_distribution, name='get_api_distribution'),
    path('case-distribution', get_case_distribution, name='get_case_distribution'),
]
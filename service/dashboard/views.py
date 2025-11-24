from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum, Q
from apiAutomation.models import TestCase, TestScene
from deviceMng.models import Device
from mockData.models import MockHistory
from apiAssets.models import ApiInfo
from django.utils import timezone
from datetime import timedelta


def get_count_data(request):
    # data = {
    #     "apis": "",
    #     "scenes": "",
    #     "plans": "",
    #     "mock_sql_lines": "",
    #     "mock_file_lines": "",
    #     "mock_business_lines": "",
    #     "machine_total": "",
    #     "machine_used": "",
    #     "machine_free": ""
    # }
    
    # 获取接口自动化数据
    api_count = ApiInfo.objects.filter(is_deleted=False).count()
    scene_count = TestScene.objects.filter(is_deleted=False).count()
    
    # 获取设备数据
    device_total = Device.objects.count()
    device_used = Device.objects.filter(status='1').count()
    device_free = Device.objects.filter(status='0').count()
    
    # 获取mock数据
    # 统计最近30天的数据
    thirty_days_ago = timezone.now() - timedelta(days=30)
    mock_data = MockHistory.objects.filter(
        create_time__gte=thirty_days_ago
    ).aggregate(
        sql_lines=Sum('increment_lines', filter=Q(mock_type='sql')),
        file_lines=Sum('increment_lines', filter=Q(mock_type='file')),
        business_count=Count('schema_name', distinct=True)
    )
    
    data = {
        "apis": str(api_count),
        "scenes": str(scene_count),
        "plans": str(scene_count),  # 暂时用场景数代替计划数
        "mock_sql_lines": str(mock_data['sql_lines'] or 0),
        "mock_file_lines": str(mock_data['file_lines'] or 0),
        "mock_business_lines": str(mock_data['business_count'] or 0),
        "machine_total": str(device_total),
        "machine_used": str(device_used),
        "machine_free": str(device_free)
    }
    
    return JsonResponse({
        'code': 200,
        'data': data
    })


def get_trend_data(request):
    # data = {
    #     "sql_mock_list_by_day": [],
    #     "file_mock_list_by_day": [],
    #     "bz_mock_list_by_day": [],
    #     "sql_mock_list_by_month": [],
    #     "file_mock_list_by_month": [],
    #     "bz_mock_list_by_month": [],
    #     "sql_mock_list_by_year": [],
    #     "file_mock_list_by_year": [],
    #     "bz_mock_list_by_year": [],
    #     "automation_data_by_day": {"total": "", "success": "", "fail": "", "block":""},
    #     "automation_data_by_month": {"total": "", "success": "", "fail": "", "block":""},
    #     "automation_data_by_year": {"total": "", "success": "", "fail": "", "block":""}
    # }
    
    # 获取最近10天的数据
    ten_days_ago = timezone.now() - timedelta(days=10)
    
    # Mock数据统计
    daily_mock = MockHistory.objects.filter(
        create_time__gte=ten_days_ago
    ).values('create_time__date').annotate(
        sql_count=Sum('increment_lines', filter=Q(mock_type='sql')),
        file_count=Sum('increment_lines', filter=Q(mock_type='file')),
        bz_count=Count('schema_name', distinct=True)
    ).order_by('create_time__date')
    
    # 自动化数据统计
    daily_automation = TestCase.objects.filter(
        update_time__gte=ten_days_ago
    ).values('update_time__date').annotate(
        total=Count('id'),
        success=Count('id', filter=Q(run_status='normal')),
        fail=Count('id', filter=Q(run_status='abnormal')),
        block=Count('id', filter=Q(run_status='abnormal', last_result__isnull=True))
    ).order_by('update_time__date')
    
    # 处理数据格式
    sql_mock_list = [item['sql_count'] or 0 for item in daily_mock]
    file_mock_list = [item['file_count'] or 0 for item in daily_mock]
    bz_mock_list = [item['bz_count'] or 0 for item in daily_mock]
    
    # 确保列表长度为10，不足的补0
    while len(sql_mock_list) < 10:
        sql_mock_list.append(0)
    while len(file_mock_list) < 10:
        file_mock_list.append(0)
    while len(bz_mock_list) < 10:
        bz_mock_list.append(0)
    
    # 获取最新一天的自动化数据
    latest_automation = daily_automation.last() or {
        'total': 0,
        'success': 0,
        'fail': 0,
        'block': 0
    }
    
    data = {
        "sql_mock_list_by_day": sql_mock_list,
        "file_mock_list_by_day": file_mock_list,
        "bz_mock_list_by_day": bz_mock_list,
        "sql_mock_list_by_month": sql_mock_list,  # 暂时用日数据代替
        "file_mock_list_by_month": file_mock_list,
        "bz_mock_list_by_month": bz_mock_list,
        "sql_mock_list_by_year": sql_mock_list,
        "file_mock_list_by_year": file_mock_list,
        "bz_mock_list_by_year": bz_mock_list,
        "automation_data_by_day": {
            "total": latest_automation['total'],
            "success": latest_automation['success'],
            "fail": latest_automation['fail'],
            "block": latest_automation['block']
        },
        "automation_data_by_month": {
            "total": latest_automation['total'] * 30,
            "success": latest_automation['success'] * 30,
            "fail": latest_automation['fail'] * 30,
            "block": latest_automation['block'] * 30
        },
        "automation_data_by_year": {
            "total": latest_automation['total'] * 365,
            "success": latest_automation['success'] * 365,
            "fail": latest_automation['fail'] * 365,
            "block": latest_automation['block'] * 365
        }
    }
    
    return JsonResponse({
        'code': 200,
        'data': data
    })


def get_api_distribution(request):
    """获取接口分布统计数据"""
    api_distribution = ApiInfo.objects.filter(
        is_deleted=False
    ).values('of_business').annotate(
        count=Count('id')
    ).order_by('-count')
    
    data = [{
        'business': item['of_business'],
        'count': item['count']
    } for item in api_distribution]
    
    return JsonResponse({
        'code': 200,
        'data': data
    })


def get_case_distribution(request):
    """获取测试用例分布统计数据"""
    case_distribution = TestCase.objects.filter(
        is_deleted=False
    ).values('business').annotate(
        count=Count('id')
    ).order_by('-count')
    
    data = [{
        'business': item['business'],
        'count': item['count']
    } for item in case_distribution]
    
    # return JsonResponse({
    #     'code': 200,
    #     'data': data
    # })
    
    # 测试数据
    return JsonResponse({
        'code': 200,
        'data': [{'business': 'OA', 'count': 10}, {'business': '汇金', 'count': 20}, {'business': '应收', 'count': 30}]
    })


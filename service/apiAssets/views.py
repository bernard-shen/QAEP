from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import ApiInfo
from .forms import ApiInfoForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Create your views here.

# API列表
@require_http_methods(["GET"])
def api_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    env = request.GET.get('env')
    of_business = request.GET.get('of_business')
    api_name = request.GET.get('api_name')
    
    apis = ApiInfo.objects.filter(is_deleted=False)
    
    # 过滤条件
    if env:
        apis = apis.filter(env=env)
        print(f"Filtered apis count: {apis.count()}")
    if of_business:
        apis = apis.filter(of_business=of_business)
    if api_name:
        apis = apis.filter(api_name=api_name)
        print(f"Filtered by api_name: {api_name}")
        print(f"Results count: {apis.count()}")
    
    paginator = Paginator(apis.order_by('-update_time'), page_size)
    
    try:
        apis_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'id': api.id,
        'env': api.env,
        'of_business': api.of_business,
        'host': api.host,
        'api_name': api.api_name,
        'api_path': api.api_path,
        'req_method': api.req_method,
        'req_header': api.req_header,
        'req_body': api.req_body,
        'body_type': api.body_type,
        'req_params': api.req_params,
        'extr_value': api.extr_value,
        'update_time': timezone.localtime(api.update_time).strftime('%Y-%m-%d %H:%M:%S'),
    } for api in apis_page]
    
    return JsonResponse({
        'code': 200,
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })

# API详情
@require_http_methods(["GET"])
def api_detail(request, api_id):
    api = get_object_or_404(ApiInfo, id=api_id, is_deleted=False)
    return JsonResponse({
        'code': 200,
        'data': {
            'id': api.id,
            'env': api.env,
            'of_business': api.of_business,
            'host': api.host,
            'api_name': api.api_name,
            'api_path': api.api_path,
            'req_method': api.req_method,
            'req_body': api.req_body,
            'body_type': api.body_type,
            'req_header': api.req_header,
            'req_params': api.req_params,
            'resp_demo': api.resp_demo,
            'extr_value': api.extr_value,
            'create_time': timezone.localtime(api.create_time).strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': timezone.localtime(api.update_time).strftime('%Y-%m-%d %H:%M:%S'),
        }
    })

# 创建API
@csrf_exempt
@require_http_methods(["POST"])
def api_create(request):
    data = json.loads(request.body)
    form = ApiInfoForm(data)
    
    if form.is_valid():
        api = form.save()
        return JsonResponse({'code': 200, 'message': '创建成功', 'id': api.id})
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

# 更新API
@csrf_exempt
@require_http_methods(["PUT"])
def api_update(request, api_id):
    api = get_object_or_404(ApiInfo, id=api_id, is_deleted=False)
    data = json.loads(request.body)
    
    form = ApiInfoForm(data, instance=api)
    if form.is_valid():
        api = form.save()
        return JsonResponse({'code': 200, 'message': '更新成功'})
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

# 删除API（软删除）
@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete(request, api_id):
    api = get_object_or_404(ApiInfo, id=api_id, is_deleted=False)
    api.is_deleted = True
    api.save()
    return JsonResponse({'code': 200, 'message': '删除成功'})

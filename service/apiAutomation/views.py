from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils import timezone
from .models import TestEnvironment, TestAccount, TestCase
import json

# Forms for validation
class TestEnvironmentForm:
    def __init__(self, data, instance=None):
        self.data = data
        self.instance = instance
        self.errors = {}

    def is_valid(self):
        required_fields = ['business', 'env', 'name', 'domain']
        for field in required_fields:
            if field not in self.data:
                self.errors[field] = f"{field} is required"
        return len(self.errors) == 0

    def save(self):
        if self.instance:
            for key, value in self.data.items():
                setattr(self.instance, key, value)
            self.instance.save()
            return self.instance
        else:
            return TestEnvironment.objects.create(**self.data)

class TestAccountForm:
    def __init__(self, data, instance=None):
        self.data = data
        self.instance = instance
        self.errors = {}

    def is_valid(self):
        required_fields = ['business', 'env', 'username', 'password']
        for field in required_fields:
            if field not in self.data:
                self.errors[field] = f"{field} is required"
        return len(self.errors) == 0

    def save(self):
        if self.instance:
            for key, value in self.data.items():
                setattr(self.instance, key, value)
            self.instance.save()
            return self.instance
        else:
            return TestAccount.objects.create(**self.data)

class TestCaseForm:
    def __init__(self, data, instance=None):
        self.data = data
        self.instance = instance
        self.errors = {}

    def is_valid(self):
        required_fields = ['name', 'business', 'env', 'account', 'api_list']
        for field in required_fields:
            if field not in self.data:
                self.errors[field] = f"{field} is required"
        return len(self.errors) == 0

    def save(self):
        if self.instance:
            for key, value in self.data.items():
                setattr(self.instance, key, value)
            self.instance.save()
            return self.instance
        else:
            return TestCase.objects.create(**self.data)

# Environment Views
@require_http_methods(["GET"])
def environment_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    business = request.GET.get('business')
    env = request.GET.get('env')
    
    environments = TestEnvironment.objects.filter(is_deleted=False)
    
    if business:
        environments = environments.filter(business=business)
    if env:
        environments = environments.filter(env=env)
    
    paginator = Paginator(environments.order_by('-update_time'), page_size)
    
    try:
        envs_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'id': env.id,
        'business': env.business,
        'env': env.env,
        'name': env.name,
        'domain': env.domain,
        'create_time': timezone.localtime(env.create_time).strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': timezone.localtime(env.update_time).strftime('%Y-%m-%d %H:%M:%S'),
    } for env in envs_page]
    
    return JsonResponse({
        'code': 200,
        'message': '获取成功',
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })

@require_http_methods(["GET"])
def environment_detail(request, env_id):
    env = get_object_or_404(TestEnvironment, id=env_id, is_deleted=False)
    return JsonResponse({
        'code': 200,
        'message': '获取成功',
        'data': {
            'id': env.id,
            'business': env.business,
            'env': env.env,
            'name': env.name,
            'domain': env.domain,
            'create_time': timezone.localtime(env.create_time).strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': timezone.localtime(env.update_time).strftime('%Y-%m-%d %H:%M:%S'),
        }
    })

@csrf_exempt
@require_http_methods(["POST"])
def environment_create(request):
    data = json.loads(request.body)
    form = TestEnvironmentForm(data)
    
    if form.is_valid():
        env = form.save()
        return JsonResponse({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': env.id
            }
        })
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

@csrf_exempt
@require_http_methods(["PUT"])
def environment_update(request, env_id):
    env = get_object_or_404(TestEnvironment, id=env_id, is_deleted=False)
    data = json.loads(request.body)
    
    form = TestEnvironmentForm(data, instance=env)
    if form.is_valid():
        env = form.save()
        return JsonResponse({'code': 200, 'message': '更新成功'})
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

@csrf_exempt
@require_http_methods(["DELETE"])
def environment_delete(request, env_id):
    env = get_object_or_404(TestEnvironment, id=env_id, is_deleted=False)
    env.is_deleted = True
    env.save()
    return JsonResponse({'code': 200, 'message': '删除成功'})

# Account Views
@require_http_methods(["GET"])
def account_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    business = request.GET.get('business')
    env = request.GET.get('env')
    
    accounts = TestAccount.objects.filter(is_deleted=False)
    
    if business:
        accounts = accounts.filter(business=business)
    if env:
        accounts = accounts.filter(env=env)
    
    paginator = Paginator(accounts.order_by('-update_time'), page_size)
    
    try:
        accounts_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'id': account.id,
        'business': account.business,
        'env': account.env,
        'username': account.username,
        'create_time': timezone.localtime(account.create_time).strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': timezone.localtime(account.update_time).strftime('%Y-%m-%d %H:%M:%S'),
    } for account in accounts_page]
    
    return JsonResponse({
        'code': 200,
        'message': '获取成功',
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })

@require_http_methods(["GET"])
def account_detail(request, account_id):
    account = get_object_or_404(TestAccount, id=account_id, is_deleted=False)
    return JsonResponse({
        'code': 200,
        'message': '获取成功',
        'data': {
            'id': account.id,
            'business': account.business,
            'env': account.env,
            'username': account.username,
            'create_time': timezone.localtime(account.create_time).strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': timezone.localtime(account.update_time).strftime('%Y-%m-%d %H:%M:%S'),
        }
    })

@csrf_exempt
@require_http_methods(["POST"])
def account_create(request):
    data = json.loads(request.body)
    form = TestAccountForm(data)
    
    if form.is_valid():
        account = form.save()
        return JsonResponse({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': account.id
            }
        })
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

@csrf_exempt
@require_http_methods(["PUT"])
def account_update(request, account_id):
    account = get_object_or_404(TestAccount, id=account_id, is_deleted=False)
    data = json.loads(request.body)
    
    form = TestAccountForm(data, instance=account)
    if form.is_valid():
        account = form.save()
        return JsonResponse({'code': 200, 'message': '更新成功'})
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

@csrf_exempt
@require_http_methods(["DELETE"])
def account_delete(request, account_id):
    account = get_object_or_404(TestAccount, id=account_id, is_deleted=False)
    account.is_deleted = True
    account.save()
    return JsonResponse({'code': 200, 'message': '删除成功'})

# Test Case Views
@require_http_methods(["GET"])
def test_case_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    business = request.GET.get('business')
    env = request.GET.get('env')
    
    cases = TestCase.objects.filter(is_deleted=False)
    
    if business:
        cases = cases.filter(business=business)
    if env:
        cases = cases.filter(env=env)
    
    paginator = Paginator(cases.order_by('-update_time'), page_size)
    
    try:
        cases_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'id': case.id,
        'name': case.name,
        'business': case.business,
        'env': case.env,
        'account': case.account,
        'api_list': case.api_list,
        'run_status': case.run_status,
        'last_result': case.last_result,
        'create_time': timezone.localtime(case.create_time).strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': timezone.localtime(case.update_time).strftime('%Y-%m-%d %H:%M:%S'),
    } for case in cases_page]
    
    return JsonResponse({
        'code': 200,
        'message': '获取成功',
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })

@require_http_methods(["GET"])
def test_case_detail(request, case_id):
    case = get_object_or_404(TestCase, id=case_id, is_deleted=False)
    return JsonResponse({
        'code': 200,
        'message': '获取成功',
        'data': {
            'id': case.id,
            'name': case.name,
            'business': case.business,
            'env': case.env,
            'account': case.account,
            'api_list': case.api_list,
            'execution_body': case.execution_body,
            'extract_body': case.extract_body,
            'assert_body': case.assert_body,
            'run_status': case.run_status,
            'last_result': case.last_result,
            'create_time': timezone.localtime(case.create_time).strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': timezone.localtime(case.update_time).strftime('%Y-%m-%d %H:%M:%S'),
        }
    })

@csrf_exempt
@require_http_methods(["POST"])
def test_case_create(request):
    data = json.loads(request.body)
    form = TestCaseForm(data)
    
    if form.is_valid():
        case = form.save()
        return JsonResponse({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': case.id
            }
        })
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

@csrf_exempt
@require_http_methods(["PUT"])
def test_case_update(request, case_id):
    case = get_object_or_404(TestCase, id=case_id, is_deleted=False)
    data = json.loads(request.body)
    
    form = TestCaseForm(data, instance=case)
    if form.is_valid():
        case = form.save()
        return JsonResponse({'code': 200, 'message': '更新成功'})
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

@csrf_exempt
@require_http_methods(["DELETE"])
def test_case_delete(request, case_id):
    case = get_object_or_404(TestCase, id=case_id, is_deleted=False)
    case.is_deleted = True
    case.save()
    return JsonResponse({'code': 200, 'message': '删除成功'})

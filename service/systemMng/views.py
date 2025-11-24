from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Menu, Role, User 
import json
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, MenuSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime
from django.db.models import Max
from .forms import UserLoginForm, UserRegisterForm
import logging
import time

logger = logging.getLogger(__name__)

def success_response(data=None, message="请求成功", count=None):
    response = {
        'code': 200,
        'message': message,
        'data': data or []
    }
    if count is not None:
        response['count'] = count
    return JsonResponse(response)

def error_response(message="请求失败"):
    return JsonResponse({
        'code': 400,
        'message': message,
        'data': []
    })

# 用户登录
@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        try:
            user = User.objects.get(username=username, is_deleted=False)
            if not check_password(password, user.password):
                return JsonResponse({'code': 400, 'message': '密码错误'})
            
            # 生成 token
            refresh = RefreshToken.for_user(user)
            # 添加自定义声明 - 确保 uid 是字符串
            refresh['user_uid'] = str(user.uid)  # 显式转换为字符串
            
            # 获取用户菜单权限
            FIELD = ['menu_id', 'label', 'path', 'is_base_menu', 'sub_menu', 'name', 'icon', 'url']
            role_permissions = Role.objects.get(role_name=user.roles).role_permissions

            # 区分一下，带有子菜单的菜单和不带子菜单的菜单
            if role_permissions != 'ALL':
                menus_id = json.loads(role_permissions)
                # 修改这里：先获取菜单，再检查 is_base_menu
                menu_base = Menu.objects.filter(
                    menu_id__in=menus_id,  # 使用 menu_id 进行过滤
                    is_deleted=False,
                    is_base_menu=True  # 直接过滤基础菜单
                ).values('menu_id', 'label', 'path', 'is_base_menu', 'sub_menu', 'name', 'icon', 'url')
            else:
                menu_base = Menu.objects.filter(
                    is_deleted=False, 
                    is_base_menu=True
                ).values('menu_id', 'label', 'path', 'is_base_menu', 'sub_menu', 'name', 'icon', 'url')
            for menu in menu_base:
                sub_menu = json.loads(menu['sub_menu'])  # 解析 JSON 字符串为 Python 对象
                if len(sub_menu) != 0:
                    menu.update({'children': []})
                    for sub_menu_id in sub_menu:
                        sub_value = Menu.objects.filter(menu_id=sub_menu_id).values('menu_id', 'label', 'path', 'name',
                                                                                    'icon', 'url').first()
                        menu['children'].append(sub_value)  # 将子菜单数据添加到 children 列表中

            user_data = UserSerializer(user).data
            # role_data = Role.objects.get(role_name=user.roles).role_name
            return JsonResponse({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'user_info': user_data,
                    'menus': list(menu_base),
                    'token': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
        except User.DoesNotExist:
            return JsonResponse({'code': 400, 'message': '用户不存在'})
            
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return JsonResponse({'code': 400, 'message': f'登录失败：{str(e)}'})


# 用户注册
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        
        if User.objects.filter(username=data['username'], is_deleted=False).exists():
            return error_response("用户名已存在")
        
        # 生成 uid (格式：U + 时间戳后6位)
        timestamp = str(int(time.time()))[-6:]
        uid = f"U{timestamp}"
        
        # 创建新用户
        user = User.objects.create(
            uid=uid,
            username=data['username'],
            password=make_password(data['password']),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            roles='游客',  # 设置默认角色
            is_deleted=False
        )
        
        return JsonResponse({
            'code': 200,
            'message': '注册成功',
            'data': {
                'uid': user.uid,
                'username': user.username
            }
        })
            
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        return error_response(f"注册失败：{str(e)}")


# 重置密码
@csrf_exempt
@require_http_methods(["POST"])
def reset_password(request):
    data = json.loads(request.body)
    username = data.get('username')
    new_password = data.get('password')
    
    try:
        user = User.objects.get(username=username)
        user.password = make_password(new_password)
        user.save()
        return JsonResponse({'code': 200, 'message': '密码重置成功'})
    except User.DoesNotExist:
        return JsonResponse({'code': 400, 'message': '用户不存在'})
    

# Create your views here.
# 菜单列表
@require_http_methods(["GET"])
def menu_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    menus = Menu.objects.filter(is_deleted=False)
    paginator = Paginator(menus, page_size)
    
    try:
        menus_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'menu_id': menu.menu_id,
        'label': menu.label,
        'is_base_menu': menu.is_base_menu,
        'sub_menu': menu.sub_menu,
        'path': menu.path,
        'name': menu.name,
        'icon': menu.icon,
        'url': menu.url
    } for menu in menus_page]
    
    return JsonResponse({
        'code': 200,
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })


# 创建菜单
@require_http_methods(["POST"])
def menu_create(request):
    data = json.loads(request.body)
    try:
        menu = Menu.objects.create(**data)
        return JsonResponse({'code': 200, 'message': '创建成功', 'menu_id': menu.menu_id})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': str(e)})


# 更新菜单
@require_http_methods(["POST"])
def menu_update(request, menu_id):
    menu = get_object_or_404(Menu, menu_id=menu_id, is_delete=False)
    data = json.loads(request.body)
    
    try:
        for key, value in data.items():
            setattr(menu, key, value)
        menu.save()
        return JsonResponse({'code': 200, 'message': '更新成功'})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': str(e)})


# 删除菜单（软删除）
@require_http_methods(["DELETE"])
def menu_delete(request, menu_id):
    menu = get_object_or_404(Menu, menu_id=menu_id, is_delete=False)
    menu.is_delete = True
    menu.save()
    return JsonResponse({'code': 200, 'message': '删除成功'}) 


# 角色列表
@require_http_methods(["GET"])
def role_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    roles = Role.objects.filter(is_deleted=False)
    paginator = Paginator(roles, page_size)
    
    try:
        roles_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'role_id': role.role_id,
        'role_name': role.role_name,
        'role_permissions': role.role_permissions,
        'tips': role.tips
    } for role in roles_page]
    
    return JsonResponse({
        'code': 200,
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })


# 创建角色
@require_http_methods(["POST"])
def role_create(request):
    data = json.loads(request.body)
    try:
        role = Role.objects.create(**data)
        return JsonResponse({'code': 200, 'message': '创建成功', 'role_id': role.role_id})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': str(e)})


# 更新角色
@require_http_methods(["POST"])
def role_update(request, role_id):
    role = get_object_or_404(Role, role_id=role_id, is_deleted=False)
    data = json.loads(request.body)
    
    try:
        for key, value in data.items():
            setattr(role, key, value)
        role.save()
        return JsonResponse({'code': 200, 'message': '更新成功'})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': str(e)})


@require_http_methods(["DELETE"])
def role_delete(request, role_id):
    role = get_object_or_404(Role, role_id=role_id, is_deleted=False)
    role.is_deleted = True
    role.save()
    return JsonResponse({'code': 200, 'message': '删除成功'})


# 用户列表
@require_http_methods(["GET"])
def user_detail(request):
    username = request.GET.get('username')
    users = User.objects.filter(is_deleted=False, username=username)

    data = [{
        'id': user.id,
        'uid': user.uid,
        'username': user.username,
        'roles': user.roles,
        'phone': user.phone,
        'email': user.email,
        'comment': user.comment
    } for user in users]

    return JsonResponse({
        'code': 200,
        'data': data
    })


@require_http_methods(["GET"])
def user_menu(request):
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    role_permissions = Role.objects.get(role_name=user.roles).role_permissions

    # 区分一下，带有子菜单的菜单和不带子菜单的菜单
    if role_permissions != 'ALL':
        menus_id = json.loads(role_permissions)
        filter_list = [_id for _id in menus_id if Menu.objects.get(menu_id=_id, is_deleted=False).is_base_menu]
        menu_base = Menu.objects.filter(is_deleted=False, is_base_menu__in=filter_list).values('menu_id', 'label',
                                                                                               'path', 'is_base_menu',
                                                                                               'sub_menu', 'name',
                                                                                               'icon', 'url')
    else:
        menu_base = Menu.objects.filter(is_deleted=False, is_base_menu=True).values('menu_id', 'label', 'path',
                                                                                    'is_base_menu', 'sub_menu', 'name',
                                                                                    'icon', 'url')
    for menu in menu_base:
        sub_menu = json.loads(menu['sub_menu'])  # 解析 JSON 字符串为 Python 对象
        if len(sub_menu) != 0:
            menu.update({'children': []})
            for sub_menu_id in sub_menu:
                sub_value = Menu.objects.filter(menu_id=sub_menu_id).values('menu_id', 'label', 'path', 'name',
                                                                            'icon', 'url').first()
                menu['children'].append(sub_value)  # 将子菜单数据添加到 children 列表中

    return JsonResponse({
        'code': 200,
        'data': list(menu_base)
    })

# 用户列表
@require_http_methods(["GET"])
def user_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    users = User.objects.filter(is_deleted=False)
    paginator = Paginator(users, page_size)
    
    try:
        users_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'id': user.id,
        'uid': user.uid,
        'username': user.username,
        'roles': user.roles,
        'phone': user.phone,
        'email': user.email,
        'create_time': timezone.localtime(user.create_time).strftime('%Y-%m-%d %H:%M:%S'),
        'comment': user.comment
    } for user in users_page]
    
    return JsonResponse({
        'code': 200,
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })


# 创建用户
@require_http_methods(["POST"])
def user_create(request):
    data = json.loads(request.body)
    try:
        # 这里应该添加密码加密处理
        user = User.objects.create(**data)
        return JsonResponse({'code': 200, 'message': '创建成功', 'id': user.id})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': str(e)})


# 更新用户
@csrf_exempt
@require_http_methods(["POST", "PUT"])
def user_update(request, uid):
    try:
        user = get_object_or_404(User, uid=uid, is_deleted=False)
        data = json.loads(request.body)
        
        if 'password' in data:
            data['password'] = make_password(data['password'])
            
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return JsonResponse({'code': 200, 'message': '更新成功'})
    except User.DoesNotExist:
        return JsonResponse({
            'code': 404, 
            'message': f'用户 {uid} 不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'code': 400, 
            'message': f'更新失败：{str(e)}'
        }, status=400)


# 删除用户（软删除）
@require_http_methods(["DELETE"])
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id, is_deleted=False)
    user.is_deleted = True
    user.save()
    return JsonResponse({'code': 200, 'message': '删除成功'})


@csrf_exempt
@require_http_methods(["POST"])
def user_register(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # 验证用户名是否已存在
    if User.objects.filter(username=username, is_deleted=False).exists():
        return JsonResponse({'code': 400, 'message': '用户名已存在'})
    
    # 密码加密
    hashed_password = make_password(password)
    
    try:
        # 创建新用户，默认游客权限
        user = User.objects.create(
            username=username,
            password=hashed_password,
            email=email,
            roles='游客',  # 默认游客权限
            phone=data.get('phone', '')
        )
        
        return JsonResponse({
            'code': 200,
            'message': '注册成功',
            'data': {
                'uid': user.uid,
                'username': user.username
            }
        })
    except Exception as e:
        return JsonResponse({'code': 400, 'message': f'注册失败：{str(e)}'})
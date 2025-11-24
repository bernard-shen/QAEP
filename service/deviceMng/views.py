from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Device, DeviceApply
from .forms import DeviceForm
import json
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from systemMng.models import User
from datetime import datetime
from django.db.models import Q
from django.db import connection


# @require_http_methods(["POST"])
def update_devices_used_days():
    """更新所有设备的使用天数"""
    try:
        print("开始更新设备使用天数")
        
        # 使用原生SQL查询获取数据
        with connection.cursor() as cursor:
            # 先执行一个查询看看所有字段的原始值
            cursor.execute("""
                SELECT * FROM devices 
                WHERE status = '1'
            """)
            # 获取列名
            columns = [col[0] for col in cursor.description]
            print("数据库列名:", columns)  # 打印列名
            
            # 获取并打印原始数据
            rows = cursor.fetchall()
            for row in rows:
                print("原始数据行:", row)  # 打印每一行的原始数据
            
            # 重新执行实际需要的查询
            cursor.execute("""
                SELECT id, holding_time, used_days, status
                FROM devices 
                WHERE status = '1'
            """)
            devices = [dict(zip([col[0] for col in cursor.description], row)) 
                      for row in cursor.fetchall()]
            
        print(f"处理后的设备数据: {devices}")
        
        for device_data in devices:
            device = Device.objects.get(id=device_data['id'])
            print(f"设备ID: {device.id}")
            print(f"设备状态: {device_data['status']}")
            print(f"数据库中的 holding_time: {device_data['holding_time']}")
            print(f"ORM中的 holding_time: {device.holding_time}")
            
            if device_data['holding_time']:
                try:
                    # 将时间戳转换为datetime对象
                    holding_time = datetime.fromtimestamp(
                        int(str(device_data['holding_time'])[:10]),
                        tz=timezone.utc
                    )
                    
                    now = timezone.now()
                    days = (now - holding_time).days
                    
                    if device.used_days != days:
                        device.used_days = days
                        device.save(update_fields=['used_days'])
                        print(f"更新设备 {device.id} 的使用天数为 {days}")
                except Exception as e:
                    print(f"处理设备 {device.id} 时出错: {str(e)}")
        
        return {
            'code': 200, 
            'message': '成功更新设备使用天数'
        }
        
    except Exception as e:
        print(f"更新失败: {str(e)}")
        return {
            'code': 400, 
            'message': f'更新失败：{str(e)}'
        }


# 设备列表
@require_http_methods(["GET"])
def device_list(request):
    # 更新设备使用天数
    # update_devices_used_days()
    
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    devices = Device.objects.all().order_by('-update_time')
    
    # 处理关键字搜索
    keyword = request.GET.get('keyword', '')
    if keyword:
        devices = devices.filter(
            Q(device_model__icontains=keyword) |
            Q(asset_code__icontains=keyword) |
            Q(owner__icontains=keyword) |
            Q(current_user__icontains=keyword)
        )
    
    paginator = Paginator(devices, page_size)
    
    try:
        devices_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'id': device.id,
        'device_type': device.device_type,
        'os_name': device.os_name,
        'os_version': device.os_version,
        'device_model': device.device_model,
        'asset_code': device.asset_code,
        'owner': device.owner,
        'current_user': device.current_user,
        'status': device.status,
        'used_days': device.used_days,
        'buy_time': device.buy_time,
        'update_time': timezone.localtime(device.update_time).strftime('%Y-%m-%d %H:%M:%S')
    } for device in devices_page]
    
    return JsonResponse({
        'code': 200,
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })

# 设备详情
@require_http_methods(["GET"])
def device_detail(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    return JsonResponse({
        'code': 200,
        'data': {
            'id': device.id,
            'device_type': device.device_type,
            'os_name': device.os_name,
            'os_version': device.os_version,
            'device_model': device.device_model,
            'asset_code': device.asset_code,
            'owner': device.owner,
            'current_user': device.current_user,
            'status': device.status,
            'used_days': device.used_days
        }
    })

# 新增设备
@require_http_methods(["POST"])
def device_create(request):
    data = json.loads(request.body)
    
    # 设置默认状态为空闲
    if 'status' not in data:
        data['status'] = '0'  # 默认为空闲状态
    
    # 处理日期格式
    if 'buy_time' in data and data['buy_time']:
        try:
            buy_time = datetime.strptime(data['buy_time'], '%Y-%m-%d').date()
            data['buy_time'] = buy_time
        except ValueError:
            return JsonResponse({
                'code': 400, 
                'message': '购入日期格式错误，应为 YYYY-MM-DD'
            })
    
    form = DeviceForm(data)
    
    if form.is_valid():
        device = form.save()
        return JsonResponse({'code': 200, 'message': '创建成功', 'id': device.id})
    
    return JsonResponse({'code': 400, 'message': str(form.errors)})

# 更新设备
@require_http_methods(["PUT"])
def device_update(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    data = json.loads(request.body)
    
    # 处理日期格式
    if 'buy_time' in data and data['buy_time']:
        try:
            buy_time = datetime.strptime(data['buy_time'], '%Y-%m-%d').date()
            data['buy_time'] = buy_time
        except ValueError:
            return JsonResponse({
                'code': 400, 
                'message': '购入日期格式错误，应为 YYYY-MM-DD'
            })
    
    # 只更新提供的字段
    for field, value in data.items():
        if hasattr(device, field):
            setattr(device, field, value)
    
    try:
        device.save()
        return JsonResponse({'code': 200, 'message': '更新成功'})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': f'更新失败：{str(e)}'})

# 删除设备
@require_http_methods(["DELETE"])
def device_delete(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    device.delete()
    return JsonResponse({'code': 200, 'message': '删除成功'})

# 设备占用
@require_http_methods(["POST"])
def device_occupy(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    data = json.loads(request.body)
    user = data.get('user')
    
    if not user:
        return JsonResponse({'code': 400, 'message': '请提供使用者信息'})
    
    if device.status != '0':  # 不是空闲状态
        return JsonResponse({'code': 400, 'message': '设备当前不可占用'})
    
    device.current_user = user
    device.status = '1'  # 设置为占用状态
    device.holding_time = timezone.now()  # 记录开始占用时间
    device.save()
    
    return JsonResponse({'code': 200, 'message': '设备占用成功'})

# 设备申请
@require_http_methods(["POST"])
def device_apply(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    
    # 从 Authorization header 中获取用户信息
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'code': 401, 'message': '未提供认证信息'})
            
        # 验证 token
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(auth_header.split()[1])
        
        # 从 token 中获取用户信息
        user_uid = validated_token.get('user_uid')  # 获取用户 uid
        if not user_uid:
            return JsonResponse({'code': 400, 'message': '无法获取用户信息'})
            
        # 通过 uid 获取用户名
        try:
            user = User.objects.get(uid=user_uid, is_deleted=False)
            username = user.username
        except User.DoesNotExist:
            return JsonResponse({'code': 400, 'message': '用户不存在'})
        
        if device.status != '0':  # 不是空闲状态
            return JsonResponse({'code': 400, 'message': '设备当前不可申请'})
        
        # 创建申请记录
        DeviceApply.objects.create(
            apply_user=username,  # 使用用户名
            apply_device=device.device_model,
            device_asset_code=device.asset_code,
            apply_time=timezone.now()
        )
        
        device.status = '2'  # 设置为申请中状态
        device.save()
        
        return JsonResponse({'code': 200, 'message': '设备申请成功'})
        
    except (InvalidToken, TokenError) as e:
        return JsonResponse({'code': 401, 'message': 'token无效或已过期'})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': f'申请失败：{str(e)}'})

# 设备释放
@require_http_methods(["POST"])
def device_release(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if device.status == '2':  # 申请中
        return JsonResponse({'code': 400, 'message': '申请中状态，不能释放'})

    if device.status == '0':  # 已经是空闲状态
        return JsonResponse({'code': 400, 'message': '设备已经是空闲状态'})
    
    # 计算占用天数
    if device.holding_time:
        days = (timezone.now() - device.holding_time).days
        device.used_days += days
    
    device.current_user = None
    device.status = '0'  # 设置为空闲状态
    device.holding_time = None  # 清空占用时间
    device.save()
    
    return JsonResponse({'code': 200, 'message': '设备释放成功'})

# 申请列表查询
@require_http_methods(["GET"])
def apply_list(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    status = request.GET.get('status')  # 审批状态过滤
    
    applies = DeviceApply.objects.all()
    
    # 状态过滤
    if status:
        applies = applies.filter(approval_status=status)
    
    paginator = Paginator(applies.order_by('-apply_time'), page_size)
    
    try:
        applies_page = paginator.page(page)
    except:
        return JsonResponse({'code': 400, 'message': '页码错误'})
    
    data = [{
        'id': apply.id,
        'apply_user': apply.apply_user,
        'device_model': apply.apply_device,
        'device_asset_code': apply.device_asset_code,
        'apply_time': timezone.localtime(apply.apply_time).strftime('%Y-%m-%d %H:%M:%S'),
        'approval_status': apply.approval_status,
        'approval_time': timezone.localtime(apply.approval_time).strftime('%Y-%m-%d %H:%M:%S') if apply.approval_time else None,
        'approval_user': apply.approval_user,
        'approval_comment': apply.approval_comment
    } for apply in applies_page]
    
    return JsonResponse({
        'code': 200,
        'data': data,
        'total': paginator.count,
        'total_pages': paginator.num_pages
    })

# 审批接口
@require_http_methods(["POST"])
def apply_approve(request, apply_id):
    apply = get_object_or_404(DeviceApply, id=apply_id)
    device = get_object_or_404(Device, asset_code=apply.device_asset_code)

    data = json.loads(request.body)

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return JsonResponse({'code': 401, 'message': '未提供认证信息'})    
    # 验证 token
    jwt_auth = JWTAuthentication()
    validated_token = jwt_auth.get_validated_token(auth_header.split()[1])
    
    # 从 token 中获取用户信息
    user_uid = validated_token.get('user_uid')  # 获取用户 uid
    if not user_uid:
        return JsonResponse({'code': 400, 'message': '无法获取用户信息'})
        
    # 通过 uid 获取用户名
    try:
        user = User.objects.get(uid=user_uid, is_deleted=False)
        username = user.username
    except User.DoesNotExist:
        return JsonResponse({'code': 400, 'message': '用户不存在'})
    
    # 已审批的申请不能重复审批
    if apply.approval_status != '0':
        return JsonResponse({'code': 400, 'message': '非待审批状态，不能审批'})
    
    approval_status = data.get('approval_status')
    approval_user = username

    if not approval_status or not approval_user:
        return JsonResponse({'code': 400, 'message': '缺少必要参数'})
    
    try:
        # 更新申请记录
        apply.approval_status = approval_status
        apply.approval_user = approval_user
        apply.approval_time = timezone.now()
        apply.save()
        
        # 如果审批通过，更新设备状态
        if approval_status == '1':
            device.current_user = apply.apply_user
            device.status = '1'  # 设置为占用状态
            device.holding_time = timezone.now()  # 记录开始占用时间
            # 使用 update_fields 来确保只更新需要的字段
            device.save(update_fields=['current_user', 'status', 'holding_time'])
        elif approval_status == '2':
            device.status = '0'
            device.save(update_fields=['status'])
        
        return JsonResponse({'code': 200, 'message': '审批成功'})
    except Exception as e:
        return JsonResponse({'code': 400, 'message': f'审批失败：{str(e)}'})


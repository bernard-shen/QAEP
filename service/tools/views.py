from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import datetime
from decimal import Decimal

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def quick_create_process(request):
    """
    快速发起流程接口
    入参：流程种类
    返回：流程编号
    """
    try:
        data = json.loads(request.body)
        process_type = data.get('process_type')
        
        if not process_type:
            return JsonResponse({
                'code': 400,
                'message': '流程种类不能为空',
                'data': None
            })
            
        # 生成流程编号
        process_id = str(uuid.uuid4())
        
        # TODO: 这里可以添加实际的流程创建逻辑
        # 比如保存到数据库等
        
        return JsonResponse({
            'code': 200,
            'message': '流程创建成功',
            'data': {
                'process_id': process_id
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'流程创建失败：{str(e)}',
            'data': None
        })

@csrf_exempt
@require_http_methods(["POST"])
def quick_approve_process(request):
    """
    快速审批流程接口
    入参：流程编号
    返回：流程审批结果
    """
    try:
        data = json.loads(request.body)
        process_id = data.get('process_id')
        
        if not process_id:
            return JsonResponse({
                'code': 400,
                'message': '流程编号不能为空',
                'data': None
            })
            
        # TODO: 这里可以添加实际的审批逻辑
        # 比如更新数据库中的流程状态等
        
        return JsonResponse({
            'code': 200,
            'message': '流程审批成功',
            'data': {
                'process_id': process_id,
                'status': 'approved'
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'流程审批失败：{str(e)}',
            'data': None
        })

@csrf_exempt
@require_http_methods(["POST"])
def quick_onboard_employee(request):
    """
    快速入职接口
    入参：
        - type: 入职类型 ("single"/"batch")
        - employees: 员工信息列表
    返回：入职员工的姓名工号信息列表
    """
    try:
        data = json.loads(request.body)
        onboard_type = data.get('type')
        employees_data = data.get('employees', [])

        if not onboard_type or onboard_type not in ['single', 'batch']:
            return JsonResponse({
                'code': 400,
                'message': '入职类型错误，必须为 single 或 batch',
                'data': None
            })

        if not employees_data:
            return JsonResponse({
                'code': 400,
                'message': '员工信息不能为空',
                'data': None
            })

        if onboard_type == 'single' and len(employees_data) > 1:
            return JsonResponse({
                'code': 400,
                'message': '单条入职模式下只能提交一条员工信息',
                'data': None
            })

        # 处理每个员工信息
        result_list = []
        current_year = datetime.datetime.now().strftime('%Y')
        
        for employee in employees_data:
            # 验证必要字段
            if not all(key in employee for key in ['name', 'id_card', 'department']):
                return JsonResponse({
                    'code': 400,
                    'message': '员工信息不完整，需要包含 name、id_card、department',
                    'data': None
                })
                
            # 生成工号（示例：年份 + 5位随机数）
            employee_id = f"{current_year}{str(uuid.uuid4().int)[:5]}"
            
            # TODO: 这里添加实际的入职处理逻辑
            # 1. 保存员工信息到数据库
            # 2. 创建相关账号
            # 3. 发送通知等
            
            result_list.append({
                'name': employee['name'],
                'employee_id': employee_id,
                'department': employee['department']
            })

        return JsonResponse({
            'code': 200,
            'message': '入职处理成功',
            'data': {
                'type': onboard_type,
                'total': len(result_list),
                'employees': result_list
            }
        })

    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'入职处理失败：{str(e)}',
            'data': None
        })

@csrf_exempt
@require_http_methods(["POST"])
def quick_create_dsp_data(request):
    """
    快速造数接口
    入参：
        - dsp_name: DSP名称
        - dsp_type: DSP类型
        - supplier: 供应商
        - revenue: 收入
        - cost: 支出
        - clicks: 点击数
        - impressions: 曝光数
    返回：造数是否成功
    """
    try:
        data = json.loads(request.body)
        
        # 验证必要字段
        required_fields = {
            'dsp_name': 'DSP名称',
            'dsp_type': 'DSP类型',
            'supplier': '供应商',
            'revenue': '收入',
            'cost': '支出',
            'clicks': '点击数',
            'impressions': '曝光数'
        }
        
        # 检查所有必要字段是否存在
        missing_fields = []
        for field, field_name in required_fields.items():
            if field not in data:
                missing_fields.append(field_name)
                
        if missing_fields:
            return JsonResponse({
                'code': 400,
                'message': f'缺少必要字段：{", ".join(missing_fields)}',
                'data': None
            })
            
        # 验证数值字段
        try:
            revenue = Decimal(str(data['revenue']))
            cost = Decimal(str(data['cost']))
            clicks = int(data['clicks'])
            impressions = int(data['impressions'])
            
            # 验证数值是否合法
            if revenue < 0 or cost < 0:
                return JsonResponse({
                    'code': 400,
                    'message': '收入和支出不能为负数',
                    'data': None
                })
                
            if clicks < 0 or impressions < 0:
                return JsonResponse({
                    'code': 400,
                    'message': '点击数和曝光数不能为负数',
                    'data': None
                })
                
            if clicks > impressions:
                return JsonResponse({
                    'code': 400,
                    'message': '点击数不能大于曝光数',
                    'data': None
                })
        except (ValueError, TypeError):
            return JsonResponse({
                'code': 400,
                'message': '数值字段格式错误',
                'data': None
            })
            
        # 生成记录ID
        record_id = str(uuid.uuid4())
        current_time = datetime.datetime.now()
        
        # TODO: 这里添加实际的数据存储逻辑
        # 1. 保存DSP数据到数据库
        # 2. 可能需要更新相关统计信息
        # 3. 可能需要触发其他业务逻辑
        
        return JsonResponse({
            'code': 200,
            'message': 'DSP数据创建成功',
            'data': {
                'record_id': record_id,
                'create_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'dsp_name': data['dsp_name'],
                'success': True
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'DSP数据创建失败：{str(e)}',
            'data': None
        })

from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import User
import logging
from rest_framework_simplejwt.settings import api_settings


logger = logging.getLogger(__name__)

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        logger.debug(f"Request path: {request.path}")
        logger.debug(f"Request method: {request.method}")
        logger.debug(f"Request headers: {request.headers}")
        # 不需要验证的路径
        exempt_paths = [
            '/auth/login/', 
            '/auth/register/', 
            '/admin',  # 修改为不带斜杠，这样可以匹配 /admin 和 /admin/
            '/static/',  # 所有静态文件
            '/favicon.ico',  # 添加 favicon.ico
            '/users/',  # 添加用户相关的路径
        ]
        
        # 检查请求路径是否需要豁免
        path = request.path
        if path == '/':  # 根路径豁免
            return self.get_response(request)
            
        # 检查是否是豁免路径
        if any(path.startswith(exempt_path) for exempt_path in exempt_paths):
            return self.get_response(request)

        try:
            # 获取 token
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return JsonResponse({'code': 401, 'message': '未提供认证信息'}, status=401)

            # 验证 token
            validated_token = self.jwt_auth.get_validated_token(auth_header.split()[1])
            
            # 从 token 中获取用户 uid
            user_uid = validated_token['user_uid']
            try:
                request.user = User.objects.get(uid=user_uid, is_deleted=False)
            except User.DoesNotExist:
                return JsonResponse({'code': 401, 'message': '用户不存在'}, status=401)

        except (InvalidToken, TokenError) as e:
            return JsonResponse({'code': 401, 'message': 'token无效或已过期'}, status=401)

        return self.get_response(request) 
from django import forms
from .models import ApiInfo

class ApiInfoForm(forms.ModelForm):
    class Meta:
        model = ApiInfo
        fields = [
            'env', 
            'of_business', 
            'host', 
            'api_name', 
            'api_path', 
            'req_method', 
            'req_body', 
            'body_type',
            'req_header',    # 添加请求头字段
            'req_params',    # 添加请求参数字段
            'resp_demo',     # 添加响应示例字段
            'extr_value'     # 添加提取值字段
        ]

    def clean_env(self):
        env = self.cleaned_data.get('env')
        if env not in ['TEST', 'PROD']:
            raise forms.ValidationError("环境只能是 TEST 或 PROD")
        return env

    def clean_host(self):
        host = self.cleaned_data.get('host')
        if not host.startswith(('http://', 'https://')):
            raise forms.ValidationError("主机地址必须以 http:// 或 https:// 开头")
        return host

    def clean_api_path(self):
        api_path = self.cleaned_data.get('api_path')
        if not api_path.startswith('/'):
            raise forms.ValidationError("API路径必须以 / 开头")
        return api_path

    def clean_req_body(self):
        req_body = self.cleaned_data.get('req_body')
        body_type = self.cleaned_data.get('body_type')
        
        if body_type == 'JSON' and req_body:
            try:
                import json
                json.loads(req_body)
            except json.JSONDecodeError:
                raise forms.ValidationError("JSON格式不正确")
        return req_body 
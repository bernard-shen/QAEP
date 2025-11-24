from django import forms
from .models import User

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=128)

class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("用户名长度不能小于3位")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("密码长度不能小于6位")
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("两次输入的密码不一致")
        return cleaned_data 
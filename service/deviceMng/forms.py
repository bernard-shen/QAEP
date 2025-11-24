from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_type', 'os_name', 'device_model', 'asset_code', 'owner']

    def check_asset_code(self):
        asset_code = self.cleaned_data.get('asset_code')
        if len(asset_code) < 4:
            raise forms.ValidationError("资产编码长度不能小于4位")
        return asset_code

    def check_device_model(self):
        device_model = self.cleaned_data.get('device_model')
        if len(device_model.strip()) == 0:
            raise forms.ValidationError("设备型号不能为空")
        return device_model 
    
    def check_owner(self):
        device_model = self.cleaned_data.get('owner')
        if len(device_model.strip()) == 0:
            raise forms.ValidationError("所属人不能为空")
        return device_model 
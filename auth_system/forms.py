from django import forms

class RegisterForm(forms.Form):
    phone = forms.CharField(label="手机号码", max_length=11, required=True)
    email = forms.EmailField(label="邮箱", max_length=150, required=True)
    name = forms.CharField(label="姓名", max_length=150, required=True)
    password = forms.CharField(label="密码", max_length=20, required=True)

class LoginForm(forms.Form):
    phone = forms.CharField(label="手机号码", max_length=11, required=True)
    password = forms.CharField(label="密码", max_length=20, required=True)
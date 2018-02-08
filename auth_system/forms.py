from django import forms

class RegisterForm(forms.Form):
    phone = forms.CharField(label="手机号码", max_length=11, required=True)
    email = forms.EmailField(label="邮箱", max_length=150, required=True)
    name = forms.CharField(label="姓名", max_length=150, required=True)
    password = forms.CharField(label="密码", max_length=20, required=True)

class LoginForm(forms.Form):
    phone = forms.CharField(label="手机号码", max_length=11, required=True)
    password = forms.CharField(label="密码", max_length=20, required=True)

SEX = (('F', '男性'), ('M', '女性'))
class InfoForm(forms.Form):
    sex = forms.ChoiceField(choices=SEX, required=False)
    birthday = forms.CharField(label='生日时间', max_length=10, required=False)
    region = forms.CharField(label='地区', max_length=1024, required=False)
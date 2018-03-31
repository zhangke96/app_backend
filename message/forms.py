from django import forms

class friendForm(forms.Form):
    phone=forms.CharField(label='好友手机号')
from django import forms
from django.db import transaction
from .models import UploadFile, UserIcon
from django.core.exceptions import ObjectDoesNotExist
import pdb

class UploadFileForm(forms.Form):
    description = forms.CharField(max_length=1024, required=True)
    file = forms.FileField(required=True)

    def save(self, user):
        if not self.is_valid():
            return False
        cd = self.cleaned_data
        desc = cd['description']
        file = cd['file']
        with transaction.atomic():
            newFile = UploadFile(
                creator = user,
                description = desc,
                filename = file.name,
            )
            newFile.save()
            return True, newFile.id
        return False

class UploadIconForm(forms.Form):
    file = forms.FileField(required=True)   # 上传的头像
    def save(self, user):
        if not self.is_valid():
            return False
        cd = self.cleaned_data
        file = cd['file']
        with transaction.atomic():
            newFile = UploadFile(
                creator=None,  # 设置None不认为是个人文件
                description="User's icon",
                filename=file.name,
            )
            newFile.save()
            try:
                userIcon = user.User_icon # 没有异常代表已经上传了头像
                user.User_icon.file = newFile
                user.User_icon.save()
            except ObjectDoesNotExist:
                UserIcon.objects.create(user=user, file=newFile)
            return True, newFile.id
        return False

from django.db import models
from auth_system.models import MyUser

class UploadFile(models.Model):
    id = models.AutoField('文件id', primary_key=True)
    creator = models.ForeignKey(MyUser, related_name='UploadFile_creator', on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField('文件描述', max_length=1024)
    filename = models.CharField('文件名', max_length=1024)

class UserIcon(models.Model):
    user = models.OneToOneField(MyUser, related_name='User_icon', on_delete=models.SET_NULL, null=True)
    file = models.OneToOneField(UploadFile, related_name='Icon_file', on_delete=models.SET_NULL, null=True)

class Invoice(models.Model):
    id = models.AutoField('发票id', primary_key=True)
    creator = models.ForeignKey(MyUser, related_name='Invoice_creator', on_delete=models.PROTECT, null=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    filename = models.CharField('发票文件名', max_length=1024)

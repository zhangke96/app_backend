from django.db import models
# import os
# from app_backend.settings import BASE_DIR

class vedios(models.Model):
    """
    用来保存上传的文件的信息
    """
    id= models.AutoField(primary_key=True)
    filename = models.CharField(max_length=1000)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=200, null=True)
    document = models.FileField(upload_to='vedioFile/')

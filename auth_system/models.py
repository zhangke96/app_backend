from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class MyUserManager(BaseUserManager):
    pass
    # def create_user(selfself, mobile, email, name, password):
    #     if not mobile or len(mobile) != 11:
    #         raise ValueError('电话错误')
    #     if not email:
    #         raise ValueError('邮箱必须有')
    #     if not name:
    #         raise ValueError('姓名必须有')
    #     if not password:
    #         raise ValueError('密码必须有')


class MyUser(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField("手机号码", max_length=11, unique=True)
    email = models.EmailField("邮箱", max_length=150, unique=True)
    name = models.CharField("姓名", max_length=150, null=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email', 'name']

    objects = MyUserManager()

    def get_all_info(self):
        return {'phone':self.mobile,
                'email':self.email,
                'name':self.name}

    def get_mobile(self):
        return self.mobile

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

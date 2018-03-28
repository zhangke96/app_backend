from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .forms import SEX

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
    friends = models.ManyToManyField(
        'MyUser',
        through='FriendShip',
        through_fields=('user', 'friend')
    )

    objects = MyUserManager()

    def get_all_info(self):
        return {'phone':self.mobile,
                'email':self.email,
                'name':self.name,
                'id': self.id,}

    def get_mobile(self):
        return self.mobile

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

class UserInfo(models.Model):
    user = models.OneToOneField(MyUser, related_name='UserInfo')
    sex = models.CharField(verbose_name='用户性别', choices=SEX, max_length=1, null=True)
    birthday = models.DateField(verbose_name='用户生日', null=True)
    region = models.CharField(verbose_name='用户地区', max_length=1024, null=True)
    update_time = models.DateTimeField(verbose_name='信息更新时间', auto_now=True)

class FriendShip(models.Model):
    """
    用来描述用户之间的好友关系
    """
    user = models.ForeignKey(MyUser)
    friend = models.ForeignKey(MyUser, related_name='all_friends')
    time = models.DateTimeField(auto_now_add=True)
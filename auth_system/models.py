from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .forms import SEX

class MyUserManager(BaseUserManager):
    def create_user(self, mobile, email, name, password=None):
        user = self.model(
            mobile=mobile,
            email=email,
            name=name
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, mobile, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            mobile=mobile,
            email=email,
            name=name,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField("手机号码", max_length=11, unique=True)
    email = models.EmailField("邮箱", max_length=150, unique=True)
    name = models.CharField("姓名", max_length=150, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
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

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_short_name(self):
        # The user is identified by their name
        return self.name

    def get_full_name(self):
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
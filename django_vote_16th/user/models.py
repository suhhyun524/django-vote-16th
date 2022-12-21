from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_id, name, email, part, team, password, is_candidate, **kwargs):
        if not user_id:
            raise ValueError('아이디를 입력해주세요')
        if not name:
            raise ValueError('이름을 입력해주세요')
        if not email:
            raise ValueError('이메일을 입력해주세요')
        if not password:
            raise ValueError('패스워드를 입력해주세요')
        if not part:
            raise ValueError('본인 파트를 선택해주세요(프론트/백)')
        if not team:
            raise ValueError('본인 팀을 선택해주세요')
        if not is_candidate:
            raise ValueError('후보자 참가 여부를 선택해주세요')

        user = self.model(
            user_id=user_id,
            name=name,
            email=email,
            part=part,
            team=team,
            is_candidate=is_candidate,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id=None, name=None, email=None, part=None, team=None, password=None, is_candidate=None, **extra_fields):
        superuser = self.create_user(
            user_id=user_id,
            name=name,
            email=email,
            part=part,
            team=team,
            password=password,
            is_candidate=is_candidate,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True, null=False, blank=False)
    name = models.CharField(max_length=10, null=False, blank=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    part = models.CharField(max_length=30, null=False)
    team = models.CharField(max_length=30)
    is_candidate = models.BooleanField(null=False, default=False)
    is_voted_demo = models.BooleanField(default=False)
    is_voted_partleader = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=300, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    refresh_token = models.CharField(max_length=300, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'name', 'part', 'team', 'is_candidate']

    class Meta:
        db_table = 'user'


from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import re

def password_validator(password):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.06
    작성내용 : 비밀번호 유효성 검증 함수
    업데이트 날짜 :
    '''
    password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
    
    if not re.search(password_regex, str(password)):
        return True
    return False

def password_pattern(password):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.06
    작성내용 : 비밀번호 패턴 유효성 검증 함수
    업데이트 날짜 :
    '''
    password_pattern = r"(.)\1+\1"
    
    if re.search(password_pattern, str(password)):
        return True
    return False


class UserManager(BaseUserManager):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.06
    작성내용 : UserManager 모델
    업데이트 날짜 :
    '''
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("이메일을 입력해주세요!")
        if not name:
            raise ValueError("이름을 입력해주세요!")

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.06
    작성내용 : User 모델
    업데이트 날짜 :
    '''
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(verbose_name="user name", max_length=30,)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
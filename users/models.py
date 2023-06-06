from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import re

# 인자값으로 들어온 문자열이 password_regex에 정의된 조건들을 모두 만족하는지 검사
def password_validator(password):
    password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
    
    if not re.search(password_regex, str(password)):
        return True
    return False

# 인자값으로 들어온 문자열의 문자중 연속해서 3개 이상의 문자가 같은 패턴인지 검사
def password_pattern(password):
    password_pattern = r"(.)\1+\1"
    
    if re.search(password_pattern, str(password)):
        return True
    return False


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
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
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
from rest_framework import serializers
from users.models import User
# from .models import User, password_validator, password_pattern
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignUpSerializer(serializers.ModelSerializer):
    '''
    작성자 : 이주한
    내용 : 회원가입에 필요한 Sign Up Serializer 클래스
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.10
    '''
    re_password = serializers.CharField(
        error_messages={
            "required": "비밀번호 확인은 필수 입력 사항입니다!",
            "blank": "비밀번호 확인은 필수 입력 사항입니다!",
        }
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "re_password",
            "email",
        )
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "email은 필수 입력 사항입니다!",
                    "invalid": "email 형식이 맞지 않습니다. 알맞은 형식의 email을 입력해주세요!",
                    "blank": "email은 필수 입력 사항입니다!",
                }
            },
            "username": {
                "error_messages": {
                    "required": "이름은 필수 입력 사항입니다!",
                    "blank": "이름은 필수 입력 사항입니다!",
                }
            },
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": "비밀번호는 필수 입력 사항입니다!",
                    "blank": "비밀번호는 필수 입력 사항입니다!",
                },
            },
        }

    def validate(self, data):
        password = data.get("password")
        re_password = data.get("re_password")

        if password != re_password:
            raise serializers.ValidationError(
                detail={"password": "비밀번호와 비밀번호 확인이 일치하지 않습니다!"})

        # if password_validator(password):
        #     raise serializers.ValidationError(
        #         detail={"password": "비밀번호는 8자 이상의 영문 대소문자와 숫자, 특수문자를 포함하여야 합니다!"})

        # if password_pattern(password):
        #     raise serializers.ValidationError(
        #         detail={"password": "비밀번호는 연속해서 3자리 이상 동일한 영문,숫자,특수문자 사용이 불가합니다!"})

        return data

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password"]
        validated_data.pop("re_password", None)
        user = User.objects.create(username=username, email=email,)
        user.set_password(password)
        user.save()

        return validated_data


class UserUpdateSerializer(serializers.ModelSerializer):
    '''
    작성자 : 이주한
    내용 : 회원정보 수정에 필요한 UserUpdateSerializer 클래스 입니다.
    최초 작성일 : 2023.06.14
    업데이트 일자 :
    '''
    class Meta:
        model = User
        fields = (
            "email",
        )
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "이메일을 입력해주세요.",
                    "blank": "이메일을 입력해주세요.",
                }
            },
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        return instance


class UpdatePasswordSerializer(serializers.ModelSerializer):
    '''
    작성자 : 이주한
    내용 : 사용자가 로그인한 상태에서 본인 계정의 비밀번호를 수정할 때 사용되는 UpdatePasswordSerializer 입니다.
            로직에는 사용자가 비밀번호를 변경하기 위해 진행해야하는 예외처리 & 유효성 검사들이 있습니다.
            1. 현재 비밀번호를 입력하여 본인임을 인증하는 검사
            2. 현재 비밀번호와 바꿀 비밀번호 끼리의 중복 검사
            3. 비밀번호와 비밀번호 확인 일치 검사
            4. 비밀번호 유효성 검사
            5. 비밀번호의 문자들 중 3자리 이상 동일 문자 유/무 검사
            위의 유효성 검사들 중 4번과 5번은 개발 단계에서 번거로울 수 있으므로 주석 처리해 두었습니다.
    최초 작성일 : 2023.06.15
    업데이트 일자 : 
    '''
    confirm_password = serializers.CharField(
        error_messages={
            "required": "비밀번호를 입력해주세요.",
            "blank": "비밀번호를 입력해주세요.",
        }
    )
    re_password = serializers.CharField(
        error_messages={
            "required": "비밀번호를 입력해주세요.",
            "blank": "비밀번호를 입력해주세요.",
        }
    )

    class Meta:
        model = User
        fields = (
            "password",
            "re_password",
            "confirm_password",
        )
        extra_kwargs = {
            "password": {
                "error_messages": {
                    "required": "비밀번호를 입력해주세요.",
                    "blank": "비밀번호를 입력해주세요.",
                },
            },
        }

    def validate(self, data):
        current_password = self.context.get("request").user.password
        confirm_password = data.get("confirm_password")
        password = data.get("password")
        re_password = data.get("re_password")

        # 현재 비밀번호 예외 처리
        if not check_password(confirm_password, current_password):
            raise serializers.ValidationError(detail={"password": "현재 비밀번호가 일치하지 않습니다."})

        # 현재 비밀번호와 바꿀 비밀번호 비교
        if check_password(password, current_password):
            raise serializers.ValidationError(detail={"password": "현재 사용중인 비밀번호와 동일한 비밀번호는 입력할 수 없습니다."})

        # 비밀번호 일치
        if password != re_password:
            raise serializers.ValidationError(detail={"password": "비밀번호가 일치하지 않습니다."})

        # # 비밀번호 유효성 검사
        # if password_validator(password):
        #     raise serializers.ValidationError(detail={"password": "비밀번호는 8자 이상 16자이하의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다."})

        # # 비밀번호 문자열 동일여부 검사
        # if password_pattern(password):
        #     raise serializers.ValidationError(detail={"password": "비밀번호는 3자리 이상 동일한 영문/사용 사용 불가합니다."})

        return data

    def update(self, instance, validated_data):
        instance.password = validated_data.get("password", instance.password)
        instance.set_password(instance.password)
        instance.save()

        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
    작성자 : 이주한
    내용 : 로그인에 필요한 Custom Token Obtain Pair Serializer 클래스
    최초 작성일 : 2023.06.06
    업데이트 일자 :
    '''
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token["email"] = user.email
        token["is_admin"] = user.is_admin
        return token


class UserSerializer(serializers.ModelSerializer):
    '''
    작성자 : 박지홍
    내용 : 어드민 페이지에서 필요한 유저의 정보를 직렬화 하는 Serializer 클래스
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    '''
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active']

from rest_framework import serializers
from users.models import User
from .models import User, password_validator, password_pattern
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpSerializer(serializers.ModelSerializer):
    '''
    작성자 : 이주한
    내용 : 회원가입에 필요한 Sign Up Serializer 클래스
    최초 작성일 : 2023.06.06
    업데이트 일자 :
    '''
    re_password = serializers.CharField(
        error_messages={
            "required": "비밀번호 확인은 필수 입력 사항입니다!",
            "blank": "비밀번호 확인은 필수 입력 사항입니다!",
            "write_only": True,
        }
    )
    
    class Meta:
        model = User
        fields = (
            "name",
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
            "name": {
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
            raise serializers.ValidationError(detail={"password": "비밀번호와 비밀번호 확인이 일치하지 않습니다!"})

        if password_validator(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 8자 이상의 영문 대소문자와 숫자, 특수문자를 포함하여야 합니다!"})

        if password_pattern(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 연속해서 3자리 이상 동일한 영문,숫자,특수문자 사용이 불가합니다!"})

        return data

    def create(self, validated_data):
        email = validated_data["email"]
        name = validated_data["name"]
        password = validated_data["password"]
        validated_data.pop("re_password", None)
        user = User.objects.create(name=name, email=email,)
        user.set_password(password)
        user.save()

        return validated_data


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
        token['email'] = user.email
        token["is_admin"] = user.is_admin
        return token


class CustomRefreshToken(RefreshToken):
    '''
    작성자 : 이주한
    내용 : 
            1.JWT access token 만료시에 token을 새로고침 하여 새로 발급받지 않고도 
                계속해서 인증된 세션을 유지할 수 있게 해주는 RefreshToken 클래스를 상속받은 CustomRefreshToken 
            2.소셜 로그인시에 access token과 refresh token 발급을 받기 위해 필요한 클래스
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    '''
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['email'] = user.email
        token['is_admin'] = user.is_admin
        return token
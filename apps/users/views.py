from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions


from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from VueShop.settings import APIKEY
from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self, num=6):
        """
        生成六位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(num):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    create:
        用户
    retrieve:
        个人中心
    """
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

    # serializer_class = UserRegSerializer
    def get_serializer_class(self):
        """
        用户详情页需要使用UserDetailSerializer类，serializer
        """
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    # 访问用户详情页需要添加RetrieveModelMixin，此时必须给用户添加权限，否则该用户会访问其他人的个人中心
    # 如果使用permission_classes定义权限，那么会对此ViewSet的所有功能都加上此权限，而注册页我们希望AllowAny。所以我们重写get_permissions方法。
    # permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # get_object对应retrieve方法，这里用来替代获取当前用户的id
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

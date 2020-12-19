from random import Random
from MetisBackend.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.core.cache import cache
from django.contrib.auth import get_user_model
from config.error_code import *
from utils.utils import build_ret_data, render_json

User = get_user_model()


def random_str(random_length=8):
    code_str = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        code_str += chars[random.randint(0, length)]
    return code_str


# 用户注册
class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        req_data = request.data
        username = req_data['username']
        password = req_data['password']
        password_confirm = req_data['passwordConfirm']
        email = req_data['email']
        if password != password_confirm:
            return_dict = build_ret_data(THROW_EXP, '两次输入密码不一致！')
            return render_json(return_dict)
        if User.objects.filter(username=username):
            return_dict = build_ret_data(THROW_EXP, '用户已经存在，请重新选择用户名！')
            return render_json(return_dict)
        try:
            User.objects.create_user(username=username,
                                     password=password,
                                     email=email,
                                     is_active=True)
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


# 更新密码
class UpdatePasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        req_data = request.data
        email = req_data['email']
        verification_code = req_data['verificationCode']
        email_title = "新密码，请妥善保存"
        new_password = random_str()
        email_body = "新密码为：{0}".format(new_password)
        user = User.objects.get(email=email)
        if not user:
            return_dict = build_ret_data(THROW_EXP, '此邮件不存在')
            return render_json(return_dict)
        email_to = [email]
        redis_verification_code = cache.get(email)
        print(verification_code, redis_verification_code)
        if verification_code != redis_verification_code:
            return_dict = build_ret_data(THROW_EXP, '验证码错误')
            return render_json(return_dict)
        try:
            user.set_password(new_password)
            user.save()
            send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, email_to, )
            return_dict = build_ret_data(OP_SUCCESS, str(send_status))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


# 更新邮箱
class UpdateEmailView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        req_data = request.data
        email = req_data['email']
        verification_code = req_data['verificationCode']
        email_title = "新密码，请妥善保存"
        new_password = random_str()
        email_body = "新密码为：{0}".format(new_password)
        user = User.objects.get(email=email)
        if not user:
            return_dict = build_ret_data(THROW_EXP, '此邮件不存在')
            return render_json(return_dict)
        email_to = [email]
        redis_verification_code = cache.get(email)
        print(verification_code, redis_verification_code)
        if verification_code != redis_verification_code:
            return_dict = build_ret_data(THROW_EXP, '验证码错误')
            return render_json(return_dict)
        try:
            user.set_password(new_password)
            user.save()
            send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, email_to, )
            return_dict = build_ret_data(OP_SUCCESS, str(send_status))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


# 发送验证码到邮箱
class ForgetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        req_data = request.data
        email_title = "找回密码"
        random_code = random_str()
        email_body = "验证码为：{0}".format(random_code)
        email = req_data['email']
        if not User.objects.get(email=email):
            return_dict = build_ret_data(THROW_EXP, '此邮件不存在')
            return render_json(return_dict)
        # conn = get_redis_connection('default')
        # conn.set(email, random_code, ex=5)
        cache.set(email, random_code)
        email_to = [email]
        try:
            send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, email_to, )
            return_dict = build_ret_data(OP_SUCCESS, str(send_status))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


# 发送新密码到邮箱
class ResetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        req_data = request.data
        email = req_data['email']
        verification_code = req_data['verificationCode']
        email_title = "新密码，请妥善保存"
        new_password = random_str()
        email_body = "新密码为：{0}".format(new_password)
        user = User.objects.get(email=email)
        if not user:
            return_dict = build_ret_data(THROW_EXP, '此邮件不存在')
            return render_json(return_dict)
        email_to = [email]
        redis_verification_code = cache.get(email)
        print(verification_code, redis_verification_code)
        if verification_code != redis_verification_code:
            return_dict = build_ret_data(THROW_EXP, '验证码错误')
            return render_json(return_dict)
        try:
            user.set_password(new_password)
            user.save()
            send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, email_to, )
            return_dict = build_ret_data(OP_SUCCESS, str(send_status))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)
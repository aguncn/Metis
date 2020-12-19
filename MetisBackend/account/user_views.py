from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from config.error_code import *
from utils.utils import build_ret_data, render_json

User = get_user_model()


# 用户注册
class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        req_data = request.data
        username = req_data['username']
        password = req_data['password']
        password_confirm = req_data['passwordConfirm']
        if password != password_confirm:
            return_dict = build_ret_data(THROW_EXP, '两次输入密码不一致！')
            return render_json(return_dict)
        if User.objects.filter(username=username):
            return_dict = build_ret_data(THROW_EXP, '用户已经存在，请重新选择用户名！')
            return render_json(return_dict)
        try:
            User.objects.create_user(username=username,
                                     password=password,
                                     is_active=True)
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)
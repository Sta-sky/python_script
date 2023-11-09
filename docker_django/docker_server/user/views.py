import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from user.models import UserInfo


def get_user(request):
    data = {"code": 0, "msg": "成功"}
    body_data = json.loads(request.body.decode('utf-8'))
    curr_name = body_data.get("name", None)
    if not curr_name:
        data["code"] = 1
        data["msg"] = "用户姓名为空！"
    else:
        try:
            user_obj = UserInfo.objects.get(name=curr_name)
            user_name = user_obj.name
        except Exception:
            user_name = None
        data['msg'] = user_name
    return JsonResponse(data)


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = {"code": 0, "msg": "成功"}
        body_data = json.loads(request.body.decode('utf-8'))

        lookup_condition = {
            'name': ''  # 根据其他条件查找记录（例如根据用户名）
        }
        curr_name = body_data.get("name", None)
        if not curr_name:
            data["code"] = 1
            data["msg"] = "用户姓名为空！"
        else:
            lookup_condition["name"] = curr_name
            user_obj, created = UserInfo.objects.update_or_create(defaults=body_data, **lookup_condition)
            data["msg"] = "用户创建成功" if created else "用户更新成功"

        return JsonResponse(data)



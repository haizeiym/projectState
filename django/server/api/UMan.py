from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.hashers import make_password
from server.models import UMModel
import json
import logging


class UMan:
    @staticmethod
    def get(request=None, user_id=None):
        """获取用户信息"""
        try:
            if user_id is None and request is not None:
                user_id = request.resolver_match.kwargs.get("user_id")

            user = UMModel.objects.get(id=user_id)
            return JsonResponse(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "project_id": user.project_id,
                    "is_active": user.is_active,
                    "is_staff": user.is_staff,
                    "date_joined": user.date_joined.isoformat(),
                    "last_login": (
                        user.last_login.isoformat() if user.last_login else None
                    ),
                }
            )

        except UMModel.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            logging.error(f"Error in get user: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def create(request):
        """创建新用户"""
        try:
            if request.method != "POST":
                return JsonResponse({"error": "Method not allowed"}, status=405)

            with transaction.atomic():
                data = json.loads(request.body)

                # 检查必要字段
                required_fields = ["username", "password", "project_id"]
                for field in required_fields:
                    if field not in data:
                        return JsonResponse(
                            {"error": f"Missing required field: {field}"}, status=400
                        )

                # 检查用户名是否已存在
                if UMModel.objects.filter(username=data["username"]).exists():
                    return JsonResponse(
                        {"error": "Username already exists"}, status=400
                    )

                # 创建用户
                user = UMModel(
                    username=data["username"],
                    password=make_password(data["password"]),  # 加密密码
                    email=data.get("email", ""),
                    project_id=data["project_id"],
                    is_active=data.get("is_active", True),
                    is_staff=data.get("is_staff", False),
                )
                user.save()

                return JsonResponse(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "project_id": user.project_id,
                        "is_active": user.is_active,
                        "is_staff": user.is_staff,
                        "date_joined": user.date_joined.isoformat(),
                    },
                    status=201,
                )

        except Exception as e:
            logging.error(f"Error in create user: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def update(request, user_id):
        """更新用户信息"""
        try:
            if request.method != "POST":
                return JsonResponse({"error": "Method not allowed"}, status=405)

            user = UMModel.objects.get(id=user_id)
            data = json.loads(request.body)

            with transaction.atomic():
                # 更新可修改的字段
                if "username" in data and data["username"] != user.username:
                    if UMModel.objects.filter(username=data["username"]).exists():
                        return JsonResponse(
                            {"error": "Username already exists"}, status=400
                        )
                    user.username = data["username"]

                if "password" in data:
                    user.password = make_password(data["password"])

                if "email" in data:
                    user.email = data["email"]

                if "project_id" in data:
                    user.project_id = data["project_id"]

                if "is_active" in data:
                    user.is_active = data["is_active"]

                if "is_staff" in data:
                    user.is_staff = data["is_staff"]

                user.save()

                return JsonResponse(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "project_id": user.project_id,
                        "is_active": user.is_active,
                        "is_staff": user.is_staff,
                        "date_joined": user.date_joined.isoformat(),
                        "last_login": (
                            user.last_login.isoformat() if user.last_login else None
                        ),
                    }
                )

        except UMModel.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            logging.error(f"Error in update user: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def delete(request, user_id):
        """删除用户"""
        try:
            if request.method != "DELETE":
                return JsonResponse({"error": "Method not allowed"}, status=405)

            user = UMModel.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"status": "success"})

        except UMModel.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            logging.error(f"Error in delete user: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def list(request):
        """获取用户列表"""
        try:
            users = UMModel.objects.all()
            user_list = []
            for user in users:
                user_list.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "project_id": user.project_id,
                        "is_active": user.is_active,
                        "is_staff": user.is_staff,
                        "date_joined": user.date_joined.isoformat(),
                        "last_login": (
                            user.last_login.isoformat() if user.last_login else None
                        ),
                    }
                )
            return JsonResponse(user_list, safe=False)

        except Exception as e:
            logging.error(f"Error in list users: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

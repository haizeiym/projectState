from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import random
import string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import logging
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

logger = logging.getLogger(__name__)
User = get_user_model()  # 获取当前项目配置的用户模型


@ensure_csrf_cookie
def get_csrf_token(request):
    """获取 CSRF Token"""
    return JsonResponse({"csrfToken": get_token(request)})


@require_http_methods(["POST"])
def login_view(request):
    """用户登录"""
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        captcha = data.get("captcha")

        if not username or not password or not captcha:
            return JsonResponse(
                {"error": "Please provide username, password and captcha"}, status=400
            )

        if not verify_captcha(request, captcha):
            return JsonResponse({"error": "Invalid captcha"}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            print(f"User ID: {user.id}")
            if user.is_active:
                login(request, user)
                return JsonResponse(
                    {
                        "id": user.id,
                        "username": user.username,
                        "project_ids": user.project_ids,
                        "is_superuser": user.is_superuser,
                    }
                )
            else:
                return JsonResponse({"error": "Account is disabled"}, status=403)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@api_view(["POST"])
def register(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        captcha = request.data.get("captcha")

        # 验证必填字段
        if not username or not password or not captcha:
            return Response({"error": "用户名、密码和验证码都是必填项"}, status=400)

        # 验证用户名长度
        if len(username) < 3:
            return Response({"error": "用户名长度至少为3个字符"}, status=400)

        # 验证密码长度
        if len(password) < 6:
            return Response({"error": "密码长度至少为6个字符"}, status=400)

        if not verify_captcha(request, captcha):
            return Response({"error": "验证码错误"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "用户名已存在"}, status=400)

        # 使用 create_user 方法创建用户
        user = User.objects.create_user(
            username=username, password=password, project_ids="", is_active=True
        )

        # 注册成功后自动登录
        login(request, user)

        # 确保会话中存储了正确的用户 ID
        request.session["_auth_user_id"] = user.id
        request.session.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "message": "注册成功",
                "is_active": user.is_active,
            },
            status=201,
        )

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return Response({"error": str(e)}, status=500)


@require_http_methods(["POST"])
def logout_view(request):
    """用户登出"""
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})


@require_http_methods(["GET"])
def get_user_info(request):
    """获取用户信息"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    return JsonResponse(
        {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "project_ids": request.user.project_ids,
            "is_active": request.user.is_active,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        }
    )


@require_http_methods(["GET"])
def get_captcha(request):
    """生成验证码"""
    # 设置响应头，禁止缓存
    response = HttpResponse(content_type="image/png")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    response["Access-Control-Allow-Origin"] = "*"  # 允许跨域访问验证码
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"

    # 生成随机字符串
    chars = string.ascii_letters + string.digits
    code = "".join(random.choices(chars, k=4))

    # 将验证码存入 session
    request.session["captcha"] = code.lower()
    request.session.modified = True  # 确保 session 被保存

    # 创建图片
    width = 120
    height = 48
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 获取字体文件路径
    font_path = os.path.join(os.path.dirname(__file__), "../static/fonts/arial.ttf")
    try:
        font = ImageFont.truetype(font_path, 32)
    except:
        font = ImageFont.load_default()

    # 添加干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(200, 200, 200))

    # 添加验证码文字
    for i, char in enumerate(code):
        x = 24 * i + 20
        y = random.randint(8, 16)
        draw.text((x, y), char, fill=(0, 0, 0), font=font)

    # 保存图片
    buffer = BytesIO()
    image.save(buffer, "PNG")
    response.write(buffer.getvalue())
    return response


def verify_captcha(request, captcha):
    """验证验证码"""
    stored_captcha = request.session.get("captcha", "").lower()
    return stored_captcha == captcha.lower()


class AuthView:
    @staticmethod
    def update_projects(request, user_id):
        """更新用户的项目ID列表"""
        if request.method != "PUT":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            user = User.objects.get(id=user_id)
            data = json.loads(request.body)
            project_ids = data.get("project_ids", [])

            # 更新用户的项目ID列表
            user.project_ids = ",".join(map(str, project_ids))
            user.save()

            return JsonResponse({"message": "Projects updated successfully"})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    def login(request):
        """用户登录"""
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            captcha = data.get("captcha")

            if not username or not password or not captcha:
                return JsonResponse(
                    {"error": "Please provide username, password and captcha"},
                    status=400,
                )

            if not verify_captcha(request, captcha):
                return JsonResponse({"error": "Invalid captcha"}, status=400)

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse(
                        {
                            "id": user.id,
                            "username": user.username,
                            "project_ids": user.project_ids,
                            "is_superuser": user.is_superuser,
                        }
                    )
                else:
                    return JsonResponse({"error": "Account is disabled"}, status=403)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @staticmethod
    def logout(request):
        """用户登出"""
        logout(request)
        return JsonResponse({"message": "Logged out successfully"})

    @staticmethod
    def info(request):
        """获取用户信息"""
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Not authenticated"}, status=401)

        return JsonResponse(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "project_ids": request.user.project_ids,
                "is_active": request.user.is_active,
                "is_staff": request.user.is_staff,
                "is_superuser": request.user.is_superuser,
            }
        )

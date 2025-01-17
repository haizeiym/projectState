from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json
import random
import string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import logging
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

logger = logging.getLogger(__name__)


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


@api_view(["POST"])
def register(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        captcha = request.data.get("captcha")

        if not verify_captcha(request, captcha):
            return Response({"error": "验证码错误"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "用户名已存在"}, status=400)

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        return Response(
            {"id": user.id, "username": user.username},
            status=201,
        )

    except Exception as e:
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
    width = 90
    height = 40
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 获取字体文件路径
    font_path = os.path.join(os.path.dirname(__file__), "../static/fonts/arial.ttf")
    try:
        font = ImageFont.truetype(font_path, 28)
    except:
        font = ImageFont.load_default()

    # 添加干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(169, 169, 169))

    # 添加验证码文字
    for i, char in enumerate(code):
        x = 18 * i + 15
        y = random.randint(5, 12)
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

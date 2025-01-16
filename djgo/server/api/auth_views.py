from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from server.models import UMModel
import json
import random
import string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import logging

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
                        "email": user.email,
                        "project_id": user.project_id,
                    }
                )
            else:
                return JsonResponse({"error": "Account is disabled"}, status=403)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_http_methods(["POST"])
@ensure_csrf_cookie
def register_view(request):
    """用户注册"""
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email", "")  # 设置默认值
        project_id = data.get("project_id")
        captcha = data.get("captcha")

        logger.info(f"Registering user: {username}, project_id: {project_id}")

        if not username or not password or not project_id or not captcha:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if not verify_captcha(request, captcha):
            return JsonResponse({"error": "Invalid captcha"}, status=400)

        if UMModel.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        try:
            user = UMModel.objects.create_user(
                username=username, password=password, email=email, project_id=project_id
            )
            logger.info(f"User created successfully: {user.id}")

            return JsonResponse(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "project_id": user.project_id,
                },
                status=201,
            )
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return JsonResponse({"error": f"Error creating user: {str(e)}"}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


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
            "project_id": request.user.project_id,
            "is_active": request.user.is_active,
            "is_staff": request.user.is_staff,
        }
    )


@require_http_methods(["GET"])
def get_captcha(request):
    """生成验证码"""
    # 生成随机字符串
    chars = string.ascii_letters + string.digits
    code = "".join(random.choices(chars, k=4))

    # 将验证码存入 session
    request.session["captcha"] = code.lower()

    # 创建图片
    width = 100
    height = 40
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)

    # 添加干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill="gray")

    # 添加验证码文字
    for i, char in enumerate(code):
        x = 20 * i + 15
        y = random.randint(5, 15)
        draw.text((x, y), char, fill="black")

    # 保存图片
    buffer = BytesIO()
    image.save(buffer, "PNG")

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def verify_captcha(request, captcha):
    """验证验证码"""
    stored_captcha = request.session.get("captcha", "").lower()
    return stored_captcha == captcha.lower()

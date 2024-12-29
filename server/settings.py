# Django 基本设置
SECRET_KEY = "django-insecure-your-secret-key-here"  # 在生产环境中应该使用环境变量存储

# 调试模式
DEBUG = True

# 允许的主机
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "server",  # 添加你的应用
    "corsheaders",
]

# 中间件配置
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 需要放在最前面
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "nodes",
        "CLIENT": {
            "host": "localhost",
            "port": 27017,
            "username": "root",
            "password": "root",
        },
    }
}

# 国际化
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 静态文件设置
STATIC_URL = "static/"

# 默认主键类型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = []

# CORS 设置
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vue 开发服务器地址
]
CORS_ALLOW_CREDENTIALS = True

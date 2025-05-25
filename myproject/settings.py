from pathlib import Path
import os
from decouple import config
from dj_database_url import parse as dburl
import environ

# プロジェクトのベースディレクトリを設定
BASE_DIR = Path(__file__).resolve().parent.parent

# 環境変数の読み込み
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# セキュリティキー（本番環境では環境変数で管理を推奨）
SECRET_KEY = 'django-insecure-o2d_7ozqnd1j_2_r5!+@r$&khg7sk&n+_@-0%&t!48zix7&x!$'

# デバッグ設定（本番ではFalseにする）
DEBUG = True

# ALLOWED_HOSTSの設定
ALLOWED_HOSTS = ['heart-libbot.onrender.com', 'localhost', '127.0.0.1']

# CSRF対応（Django 4.x以降で必要）
CSRF_TRUSTED_ORIGINS = ['https://heart-libbot.onrender.com']

# アプリケーション定義
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'diary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← 修正済み
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# データベース設定（自動でSQLite→PostgreSQL切替）
default_dburl = "sqlite:///" + str(BASE_DIR / "db.sqlite3")
DATABASES = {
    'default': config("DATABASE_URL", default=default_dburl, cast=dburl)
}

# パスワードバリデーション
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国際化
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# 静的ファイル
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# デフォルトのプライマリキー
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 環境変数でスーパーユーザー情報
SUPERUSER_NAME = env("SUPERUSER_NAME", default="admin")
SUPERUSER_EMAIL = env("SUPERUSER_EMAIL", default="admin@example.com")
SUPERUSER_PASSWORD = env("SUPERUSER_PASSWORD", default="password")

from pathlib import Path

# Caminho base do projeto (onde está o manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
#  Configurações básicas
# =========================

# Chave secreta para criptografia interna
SECRET_KEY = "django-insecure-kg6j-*-dhz-j9s2mqv1a$r^4*huz0p&2^5h&0@5u2!0!0y)$0$"

# Modo de desenvolvimento (deixe False em produção)
DEBUG = False

# Domínios autorizados a acessar o sistema
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

# =========================
# Aplicativos instalados
# =========================

INSTALLED_APPS = [
    # Apps nativos do Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "widget_tweaks",

    # App criado no projetofrom pathlib import Path
    #
    # # Caminho base do projeto (onde está o manage.py)
    # BASE_DIR = Path(__file__).resolve().parent.parent
    #
    # # =========================
    # #  Configurações básicas
    # # =========================
    #
    # # Chave secreta para criptografia interna
    # SECRET_KEY = "django-insecure-kg6j-*-dhz-j9s2mqv1a$r^4*huz0p&2^5h&0@5u2!0!0y)$0$"
    #
    # # Modo de desenvolvimento (deixe False em produção)
    # DEBUG = True
    #
    # # Domínios autorizados a acessar o sistema
    # ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'victoracioly.pythonanywhere.com']
    #
    # # =========================
    # # Aplicativos instalados
    # # =========================
    #
    # INSTALLED_APPS = [
    #     # Apps nativos do Django
    #     "django.contrib.admin",
    #     "django.contrib.auth",
    #     "django.contrib.contenttypes",
    #     "django.contrib.sessions",
    #     "django.contrib.messages",
    #     "django.contrib.staticfiles",
    #     "django_extensions",
    #     "rest_framework",
    #
    #     # App criado no projeto
    #     "gestaodeatas",
    #     "users",
    #     "monitoramento_pncp",
    #     "dispositivos_medicos_anvisa",
    #     "core", # A idéia aqui é que seja um app que tenha informacoes tranversais que se aplique a vários sistemas, tipo o sidebar do html
    # ]
    #
    # # =========================
    # # Middlewares (interceptadores de requisições)
    # # =========================
    #
    # MIDDLEWARE = [
    #     "django.middleware.security.SecurityMiddleware",
    #     "django.contrib.sessions.middleware.SessionMiddleware",
    #     "django.middleware.common.CommonMiddleware",
    #     "django.middleware.csrf.CsrfViewMiddleware",
    #     "django.contrib.auth.middleware.AuthenticationMiddleware",
    #     "django.contrib.messages.middleware.MessageMiddleware",
    #     "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # ]
    #
    # # =========================
    # # Configuração de rotas e templates
    # # =========================
    #
    # # Arquivo principal de URLs
    # ROOT_URLCONF = "aprendendopython.urls"
    #
    # # Configurações de templates HTML
    # TEMPLATES = [
    #     {
    #         "BACKEND": "django.template.backends.django.DjangoTemplates",
    #         "DIRS": [BASE_DIR / "core/templates"],  # diretórios adicionais de templates
    #         "APP_DIRS": True,  # busca em pastas templates de apps
    #         "OPTIONS": {
    #             "context_processors": [
    #                 "django.template.context_processors.request",
    #                 "django.contrib.auth.context_processors.auth",
    #                 "django.contrib.messages.context_processors.messages",
    #             ],
    #         },
    #     },
    # ]
    #
    # # Ponto de entrada para servidores WSGI (ex: Gunicorn)
    # WSGI_APPLICATION = "aprendendopython.wsgi.application"
    #
    # # =========================
    # # Banco de dados
    # # =========================
    #
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.sqlite3",
    #         "NAME": BASE_DIR / "db.sqlite3",
    #     }
    # }
    #
    # # =========================
    # #  Validação de senhas
    # # =========================
    #
    # AUTH_PASSWORD_VALIDATORS = [
    #     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    #     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    #     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    #     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    # ]
    #
    # # =========================
    # #  Internacionalização
    # # =========================
    #
    # # Idioma padrão
    # LANGUAGE_CODE = "en-us"
    #
    # # Fuso horário
    # TIME_ZONE = "UTC"
    #
    # USE_I18N = True
    # USE_TZ = True
    #
    # # =========================
    # #  Arquivos estáticos
    # # =========================
    #
    # # Caminho onde os arquivos estáticos serão coletados
    # STATIC_ROOT = BASE_DIR / "staticfiles"
    #
    # # URL para acessar os arquivos estáticos
    # STATIC_URL = "/static/"
    #
    # # =========================
    # # Chave primária padrão
    # # =========================
    #
    # # Define o tipo de chave primária padrão como BigAutoField (inteiro grande)
    # DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    "gestaodeatas",
    "users",
    "monitoramento_pncp",
    "dispositivos_medicos_anvisa",
    "core", # A idéia aqui é que seja um app que tenha informacoes tranversais que se aplique a vários sistemas, tipo o sidebar do html
]

# =========================
# Middlewares (interceptadores de requisições)
# =========================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================
# Configuração de rotas e templates
# =========================

# Arquivo principal de URLs
ROOT_URLCONF = "aprendendopython.urls"

# Configurações de templates HTML
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core/templates"],  # diretórios adicionais de templates
        "APP_DIRS": True,  # busca em pastas templates de apps
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Ponto de entrada para servidores WSGI (ex: Gunicorn)
WSGI_APPLICATION = "aprendendopython.wsgi.application"

# =========================
# Banco de dados
# =========================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# =========================
#  Validação de senhas
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
#  Internacionalização
# =========================

# Idioma padrão
LANGUAGE_CODE = "en-us"

# Fuso horário
TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True

# =========================
#  Arquivos estáticos
# =========================

# Caminho onde os arquivos estáticos serão coletados
STATIC_ROOT = BASE_DIR / "staticfiles"

# URL para acessar os arquivos estáticos
STATIC_URL = "/static/"

# =========================
# Chave primária padrão
# =========================

# Define o tipo de chave primária padrão como BigAutoField (inteiro grande)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
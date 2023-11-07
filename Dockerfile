FROM python:3.8


ENV DJANGO__SECRET_KEY="????????"
ENV DJANGO__HOSTNAME="http://localhost:8000"


# =============================================================
# 아래의 주석을 해제하여 개발 모드에서 서버 구동
# =============================================================
# ENV DJANGO__DEBUG=true


# =============================================================
# 아래의 주석을 해제하여 외부 DB 사용.
# DB 설정을 따로 하지 않으면 config/settings.py에서
# sqlite3를 사용한다.
# =============================================================
# ENV DJANGO__DATABASE_ENGINE="django.db.backends.mysql"
# ENV DJANGO__DATABASE_NAME=""
# ENV DJANGO__DATABASE_USER=""
# ENV DJANGO__DATABASE_PASSWORD=""
# ENV DJANGO__DATABASE_HOST=""
# ENV DJANGO__DATABASE_PORT=3306


# =============================================================
# 이메일 인증에 사용할 이메일 서비스 정보 입력 (필수)
# =============================================================
ENV DJANGO__EMAIL_HOST=""
ENV DJANGO__EMAIL_HOST_USER=""
ENV DJANGO__EMAIL_HOST_PASSWORD=""
ENV DJANGO__DEFAULT_FROM_MAIL=""
ENV DJANGO__EMAIL_PORT=587
ENV DJANGO__EMAIL_USE_TLS=true


COPY . .


# Python 의존성 설치
COPY requirements.txt ./
RUN pip install -r requirements.txt


# Django 데이터 베이스 구축
RUN python manage.py makemigrations
RUN python manage.py migrate


# HTTPS 통신을 위한 세팅
RUN echo "KR\nSeoul\nJongRo\nLikelion-Univ.\nLogged.me\nDjango-server\nhepheir@gmail.com" > django.cert.details
RUN openssl genrsa 2048 > django.key
RUN openssl req -new -x509 -nodes -sha256 -days 365 -key django.key > django.cert < django.cert.details


EXPOSE 443
ENTRYPOINT ["python", "manage.py", "runsslserver", "--certificate", "/django.cert", "--key", "/django.key", "0:443"]

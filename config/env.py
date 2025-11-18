"""
설정에 필요한 값 중 환경변수에서 가져오는 값들만 모아놓은 모듈.
"""

import os

# 사용자 비밀번호 암호화에 사용되는 솔트 값.
SECRET_KEY = os.environ.get('SECRET_KEY')

# 디버그 모드 활성화 여부.
# 활성화 시, 오류 메시지와 환경변수가 노출되므로 프로덕션에서는 절대 True로 설정하지 말 것.
DEBUG = bool(os.environ.get('DEBUG', False))

# 외부에서 서버에 액세스하기위해 사용하는 도메인 주소.
HOSTNAME = os.environ.get('HOSTNAME')

# 회원가입 로직에서 이메일 인증 발송에 필요한 계정 정보.
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# 데이터베이스 설정
DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_USER = os.environ.get('DATABASE_USER', None)
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', None)
DATABASE_HOST = os.environ.get('DATABASE_HOST', None)
DATABASE_PORT = os.environ.get('DATABASE_PORT', None)

FROM python:3.13-slim

# .pyc 파일을 만들지 않고, 로그를 버퍼 없이 바로 출력한다.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 의존성을 먼저 설치해 두면 코드만 바뀌었을 때 이 단계는 캐시를 재사용한다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# root가 아닌 일반 사용자로 실행한다. 앱이 뚫려도 컨테이너 안 권한이 작다.
RUN useradd --create-home selfspar
USER selfspar

EXPOSE 8000

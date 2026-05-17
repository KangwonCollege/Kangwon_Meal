FROM python:3.12-slim

WORKDIR /srv/app

COPY requirements.txt .

# RUN apt-get update && apt-get install -y --no-install-recommends \
#         gcc \
#         libffi-dev \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
#     && apt-get purge -y gcc libffi-dev \
#     && apt-get autoremove -y \

COPY . .

EXPOSE 8000

# Gunicorn이 프로세스를 관리하고, UvicornWorker가 ASGI(FastAPI)를 처리
CMD ["gunicorn", "app:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120"]

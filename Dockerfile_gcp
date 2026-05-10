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

EXPOSE 8080

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"]

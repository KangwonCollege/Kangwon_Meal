# Kind 실습: Nginx → Gunicorn → FastAPI → MySQL

## 전체 구성도

```
[브라우저/curl]
      |
      | :8080 (호스트 PC)
      v
[Kind 노드] :30080 (NodePort)
      |
      v
[Nginx Pod] :80  ─── ClusterIP ───>  [FastAPI Pod x2] :8000  ─── ClusterIP ───>  [MySQL Pod] :3306
  (리버스 프록시)                        (Gunicorn + ASGI)                              (데이터베이스)
```

## 실습 순서

### 1. Kind 클러스터 생성

```bash
kind create cluster --config kind-config.yaml
```

### 2. FastAPI 이미지 빌드 & Kind에 로드

```bash
# 프로젝트 루트에서 실행
docker build -t kangwon-meal:latest .

# Kind 클러스터 내부로 이미지 전달 (레지스트리 없이 사용)
kind load docker-image kangwon-meal:latest --name kangwon-meal
```

### 3. 리소스 순서대로 적용

```bash
kubectl apply -f 01-namespace.yaml
kubectl apply -f 02-mysql-secret.yaml
kubectl apply -f 03-mysql-pvc.yaml
kubectl apply -f 04-mysql.yaml

# MySQL이 Ready 상태가 될 때까지 대기
kubectl wait --for=condition=ready pod -l app=mysql -n kangwon-meal --timeout=120s

kubectl apply -f 05-fastapi.yaml
kubectl apply -f 06-nginx-configmap.yaml
kubectl apply -f 07-nginx.yaml
```

### 4. 상태 확인

```bash
# 모든 파드 상태 확인
kubectl get pods -n kangwon-meal

# 서비스 목록 확인
kubectl get services -n kangwon-meal

# 특정 파드 로그 보기
kubectl logs -l app=fastapi -n kangwon-meal
kubectl logs -l app=nginx -n kangwon-meal
```

### 5. 접속 테스트

```bash
# API 문서 접속
curl http://localhost:8080/docs

# 브라우저에서 http://localhost:8080/docs
```

### 6. 실습 종료

```bash
kind delete cluster --name kangwon-meal
```

## 파일 목록

| 파일 | 리소스 종류 | 설명 |
|------|-------------|------|
| `kind-config.yaml` | Kind 설정 | 포트 포워딩 설정 (호스트 8080 → 노드 30080) |
| `01-namespace.yaml` | Namespace | 리소스 격리용 네임스페이스 |
| `02-mysql-secret.yaml` | Secret | DB 인증 정보 (암호화 저장) |
| `03-mysql-pvc.yaml` | PersistentVolumeClaim | MySQL 데이터 영구 저장소 |
| `04-mysql.yaml` | Deployment + Service | MySQL 파드 + ClusterIP 서비스 |
| `05-fastapi.yaml` | Deployment + Service | Gunicorn/FastAPI 파드 x2 + ClusterIP 서비스 |
| `06-nginx-configmap.yaml` | ConfigMap | Nginx 리버스 프록시 설정 파일 |
| `07-nginx.yaml` | Deployment + Service | Nginx 파드 + NodePort 서비스 |

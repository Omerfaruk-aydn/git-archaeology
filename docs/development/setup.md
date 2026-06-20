# Geliştirme Ortamı Kurulumu

## Gereksinimler

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+
- Git

## Kurulum

### 1. Depoyu Klonla

```bash
git clone https://github.com/username/git-archaeology.git
cd git-archaeology
```

### 2. Backend Kurulumu

```bash
cd backend

# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Ortam değişkenlerini ayarla
cp ../.env.example ../.env
# .env dosyasını düzenle

# Veritabanı migrasyonlarını uygula
alembic upgrade head

# Backend'i başlat
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Kurulumu

```bash
cd frontend

# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm run dev
```

### 4. Redis Kurulumu (Opsiyonel)

```bash
# Docker ile
docker run -d -p 6379:6379 redis:7-alpine

# Veya yerel kurulum
# Windows: Chocolatey ile
choco install redis-64

# Linux
sudo apt install redis-server
```

## Geliştirme Akışı

1. Backend: http://localhost:8000
2. Frontend: http://localhost:5173
3. API Dokümantasyonu: http://localhost:8000/docs

## Kod Standartları

- Python: PEP 8, black formatting
- TypeScript: ESLint + Prettier
- Commit mesajları: Conventional Commits formatı
- Branch isimleri: `feature/`, `bugfix/`, `hotfix/` prefix

## Testler

```bash
# Backend testleri
cd backend
pytest -v

# Frontend testleri
cd frontend
npm test

# Coverage
pytest --cov=app --cov-report=html
```

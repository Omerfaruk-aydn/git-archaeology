# Docker Deployment

## Gereksinimler

- Docker 24.0+
- Docker Compose v2.20+

## Production Deployment

```bash
# .env dosyasını oluştur
cp .env.example .env

#编辑 .env dosyası
nano .env

# Servisleri başlat
docker compose up -d

# Logları izle
docker compose logs -f
```

## Development Deployment

```bash
# Development modunda başlat
docker compose -f docker-compose.dev.yml up -d

# Backend hot reload
docker compose -f docker-compose.dev.yml logs -f backend
```

## Servisler

| Servis | Port | Açıklama |
|--------|------|----------|
| backend | 8000 | FastAPI uygulaması |
| frontend | 3000 | React uygulaması |
| db | 5432 | PostgreSQL |
| redis | 6379 | Redis cache |
| worker | - | Celery worker |

## Veritabanı Migrasyonları

```bash
# Migrasyonları uygula
docker compose exec backend alembic upgrade head

# Yeni migrasyon oluştur
docker compose exec backend alembic revision --autogenerate -m "migration name"
```

## Backup

```bash
# PostgreSQL backup
docker compose exec db pg_dump -U postgres gitarchaeology > backup.sql

# Geri yükle
docker compose exec -T db psql -U postgres gitarchaeology < backup.sql
```

## Sorun Giderme

```bash
# Servis durumlarını kontrol et
docker compose ps

# Container loglarını görüntüle
docker compose logs backend

# Container'a gir
docker compose exec backend bash

# Veritabanına bağlan
docker compose exec db psql -U postgres gitarchaeology
```

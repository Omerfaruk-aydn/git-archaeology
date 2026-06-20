# API Dokümantasyonu

## Giriş

Git Arkeoloji Aracı API'si, Git depolarını analiz etmek ve raporlar oluşturmak için RESTful bir arayüz sunar.

## Base URL

```
http://localhost:8000/api/v1
```

## Kimlik Doğrulama

Tüm API istekleri Bearer token kimlik doğrulaması gerektirir.

```http
Authorization: Bearer <token>
```

Token almak için:
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

## Endpoint'ler

### Depo Yönetimi

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | /repositories | Tüm depoları listele |
| POST | /repositories | Yeni depo oluştur |
| GET | /repositories/{id} | Depo detayını getir |
| PUT | /repositories/{id} | Depoyu güncelle |
| DELETE | /repositories/{id} | Depoyu sil |

### Analiz

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | /analyses | Analiz başlat |
| GET | /analyses | Analizleri listele |
| GET | /analyses/{id} | Analiz detayını getir |
| DELETE | /analyses/{id} | Analizi sil |

### Commit'ler

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | /commits | Commit'leri listele |
| GET | /commits/{id} | Commit detayını getir |

### Raporlar

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | /reports | Rapor oluştur |
| GET | /reports | Raporları listele |
| GET | /reports/{id} | Rapor detayını getir |
| GET | /reports/{id}/download | Raporu indir |

## Hata Kodları

| Kod | Açıklama |
|-----|----------|
| 400 | Geçersiz istek |
| 401 | Yetkisiz erişim |
| 404 | Bulunamadı |
| 429 | Çok fazla istek |
| 500 | Sunucu hatası |

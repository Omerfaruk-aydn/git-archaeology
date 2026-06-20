# Mimari Genel Bakış

## Sistem Mimarisi

Git Arkeoloji Aracı, three-tier mimari ile tasarlanmıştır:

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Dashboard │  │ Analiz   │  │ Rapor    │  │ Ayarlar │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │ REST API
┌───────────────────────┴─────────────────────────────────┐
│                  Backend (FastAPI)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Repo     │  │ Analiz   │  │ Rapor    │  │ Auth    │ │
│  │ Manager  │  │ Engine   │  │ Builder  │  │ Service │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Git      │  │ LLM      │  │ Queue    │              │
│  │ Service  │  │ Service  │  │ Worker   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────┴─────────────────────────────────┐
│                    Data Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │PostgreSQL│  │  Redis   │  │  Git     │              │
│  │          │  │          │  │  Repos   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

## Teknoloji Seçimleri

| Katman | Teknoloji | Sebep |
|--------|-----------|-------|
| Backend | Python 3.11+ / FastAPI | Yüksek performans, async support |
| Veritabanı | PostgreSQL 16 + SQLAlchemy 2.0 | JSONB desteği,全文 arama |
| Cache | Redis 7 | Analiz sonuçlarını cacheleme |
| Celery | Celery 5 + Redis broker | Arka plan analiz jobları |
| Frontend | React 18 + TypeScript + Vite | Type safety, hızlı geliştirme |
| UI | Tailwind CSS | Utility-first, erişilebilir |

## Veri Akışı

### Analiz Akışı

1. Kullanıcı "Analiz Başlat" butonuna tıklar
2. Frontend: POST /api/v1/analyses
3. Backend: Analiz kaydı oluştur (status: pending)
4. Background task başlat
5. Git servisi ile commit'leri çek
6. Her batch için:
   - Commit'u kaydet
   - File change'leri kaydet
   - LLM ile analiz et
   - Sonucu kaydet
7. Tüm commit'ler işlendi
8. Genel özet oluştur (LLM)
9. Sonuçları analiz kaydına ekle
10. Durumu "completed" olarak güncelle

### Rapor Oluşturma Akışı

1. Kullanıcı rapor türünü seçer
2. Frontend: POST /api/v1/reports
3. Backend: İlgili commit ve file change'leri çek
4. Analiz verilerini hazırla
5. LLM ile rapor oluştur
6. Markdown formatında rapor dönüştür
7. Frontend: Raporu göster

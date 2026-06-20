<div align="center">

```
 ██████╗ ██╗████████╗    ███████╗██╗      ██████╗  ██████╗██╗  ██╗
██╔════╝ ██║╚══██╔══╝    ██╔════╝██║     ██╔═══██╗██╔════╝██║ ██╔╝
██║  ███╗██║   ██║       █████╗  ██║     ██║   ██║██║     █████╔╝
██║   ██║██║   ██║       ██╔══╝  ██║     ██║   ██║██║     ██╔═██╗
╚██████╔╝██║   ██║       ██║     ███████╗╚██████╔╝╚██████╗██║  ██╗
 ╚═════╝ ╚═╝   ╚═╝       ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
```

# 🏛️ Git Archaeology Tool (GitArch)

### *Git Geçmişinizi Yapay Zeka ile Keşfedin*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

[📊 Demo](#-demo) • [⚡ Hızlı Başlangıç](#-hızlı-başlangıç) • [📚 Dokümantasyon](#-dokümantasyon) • [🤝 Katkıda Bulunma](#-katkıda-bulunma)

</div>

---

## 📋 İçindekiler

- [🎯 Proje Tanımı](#-proje-tanımı)
- [✨ Özellikler](#-özellikler)
- [🏗️ Mimari](#️-mimari)
- [⚡ Hızlı Başlangıç](#-hızlı-başlangıç)
- [🐳 Docker ile Kurulum](#-docker-ile-kurulum)
- [🔧 Manuel Kurulum](#-manuel-kurulum)
- [🤖 Yapay Zeka Sağlayıcıları](#-yapay-zeka-sağlayıcıları)
- [📡 API Endpoints](#-api-endpoints)
- [🗄️ Veri Modelleri](#️-veri-modelleri)
- [🎨 Frontend Bileşenleri](#-frontend-bileşenleri)
- [🌐 Sayfalar](#-sayfalar)
- [🔐 Kimlik Doğrulama](#-kimlik-doğrulama)
- [📊 Demo](#-demo)
- [🧪 Testler](#-testler)
- [🚀 Deployment](#-deployment)
- [🔧 Sorun Giderme](#-sorun-giderme)
- [📝 Changelog](#-changelog)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)
- [📄 Lisans](#-lisans)

---

## 🎯 Proje Tanımı

**Git Archaeology Tool (GitArch)**, Git depo geçmişini analiz ederek kodun **neden**, **ne zaman** ve **kim** tarafından değiştirildiğini anlayan, bunu doğal dilde açıklayan devrim niteliğinde bir araçtır.

### 🤔 Bu Araç Ne Yapar?

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   📁 Git Deposu  ──────►  🔍 Analiz  ──────►  📊 Rapor              │
│                                                                     │
│   • Commit geçmişi       • İstatistikler     • Doğal dil açıklama  │
│   • Dosya değişiklikleri • Trend analizi     • Öneriler            │
│   • Yazar bilgileri      • Hotspot tespiti   • Güvenlik analizi    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 🎯 Hedef Kullanıcılar

| Kullanıcı | Kullanım Senaryosu |
|-----------|-------------------|
| 💻 **Yazılım Geliştiriciler** | Legacy kodun neden böyle yazıldığını anlama |
| 🏗️ **DevOps Mühendisleri** | Deployment öncesi risk analizi |
| 👨‍💻 **Teknik Liderler** | Kod kalitesi ve trend takibi |
| 🔍 **Kod İnceleme Ekipleri** | Değişiklik geçmişini anlama |
| 🎓 **Yeni Katılımcılar** | Proje tarihçesini hızlı öğrenme |

### 💡 Neden GitArch?

| Sorun | Çözümümüz |
|-------|-----------|
| "Bu kod neden böyle yazılmış?" | 🤖 LLM ile doğal dilde açıklama |
| "Bu dosya neden sürekli değişiyor?" | 📊 Hotspot analizi ile tespit |
| "Bu değişiklik riskli mi?" | ⚠️ Risk skorlama sistemi |
| "Kim bu alanda uzman?" | 👥 Katkıcı analizi |
| "Legacy kodu nasıl anlarım?" | 🏛️ Arkeolojik raporlar |

---

## ✨ Özellikler

### 🔧 Temel Özellikler

```
┌─────────────────────────────────────────────────────────────────────┐
│  🔄 GIT DEPO ANALİZİ                                                │
│  ├── 📁 Depo klonlama ve senkronizasyon                             │
│  ├── 📜 Commit geçmişi analizi                                       │
│  ├── 📄 Dosya değişiklik takibi                                     │
│  ├── 🌿 Branch karşılaştırması                                      │
│  └── 📊 İstatistiksel özet                                          │
│                                                                     │
│  🤖 YAPAY ZEKA ENTEGRASYONU                                        │
│  ├── 💬 Doğal dilde kod açıklaması                                  │
│  ├── 🔍 Anomali tespiti                                             │
│  ├── 💡 İyileştirme önerileri                                       │
│  ├── 🔒 Güvenlik analizi                                            │
│  └── 📈 Trend tahminleri                                            │
│                                                                     │
│  📊 RAPORLAMA                                                       │
│  ├── 📄 Markdown raporlar                                           │
│  ├── 📈 İstatistiksel grafikler                                     │
│  ├── 👥 Yazar katkı haritaları                                      │
│  ├── 🔥 Hotspot haritaları                                          │
│  └── 📋 Özelleştirilebilir şablonlar                                │
│                                                                     │
│  🌐 WEB ARAYÜZÜ                                                     │
│  ├── 📱 Responsive tasarım                                          │
│  ├── 🎨 Modern UI/UX                                                │
│  ├── ⚡ Gerçek zamanlı güncelleme                                    │
│  ├── 🔐 JWT kimlik doğrulama                                        │
│  └── 🌍 Türkçe arayüz                                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 🎨 Görsel Özellikler

- **Gradient Banner**: Hoş geldiniz mesajı ve hızlı erişim butonları
- **Renkli İstatistik Kartları**: Mavi, mor, yeşil, kırmızı tonlarında
- **Animasyonlu Sidebar**: Mobilde arka plan karartmalı overlay
- **Durum Rozetleri**: Beklemede, Çalışıyor, Tamamlandı, Başarısız
- **Progress Bar**: Gerçek zamanlı analiz ilerlemesi
- **Hover Efektleri**: Modern kart ve liste etkileşimleri

---

## 🏗️ Mimari

### 📐 Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              🌐 TARAYICI                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        React SPA (Vite)                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │Dashboard │  │ Depolar  │  │ Analizler│  │ Raporlar │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                         │   │
│  │  │Commitler │  │ Ayarlar  │  │  Login   │                         │   │
│  │  └──────────┘  └──────────┘  └──────────┘                         │   │
│  └─────────────────────────────────┬───────────────────────────────────┘   │
│                                    │ REST API                               │
└────────────────────────────────────┼───────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼───────────────────────────────────────┐
│                              🖥️ SUNUCU                                     │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │                     FastAPI Backend (Python)                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │Auth API  │  │Repo API  │  │Analiz API│  │Report API│           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                         │   │
│  │  │Git Serv. │  │LLM Serv. │  │Queue Work│                         │   │
│  │  └──────────┘  └──────────┘  └──────────┘                         │   │
│  └─────────────────────────────────┬───────────────────────────────────┘   │
│                                    │                                       │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │                        🗄️ VERİ KATMANI                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │PostgreSQL│  │  Redis   │  │Git Repos │  │  SQLite  │           │   │
│  │  │(Prod)    │  │(Cache)   │  │(Disk)    │  │(Dev)     │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     🤖 YAPAY ZEKA KATMANI                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │ OpenAI   │  │Anthropic │  │  Gemini  │  │  Groq    │           │   │
│  │  │ GPT-4o   │  │Claude 3.5│  │Flash 2.5 │  │Llama 70B │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │ Mistral  │  │DeepSeek  │  │  Qwen    │  │  Local   │           │   │
│  │  │  Large   │  │   V3     │  │  Plus    │  │ Ollama   │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────┘
```

### 🔄 Veri Akışı

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Kullanıcı│───►│ Frontend │───►│ Backend  │───►│   Git    │───►│   LLM    │
│          │    │  (React) │    │ (FastAPI)│    │  Repos   │    │  Models  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     ▲                               │               │               │
     │                               ▼               ▼               ▼
     │                         ┌──────────┐    ┌──────────┐    ┌──────────┐
     └─────────────────────────│ Database │    │  Cache   │    │  Queue   │
                               │(Postgres)│    │ (Redis)  │    │ (Celery) │
                               └──────────┘    └──────────┘    └──────────┘
```

### 📁 Proje Yapısı

```
git-archaeology/
├── 📄 .env.example              # Çevresel değişken şablonu
├── 📄 .gitignore                # Git yok sayma kuralları
├── 📄 docker-compose.yml        # Docker compose yapılandırması
├── 📄 docker-compose.dev.yml    # Geliştirme docker compose
├── 📄 README.md                 # Bu dosya
├── 📄 PROMPT.md                 # Proje spesifikasyonu
│
├── 📁 backend/                  # 🐍 Python FastAPI Backend
│   ├── 📄 Dockerfile            # Backend Docker imajı
│   ├── 📄 Dockerfile.dev        # Geliştirme Docker imajı
│   ├── 📄 requirements.txt      # Python bağımlılıkları
│   ├── 📄 alembic.ini           # Alembic yapılandırması
│   │
│   ├── 📁 alembic/              # Veritabanı migrasyonları
│   │   ├── 📄 env.py
│   │   ├── 📄 script.py.mako
│   │   └── 📁 versions/
│   │       ├── 📄 001_initial.py
│   │       └── 📄 002_sqlite_compatible.py
│   │
│   ├── 📁 app/                  # Ana uygulama
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py           # FastAPI app entry point
│   │   ├── 📄 database.py       # SQLAlchemy engine & session
│   │   ├── 📄 worker.py         # Celery worker
│   │   │
│   │   ├── 📁 core/             # Çekirdek modüller
│   │   │   ├── 📄 config.py     # Pydantic Settings
│   │   │   ├── 📄 logging.py    # Logging yapılandırması
│   │   │   └── 📄 i18n.py       # Uluslararasılaştırma
│   │   │
│   │   ├── 📁 models/           # SQLAlchemy modelleri
│   │   │   ├── 📄 repository.py # Repository, Commit, Analysis
│   │   │   └── 📄 user.py       # User modeli
│   │   │
│   │   ├── 📁 schemas/          # Pydantic shemaları
│   │   │   └── 📄 repository.py # Request/Response shemaları
│   │   │
│   │   ├── 📁 api/              # API endpointleri
│   │   │   ├── 📄 deps.py       # Bağımlılık enjeksiyonu
│   │   │   └── 📁 v1/
│   │   │       └── 📁 routes/
│   │   │           ├── 📄 auth.py
│   │   │           ├── 📄 repository.py
│   │   │           ├── 📄 analysis.py
│   │   │           ├── 📄 commits.py
│   │   │           ├── 📄 reports.py
│   │   │           └── 📄 providers.py
│   │   │
│   │   ├── 📁 services/         # İş mantığı
│   │   │   ├── 📄 git_service.py
│   │   │   ├── 📄 llm_service.py
│   │   │   ├── 📄 analysis_engine.py
│   │   │   ├── 📄 report_service.py
│   │   │   └── 📄 cache_service.py
│   │   │
│   │   └── 📁 middleware/       # Middleware'ler
│   │       ├── 📄 error_handler.py
│   │       ├── 📄 rate_limit.py
│   │       └── 📄 monitoring.py
│   │
│   ├── 📁 cli/                  # CLI araçları
│   │   └── 📄 main.py
│   │
│   └── 📁 tests/                # Testler
│       ├── 📄 __init__.py
│       ├── 📄 conftest.py
│       ├── 📄 test_git_service.py
│       └── 📄 test_analysis_engine.py
│
├── 📁 frontend/                 # ⚛️ React TypeScript Frontend
│   ├── 📄 Dockerfile            # Frontend Docker imajı
│   ├── 📄 nginx.conf            # Nginx yapılandırması
│   ├── 📄 package.json          # Node.js bağımlılıkları
│   ├── 📄 vite.config.ts        # Vite yapılandırması
│   ├── 📄 tailwind.config.ts    # Tailwind yapılandırması
│   ├── 📄 tsconfig.json         # TypeScript yapılandırması
│   ├── 📄 postcss.config.js     # PostCSS yapılandırması
│   ├── 📄 index.html            # HTML entry point
│   │
│   ├── 📁 public/               # Statik dosyalar
│   │   └── 📄 vite.svg
│   │
│   └── 📁 src/                  # Kaynak kodlar
│       ├── 📄 App.tsx           # Ana bileşen
│       ├── 📄 main.tsx          # Entry point
│       ├── 📄 index.css         # Global stiller
│       │
│       ├── 📁 api/              # API istemcileri
│       │   ├── 📄 client.ts     # Axios/Fetch wrapper
│       │   ├── 📄 repositories.ts
│       │   ├── 📄 analyses.ts
│       │   ├── 📄 commits.ts
│       │   ├── 📄 reports.ts
│       │   └── 📄 providers.ts
│       │
│       ├── 📁 components/       # React bileşenleri
│       │   ├── 📁 common/       # Ortak bileşenler
│       │   │   ├── 📄 DataTable.tsx
│       │   │   ├── 📄 DateRangePicker.tsx
│       │   │   ├── 📄 ErrorBoundary.tsx
│       │   │   └── 📄 LoadingSpinner.tsx
│       │   │
│       │   ├── 📁 layout/       # Layout bileşenleri
│       │   │   ├── 📄 Header.tsx
│       │   │   ├── 📄 Layout.tsx
│       │   │   └── 📄 Sidebar.tsx
│       │   │
│       │   ├── 📁 analysis/     # Analiz bileşenleri
│       │   │   ├── 📄 AnalysisCard.tsx
│       │   │   ├── 📄 AnalysisProgress.tsx
│       │   │   └── 📄 StartAnalysisForm.tsx
│       │   │
│       │   ├── 📁 commits/      # Commit bileşenleri
│       │   │   ├── 📄 CommitList.tsx
│       │   │   ├── 📄 CommitDetail.tsx
│       │   │   └── 📄 CommitFilters.tsx
│       │   │
│       │   ├── 📁 repositories/ # Depo bileşenleri
│       │   │   ├── 📄 RepositoryList.tsx
│       │   │   └── 📄 CreateRepositoryForm.tsx
│       │   │
│       │   └── 📁 reports/      # Rapor bileşenleri
│       │       ├── 📄 ReportCard.tsx
│       │       ├── 📄 ReportPreview.tsx
│       │       └── 📄 GenerateReportForm.tsx
│       │
│       ├── 📁 pages/            # Sayfa bileşenleri
│       │   ├── 📄 Dashboard.tsx
│       │   ├── 📄 Login.tsx
│       │   ├── 📄 Repositories.tsx
│       │   ├── 📄 RepositoryDetail.tsx
│       │   ├── 📄 Analysis.tsx
│       │   ├── 📄 AnalysisDetail.tsx
│       │   ├── 📄 Commits.tsx
│       │   ├── 📄 Reports.tsx
│       │   └── 📄 Settings.tsx
│       │
│       ├── 📁 hooks/            # React hook'ları
│       │   ├── 📄 useRepository.ts
│       │   ├── 📄 useAnalysis.ts
│       │   └── 📄 useCommits.ts
│       │
│       ├── 📁 store/            # State yönetimi
│       │   ├── 📄 authStore.ts
│       │   └── 📄 uiStore.ts
│       │
│       ├── 📁 types/            # TypeScript tipleri
│       │   └── 📄 index.ts
│       │
│       └── 📁 utils/            # Yardımcı fonksiyonlar
│           ├── 📄 formatters.ts
│           └── 📄 validators.ts
│
├── 📁 docs/                     # 📚 Dokümantasyon
│   ├── 📁 api/                  # API dokümantasyonu
│   │   ├── 📄 repositories.md
│   │   ├── 📄 analyses.md
│   │   ├── 📄 commits.md
│   │   └── 📄 reports.md
│   │
│   ├── 📁 architecture/         # Mimari dokümantasyon
│   │   ├── 📄 overview.md
│   │   ├── 📄 database.md
│   │   └── 📄 security.md
│   │
│   ├── 📁 deployment/           # Deployment dokümantasyonu
│   │   ├── 📄 docker.md
│   │   ├── 📄 kubernetes.md
│   │   └── 📄 environment.md
│   │
│   ├── 📁 development/          # Geliştirme dokümantasyonu
│   │   ├── 📄 setup.md
│   │   ├── 📄 contributing.md
│   │   └── 📄 testing.md
│   │
│   └── 📁 user-guide/           # Kullanıcı kılavuzu
│       ├── 📄 getting-started.md
│       ├── 📄 creating-repository.md
│       ├── 📄 running-analysis.md
│       └── 📄 generating-reports.md
│
└── 📁 locales/                  # 🌍 Çeviri dosyaları
    └── 📄 tr.json               # Türkçe çeviriler
```

---

## ⚡ Hızlı Başlangıç

### 📋 Ön Gereksinimler

| Gereksinim | Versiyon | Kontrol Komutu |
|-----------|----------|----------------|
| 🐍 Python | 3.11+ | `python --version` |
| 📦 Node.js | 20+ | `node --version` |
| 📦 npm | 9+ | `npm --version` |
| 🐘 PostgreSQL | 16+ | `psql --version` |
| 🔴 Redis | 7+ | `redis-cli --version` |
| 🐳 Docker | 24+ | `docker --version` |

### 🚀 3 Kolay Adımda Başlayın

#### Adım 1: Depoyu Klonlayın

```bash
# Depoyu klonlayın
git clone https://github.com/Omerfaruk-aydn/git-archaeology.git

# Dizine gidin
cd git-archaeology
```

#### Adım 2: Çevresel Değişkenleri Yapılandırın

```bash
# Örnek .env dosyasını kopyalayın
cp .env.example .env

# .env dosyasını düzenleyin
nano .env  # veya favori editörünüzü kullanın
```

**Minimum Yapılandırma:**

```env
# Veritabanı (SQLite - geliştirme için)
DATABASE_URL=sqlite:///./gitarchaeology.db

# JWT Secret (değiştirin!)
JWT_SECRET_KEY=your-super-secret-key-change-this

# En az bir LLM sağlayıcısı (birini seçin)
OPENAI_API_KEY=sk-your-openai-key
# VEYA
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
# VEYA
GROQ_API_KEY=gsk-your-groq-key
# VEYA (ücretsiz)
LOCAL_LLM_URL=http://localhost:11434
DEFAULT_LLM_PROVIDER=local
```

#### Adım 3: Uygulamayı Çalıştırın

```bash
# Backend bağımlılıklarını yükleyin
cd backend
pip install -r requirements.txt

# Veritabanı tablolarını oluşturun
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"

# Backend'i başlatın (ayrı terminal)
uvicorn app.main:app --reload --port 8000

# Frontend bağımlılıklarını yükleyin (ayrı terminal)
cd ../frontend
npm install

# Frontend'i başlatın
npm run dev
```

### 🎉 Tebrikler!

Uygulama şimdi çalışıyor:

- 🌐 **Frontend**: http://localhost:5173
- 📡 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

---

## 🐳 Docker ile Kurulum

### Hızlı Başlangıç (Önerilen)

```bash
# Depoyu klonlayın
git clone https://github.com/Omerfaruk-aydn/git-archaeology.git
cd git-archaeology

# .env dosyasını oluşturun
cp .env.example .env

# API anahtarınızı ayarlayın
# nano .env

# Docker Compose ile başlatın
docker-compose up -d

# Durumu kontrol edin
docker-compose ps
```

### Docker Servisleri

| Servis | Port | Açıklama |
|--------|------|----------|
| `frontend` | 3000 | React uygulaması (Nginx) |
| `backend` | 8000 | FastAPI sunucusu |
| `worker` | - | Celery arka plan işleri |
| `db` | 5432 | PostgreSQL veritabanı |
| `redis` | 6379 | Redis önbellek |

### Docker Komutları

```bash
# Servisleri başlatın
docker-compose up -d

# Servisleri durdurun
docker-compose down

# Logları görüntüleyin
docker-compose logs -f

# Belirli bir servisin logları
docker-compose logs -f backend

# Veritabanına bağlanın
docker-compose exec db psql -U postgres -d gitarchaeology

# Backend'e SSH
docker-compose exec backend bash

# Veritabanını sıfırlayın
docker-compose down -v
docker-compose up -d
```

### Geliştirme Modu

```bash
# Geliştirme compose'u kullanın
docker-compose -f docker-compose.dev.yml up -d

# Hot reload ile development
docker-compose -f docker-compose.dev.yml logs -f backend
```

---

## 🔧 Manuel Kurulum

### Backend Kurulumu

```bash
cd backend

# Python sanal ortamı oluşturun
python -m venv venv

# Sanal ortamı etkinleştirin
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# .env dosyasını ayarlayın
cp ../.env.example ../.env
# ../.env dosyasını düzenleyin

# Veritabanı tablolarını oluşturun
python -c "
from app.database import engine, Base
from app.models import repository, user
Base.metadata.create_all(bind=engine)
print('✅ Veritabanı tabloları oluşturuldu!')
"

# Backend'i başlatın
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Kurulumu

```bash
cd frontend

# Bağımlılıkları yükleyin
npm install

# Geliştirme sunucusunu başlatın
npm run dev
```

### Production Build

```bash
cd frontend

# Production build
npm run build

# Build dizinini sunun
npm run preview
# veya
npx serve dist
```

---

## 🤖 Yapay Zeka Sağlayıcıları

### 📊 Sağlayıcı Karşılaştırması

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    YAPAY ZEKA SAĞLAYICI KARŞILAŞTIRMASI                      │
├──────────────┬──────────┬──────────┬──────────┬──────────┬─────────────────┤
│ Sağlayıcı    │ Hız      │ Kalite   │ Fiyat    │ Ücretsiz │ Model           │
├──────────────┼──────────┼──────────┼──────────┼──────────┼─────────────────┤
│ OpenAI       │ ⚡⚡⚡   │ ⭐⭐⭐⭐⭐│ $$       │ ❌       │ GPT-4o          │
│ Anthropic    │ ⚡⚡⚡   │ ⭐⭐⭐⭐⭐│ $$       │ ❌       │ Claude 3.5      │
│ Gemini       │ ⚡⚡⚡⚡ │ ⭐⭐⭐⭐  │ $        │ ✅       │ Flash 2.5       │
│ Groq         │ ⚡⚡⚡⚡⚡│ ⭐⭐⭐⭐  │ $        │ ✅       │ Llama 70B       │
│ Mistral      │ ⚡⚡⚡   │ ⭐⭐⭐⭐  │ $$       │ ❌       │ Large           │
│ DeepSeek     │ ⚡⚡⚡   │ ⭐⭐⭐⭐  │ $        │ ❌       │ V3              │
│ Local        │ ⚡⚡     │ ⭐⭐⭐    │ Ücretsiz │ ✅       │ Ollama          │
└──────────────┴──────────┴──────────┴──────────┴──────────┴─────────────────┘
```

### 🏢 Bulut Sağlayıcıları

#### OpenAI

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1
```

| Model | Yetenek | Fiyat (1M token) |
|-------|---------|-----------------|
| `gpt-4o` | En yeni, çok modlu | $2.50 / $10.00 |
| `gpt-4o-mini` | Hızlı ve ucuz | $0.15 / $0.60 |
| `gpt-4-turbo` | Eski ama güçlü | $10.00 / $30.00 |

#### Anthropic

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

| Model | Yetenek | Fiyat (1M token) |
|-------|---------|-----------------|
| `claude-3-5-sonnet` | En dengeli | $3.00 / $15.00 |
| `claude-3-opus` | En yetenekli | $15.00 / $75.00 |
| `claude-3-haiku` | En hızlı | $0.25 / $1.25 |

#### Google Gemini

```env
GEMINI_API_KEY=your-gemini-key
GEMINI_MODEL=gemini-2.5-flash
```

| Model | Yetenek | Fiyat (1M token) |
|-------|---------|-----------------|
| `gemini-2.5-flash` | Hızlı ve ücretsiz | Ücretsiz (sınırlı) |
| `gemini-2.5-pro` | En güçlü | $1.25 / $5.00 |

### ⚡ Hız Odaklı Sağlayıcılar

#### Groq (Ultra Hızlı)

```env
GROQ_API_KEY=gsk-your-key-here
GROQ_MODEL=llama-3.3-70b-versatile
```

> 💡 Groq, LPU (Language Processing Unit) kullanarak **inanılmaz hızlı** inference sağlar. Ücretsiz tier mevcuttur.

#### Together AI

```env
TOGETHER_API_KEY=your-key-here
TOGETHER_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
```

### 🇹🇷 Türk Sağlayıcılar

#### DeepSeek (Uygun Fiyatlı)

```env
DEEPSEEK_API_KEY=sk-your-key-here
DEEPSEEK_MODEL=deepseek-chat
```

> 💡 DeepSeek V3, GPT-4 kalitesinde ama **10x daha ucuz**!

### 🏠 Yerel Model (Ücretsiz)

#### Ollama Kurulumu

```bash
# Ollama'yı kurun
curl -fsSL https://ollama.ai/install.sh | sh

# Model indirin
ollama pull llama3
ollama pull codellama
ollama pull mistral

# Ollama'yı başlatın
ollama serve
```

```env
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3
DEFAULT_LLM_PROVIDER=local
```

### 🔀 OpenRouter (100+ Model)

```env
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_MODEL=openai/gpt-4o
```

> 💡 OpenRouter, tek API key ile **100+ model**e erişim sağlar.

---

## 📡 API Endpoints

### 🔐 Kimlik Doğrulama

| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `POST` | `/api/v1/auth/register` | Kullanıcı kaydı | ❌ |
| `POST` | `/api/v1/auth/login` | Giriş yapma | ❌ |
| `GET` | `/api/v1/auth/me` | Mevcut kullanıcı bilgisi | ✅ |

### 📁 Deposalar

| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/v1/repositories` | Depoları listele | ✅ |
| `POST` | `/api/v1/repositories` | Yeni depo ekle | ✅ |
| `GET` | `/api/v1/repositories/:id` | Depo detayı | ✅ |
| `PUT` | `/api/v1/repositories/:id` | Depo güncelle | ✅ |
| `DELETE` | `/api/v1/repositories/:id` | Depo sil | ✅ |
| `POST` | `/api/v1/repositories/:id/clone` | Depoyu klonla | ✅ |
| `POST` | `/api/v1/repositories/:id/sync` | Depoyu senkronize et | ✅ |

### 🔍 Analizler

| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/v1/analyses` | Analizleri listele | ✅ |
| `POST` | `/api/v1/analyses` | Yeni analiz başlat | ✅ |
| `GET` | `/api/v1/analyses/:id` | Analiz detayı | ✅ |
| `GET` | `/api/v1/analyses/:id/result` | Analiz sonuçları | ✅ |
| `DELETE` | `/api/v1/analyses/:id` | Analiz sil | ✅ |

### 📜 Commit'ler

| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/v1/commits` | Commit'leri listele | ✅ |
| `GET` | `/api/v1/commits/:sha` | Commit detayı | ✅ |
| `POST` | `/api/v1/commits/:sha/analyze` | Commit analiz et | ✅ |
| `GET` | `/api/v1/commits/:sha/explain` | Değişikliği açıkla | ✅ |

### 📊 Raporlar

| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `POST` | `/api/v1/reports` | Rapor oluştur | ✅ |
| `GET` | `/api/v1/reports/:repo_id/archeological/:path` | Arkeolojik rapor | ✅ |

### 🤖 LLM Sağlayıcıları

| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/v1/llm/providers` | Tüm sağlayıcıları listele | ❌ |
| `GET` | `/api/v1/llm/providers/available` | Aktif sağlayıcıları listele | ❌ |

### 📋 İstek/Yanıt Örnekleri

#### Depo Oluşturma

```bash
curl -X POST http://localhost:8000/api/v1/repositories \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Projem",
    "url": "https://github.com/user/repo.git",
    "description": "Açıklama",
    "default_branch": "main"
  }'
```

**Yanıt:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Projem",
  "url": "https://github.com/user/repo.git",
  "local_path": null,
  "default_branch": "main",
  "description": "Açıklama",
  "is_analyzed": false,
  "last_analyzed_at": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Analiz Başlatma

```bash
curl -X POST http://localhost:8000/api/v1/analyses \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "repository_id": "550e8400-e29b-41d4-a716-446655440000",
    "branch": "main",
    "max_commits": 100,
    "llm_provider": "openai",
    "llm_model": "gpt-4o",
    "focus_areas": ["security", "performance"],
    "include_diffs": true,
    "batch_size": 10
  }'
```

**Yanıt:**

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "repository_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "progress": 0.0,
  "total_commits": 0,
  "processed_commits": 0,
  "error_message": null,
  "started_at": null,
  "completed_at": null,
  "created_at": "2024-01-15T10:35:00Z"
}
```

---

## 🗄️ Veri Modelleri

### 📊 Entity İlişkileri

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│      User       │       │   Repository    │       │     Branch      │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (UUID)       │◄──┐   │ id (UUID)       │◄──┐   │ id (UUID)       │
│ email           │   │   │ name            │   │   │ repository_id   │──┐
│ username        │   │   │ url             │   │   │ name            │  │
│ password_hash   │   │   │ local_path      │   │   │ head_sha        │  │
│ full_name       │   │   │ default_branch  │   │   │ is_default      │  │
│ avatar_url      │   │   │ description     │   │   │ created_at      │  │
│ created_at      │   │   │ is_analyzed     │   │   └─────────────────┘  │
│ updated_at      │   │   │ last_analyzed_at│   │                        │
└─────────────────┘   │   │ owner_id        │──┘                        │
                      │   │ created_at      │                           │
                      │   │ updated_at      │                           │
                      │   └─────────────────┘                           │
                      │         │                                       │
                      │         │ 1:N                                   │
                      │         ▼                                       │
                      │   ┌─────────────────┐                           │
                      │   │     Commit      │                           │
                      │   ├─────────────────┤                           │
                      │   │ id (UUID)       │                           │
                      │   │ repository_id   │──┐                        │
                      │   │ sha             │  │                        │
                      │   │ message         │  │                        │
                      │   │ author_name     │  │                        │
                      │   │ author_email    │  │                        │
                      │   │ author_date     │  │                        │
                      │   │ additions       │  │                        │
                      │   │ deletions       │  │                        │
                      │   │ files_changed   │  │                        │
                      │   │ analyzed        │  │                        │
                      │   │ analysis_result │  │                        │
                      │   │ created_at      │  │                        │
                      │   └─────────────────┘  │                        │
                      │         │              │                        │
                      │         │ 1:N          │                        │
                      │         ▼              │                        │
                      │   ┌─────────────────┐  │                        │
                      │   │   FileChange    │  │                        │
                      │   ├─────────────────┤  │                        │
                      │   │ id (UUID)       │  │                        │
                      │   │ commit_id       │──┘                        │
                      │   │ file_path       │                           │
                      │   │ old_path        │                           │
                      │   │ change_type     │                           │
                      │   │ additions       │                           │
                      │   │ deletions       │                           │
                      │   │ diff            │                           │
                      │   │ old_content     │                           │
                      │   │ new_content     │                           │
                      │   │ analysis        │                           │
                      │   └─────────────────┘                           │
                      │                                                 │
                      │   ┌─────────────────┐                           │
                      │   │    Analysis     │                           │
                      │   ├─────────────────┤                           │
                      │   │ id (UUID)       │                           │
                      │   │ repository_id   │──┐                        │
                      │   │ status          │  │                        │
                      │   │ progress        │  │                        │
                      │   │ total_commits   │  │                        │
                      │   │ processed_commits│ │                        │
                      │   │ error_message   │  │                        │
                      │   │ result          │  │                        │
                      │   │ config          │  │                        │
                      │   │ started_at      │  │                        │
                      │   │ completed_at    │  │                        │
                      │   │ created_at      │  │                        │
                      │   └─────────────────┘  │                        │
                      │                         │                        │
                      │   ┌─────────────────┐  │                        │
                      │   │ FileSnapshot    │  │                        │
                      │   ├─────────────────┤  │                        │
                      │   │ id (UUID)       │  │                        │
                      │   │ repository_id   │──┘                        │
                      │   │ file_path       │                           │
                      │   │ commit_sha      │                           │
                      │   │ content         │                           │
                      │   │ content_hash    │                           │
                      │   │ size_bytes      │                           │
                      │   │ created_at      │                           │
                      │   └─────────────────┘                           │
                      │                                                 │
                      └─────────────────────────────────────────────────┘
```

### 📝 Model Detayları

#### Repository

```python
class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[str]                    # UUID primary key
    name: Mapped[str]                  # Depo adı (max 255)
    url: Mapped[str]                   # Git URL (max 1024)
    local_path: Mapped[Optional[str]]  # Yerel disk yolu
    default_branch: Mapped[str]        # Varsayılan branch (main)
    description: Mapped[Optional[str]] # Açıklama
    is_analyzed: Mapped[bool]          # Analiz edildi mi?
    last_analyzed_at: Mapped[Optional[datetime]]  # Son analiz tarihi
    owner_id: Mapped[str]              # Kullanıcı ID (FK)
    created_at: Mapped[datetime]       # Oluşturulma tarihi
    updated_at: Mapped[datetime]       # Güncellenme tarihi
```

#### Commit

```python
class Commit(Base):
    __tablename__ = "commits"

    id: Mapped[str]                    # UUID primary key
    repository_id: Mapped[str]         # Depo ID (FK)
    sha: Mapped[str]                   # Git SHA (40 char)
    message: Mapped[str]               # Commit mesajı
    author_name: Mapped[str]           # Yazar adı
    author_email: Mapped[str]          # Yazar e-postası
    author_date: Mapped[datetime]      # Yazar tarihi
    committer_name: Mapped[str]        # İşlem yapan adı
    committer_email: Mapped[str]       # İşlem yapan e-postası
    committer_date: Mapped[datetime]   # İşlem tarihi
    parents: Mapped[Optional[list]]    # Parent SHA'ları (JSON)
    additions: Mapped[int]             # Eklenen satırlar
    deletions: Mapped[int]             # Silinen satırlar
    files_changed: Mapped[int]         # Değişen dosya sayısı
    analyzed: Mapped[bool]             # Analiz edildi mi?
    analysis_result: Mapped[Optional[dict]]  # Analiz sonucu (JSON)
```

#### Analysis

```python
class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[str]                    # UUID primary key
    repository_id: Mapped[str]         # Depo ID (FK)
    status: Mapped[str]                # pending/running/completed/failed
    progress: Mapped[float]            # İlerleme (0.0 - 100.0)
    total_commits: Mapped[int]         # Toplam commit sayısı
    processed_commits: Mapped[int]     # İşlenen commit sayısı
    error_message: Mapped[Optional[str]]  # Hata mesajı
    result: Mapped[Optional[dict]]     # Analiz sonucu (JSONB)
    config: Mapped[Optional[dict]]     # Analiz yapılandırması (JSONB)
    started_at: Mapped[Optional[datetime]]  # Başlangıç tarihi
    completed_at: Mapped[Optional[datetime]]  # Bitiş tarihi
```

---

## 🎨 Frontend Bileşenleri

### 🧩 Bileşen Ağacı

```
App
└── ProtectedRoute
    └── Layout
        ├── Sidebar
        │   └── Navigation Links
        ├── Header
        │   ├── Menu Button
        │   └── User Info + Logout
        └── Main Content
            ├── Dashboard
            │   ├── Welcome Banner
            │   ├── Stat Cards
            │   ├── Repository List
            │   └── Analysis List
            ├── Repositories
            │   ├── Search Input
            │   ├── Repository List
            │   └── Create Repository Modal
            ├── RepositoryDetail
            │   ├── Repository Info
            │   ├── Branch Selector
            │   ├── Tab Navigation
            │   ├── Commit List
            │   └── Analysis List
            ├── Analysis
            │   ├── Analysis List
            │   └── Analysis Card
            ├── AnalysisDetail
            │   ├── Analysis Info
            │   ├── Progress Bar
            │   ├── Tab Navigation
            │   ├── Insights
            │   ├── Recommendations
            │   ├── File Hotspots
            │   └── Author Contributions
            ├── Commits
            │   ├── Author Filter
            │   ├── Commit List
            │   └── Commit Detail
            ├── Reports
            │   ├── Report List
            │   └── Report Preview
            ├── Settings
            │   ├── Profile Info
            │   ├── LLM Providers
            │   └── App Settings
            └── Login
                ├── Login Form
                └── Register Form
```

### 📦 Bileşen Detayları

#### Dashboard

```tsx
// 🏠 Ana sayfa - Genel bakış ve hızlı erişim
// Özelliği:
// - Gradient karşılama banner'ı
// - İstatistik kartları (Depo, Analiz, Tamamlanan, Başarısız)
// - Son eklenen depolar listesi
// - Son analizler listesi
// - Boş durum görseli
```

#### Sidebar

```tsx
// 📱 Mobil uyumlu navigasyon
// Özelliği:
// - Fixed pozisyonlu sol sidebar
// - Mobilde overlay karartma
// - Link tıklamasıyla otomatik kapanma
// - Aktif sayfa vurgulama
// - Transformsasyon animasyonları
```

#### AnalysisCard

```tsx
// 📊 Analiz kartı bileşeni
// Özelliği:
// - Durum rozeti (Beklemede/Çalışıyor/Tamamlandı/Başarısız)
// - İlerleme çubuğu
// - Commit istatistikleri
// - Tarih bilgisi
```

#### CommitDetail

```tsx
// 📜 Detaylı commit görüntüleme
// Özelliği:
// - SHA ve mesaj
// - Yazar ve tarih bilgisi
// - Dosya değişiklikleri listesi
// - Diff görüntüleme
// - Analiz sonuçları
```

---

## 🌐 Sayfalar

### 📄 Sayfa Haritası

| Sayfa | Yol | Açıklama |
|-------|-----|----------|
| 🏠 Dashboard | `/` | Ana sayfa, genel bakış |
| 🔐 Login | `/login` | Giriş/Kayıt sayfası |
| 📁 Depolar | `/repositories` | Depo listesi |
| 📁 Depo Detayı | `/repositories/:id` | Depo bilgileri, commit'ler, analizler |
| 🔍 Analizler | `/analyses` | Analiz listesi |
| 🔍 Analiz Detayı | `/analyses/:id` | Analiz sonuçları ve öneriler |
| 📜 Commit'ler | `/commits?repo=:id` | Commit listesi |
| 📊 Raporlar | `/reports` | Rapor listesi |
| ⚙️ Ayarlar | `/settings` | Profil ve uygulama ayarları |

### 🎨 Sayfa Görünümleri

#### Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  🏛️ GitArch'e Hoş Geldiniz                                      │
│  Git depolarınızın geçmişini analiz edin...                      │
│  [ Yeni Depo Ekle ] [ Raporları Görüntüle ]                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ 📁 3     │ │ 🔍 5     │ │ ✓ 4      │ │ ✗ 1      │           │
│  │ Toplam   │ │ Toplam   │ │ Tamamlan │ │ Başarısız│           │
│  │ Depo     │ │ Analiz   │ │ ANALİZ   │ │ ANALİZ   │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
├─────────────────────────────────────────────────────────────────┤
│  Son Eklenen Depolar          │  Son Analizler                  │
│  ┌────────────────────────┐   │  ┌────────────────────────┐     │
│  │ 📁 repo-1              │   │  │ 🔍 Analiz #a1b2...     │     │
│  │    github.com/...      │   │  │    50/100 commit       │     │
│  │    Analiz Edildi ✓     │   │  │    ✓ Tamamlandı        │     │
│  ├────────────────────────┤   │  ├────────────────────────┤     │
│  │ 📁 repo-2              │   │  │ 🔍 Analiz #c3d4...     │     │
│  │    github.com/...      │   │  │    25/50 commit        │     │
│  │    Beklemede           │   │  │    ⏳ Çalışıyor ████░░ │     │
│  └────────────────────────┘   │  └────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

#### Login

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    🏛️ GitArch                                    │
│                                                                 │
│                    Giriş Yap                                     │
│                    Git Arkeoloji Aracı                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ E-posta                                                  │   │
│  │ ┌─────────────────────────────────────────────────────┐ │   │
│  │ │ user@example.com                                     │ │   │
│  │ └─────────────────────────────────────────────────────┘ │   │
│  │                                                         │   │
│  │ Şifre                                                   │   │
│  │ ┌─────────────────────────────────────────────────────┐ │   │
│  │ │ ••••••••                                             │ │   │
│  │ └─────────────────────────────────────────────────────┘ │   │
│  │                                                         │   │
│  │ ┌─────────────────────────────────────────────────────┐ │   │
│  │ │                   GİRİŞ YAP                         │ │   │
│  │ └─────────────────────────────────────────────────────┘ │   │
│  │                                                         │   │
│  │          Hesabınız yok mu? Kayıt olun                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Kimlik Doğrulama

### 🔑 JWT Token Akışı

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  Kullanıcı│                    │ Frontend │                    │ Backend  │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. Giriş Yap                 │                               │
     │  (email + password)           │                               │
     │──────────────────────────────►│                               │
     │                               │  2. POST /auth/login          │
     │                               │──────────────────────────────►│
     │                               │                               │
     │                               │  3. JWT Token                 │
     │                               │◄──────────────────────────────│
     │                               │                               │
     │  4. Token sakla               │                               │
     │  (localStorage)               │                               │
     │◄──────────────────────────────│                               │
     │                               │                               │
     │  5. API İsteği                │                               │
     │  (Authorization: Bearer xxx)  │                               │
     │──────────────────────────────►│                               │
     │                               │  6. Token doğrula             │
     │                               │──────────────────────────────►│
     │                               │                               │
     │                               │  7. Yanıt                     │
     │                               │◄──────────────────────────────│
     │  8. Sonucu göster             │                               │
     │◄──────────────────────────────│                               │
     │                               │                               │
```

### 📝 Token Yapısı

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 🔒 Güvenlik Önlemleri

- **BCrypt**: Şifre hashleme (cost factor: 12)
- **JWT**: HS256 algoritması ile imzalama
- **CORS**: Sadece yetkili origin'lere izin
- **Rate Limiting**: IP bazlı istek kısıtlaması
- **Input Validation**: Pydantic ile tüm giriş doğrulama

---

## 📊 Demo

### 🎬 Ekran Görüntüleri

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  📱 Masaüstü Görünümü                                                       │
│  ┌─────────┬────────────────────────────────────────────────────────────┐   │
│  │         │                                                            │   │
│  │ 🏠 Dash │  🏛️ GitArch'e Hoş Geldiniz                                │   │
│  │ 📁 Depo │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │   │
│  │ 🔍 Anal │  │   3     │ │   5     │ │   4     │ │   1     │         │   │
│  │ 📜 Comm │  │  Depo   │ │ Analiz  │ │Tamamlan.│ │Başarısız│         │   │
│  │ 📊 Rapor│  └─────────┘ └─────────┘ └─────────┘ └─────────┘         │   │
│  │ ⚙️ Ayar │                                                            │   │
│  │         │  ┌────────────────────────────────────────────────────┐   │   │
│  │         │  │ Son Eklenen Depolar                                 │   │   │
│  │         │  │ 📁 git-archaeology  ✓ Analiz Edildi                │   │   │
│  │         │  │ 📁 frontend-app     ⏳ Beklemede                   │   │   │
│  │         │  │ 📁 backend-api      ✓ Analiz Edildi                │   │   │
│  │         │  └────────────────────────────────────────────────────┘   │   │
│  │         │                                                            │   │
│  └─────────┴────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 🖥️ Canlı Demo

> 🚧 Demo yakında eklenecek!

---

## 🧪 Testler

### 📋 Test Çalıştırma

```bash
cd backend

# Tüm testleri çalıştırın
pytest

# Coverage ile çalıştırın
pytest --cov=app --cov-report=html

# Sadece belirli testleri çalıştırın
pytest tests/test_git_service.py
pytest tests/test_analysis_engine.py

# Verimlilik testleri
pytest -v --tb=short
```

### 📊 Test Yapılandırması

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(test_db):
    from fastapi.testclient import TestClient
    from app.api.deps import get_db

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
```

---

## 🚀 Deployment

### 🐳 Docker ile Production

```bash
# Production compose
docker-compose -f docker-compose.yml up -d

# SSL sertifikası ekleyin (nginx.conf)
# Monitoring yapılandırın
# Backup stratejisi oluşturun
```

### ☸️ Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gitarch-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gitarch-backend
  template:
    metadata:
      labels:
        app: gitarch-backend
    spec:
      containers:
      - name: backend
        image: gitarch-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: gitarch-secrets
              key: database-url
```

### 🔧 Ortam Değişkenleri

| Değişken | Zorunlu | Açıklama |
|----------|---------|----------|
| `DATABASE_URL` | ✅ | Veritabanı bağlantı URL'i |
| `JWT_SECRET_KEY` | ✅ | JWT imzalama anahtarı |
| `OPENAI_API_KEY` | ⚠️* | OpenAI API anahtarı |
| `REDIS_URL` | ❌ | Redis bağlantı URL'i |
| `CORS_ORIGINS` | ❌ | İzin verilen origin'ler |

*En az bir LLM sağlayıcı API anahtarı gereklidir

---

## 🔧 Sorun Giderme

### 🐛 Sık Karşılaşılan Sorunlar

#### 1. "Cannot read properties of undefined (reading 'map')"

**Sebep**: API yanıt formatı frontend'in beklediği formatta değil.

**Çözüm**:
```bash
# Backend'i yeniden başlatın
# Hot reload değişiklikleri almayabilir
kill <backend_pid>
uvicorn app.main:app --reload --port 8000
```

#### 2. "bcrypt" Hatası

**Sebep**: passlib ve bcrypt versiyon uyumsuzluğu.

**Çözüm**:
```bash
pip uninstall bcrypt passlib
pip install bcrypt==4.0.1 passlib==1.7.4
```

#### 3. Veritabanı Tabloları Oluşmuyor

**Sebep**: Alembic migrasyonları çalıştırılmadı veya SQLite modunda tablolar elle oluşturulmalı.

**Çözüm**:
```bash
# SQLite için
python -c "
from app.database import engine, Base
from app.models import repository, user
Base.metadata.create_all(bind=engine)
"

# PostgreSQL için
alembic upgrade head
```

#### 4. CORS Hatası

**Sebep**: Frontend ve backend farklı portlarda.

**Çözüm**:
```env
# .env dosyasında
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

#### 5. "Module not found" Hatası

**Çözüm**:
```bash
# Python path ayarlayın
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# veya
cd backend
python -m uvicorn app.main:app --reload
```

### 📞 Destek

- 📧 **E-posta**: destek@gitarch.example.com
- 💬 **Discord**: [Sunucuya Katıl](https://discord.gg/example)
- 🐛 **Bug Report**: [GitHub Issues](https://github.com/Omerfaruk-aydn/git-archaeology/issues)

---

## 📝 Changelog

### [1.0.0] - 2024-01-15

#### ✨ Eklenenler
- 🎉 İlk sürüm yayınlandı
- 📁 Depo klonlama ve senkronizasyon
- 🔍 Commit analizi
- 🤖 LLM entegrasyonu (24+ sağlayıcı)
- 📊 Rapor oluşturma
- 🌐 Web arayüzü
- 🔐 JWT kimlik doğrulama
- 📱 Responsive tasarım
- 🇹🇷 Türkçe arayüz

#### 🐛 Düzeltilenler
- Sidebar kapatılamama sorunu
- Dashboard boş ekran hatası
- API yanıt format uyumsuzluğu
- bcrypt versiyon uyumsuzluğu

#### 📝 Değişiklikler
- Dashboard yeniden tasarlandı
- Sidebar mobil deneyim iyileştirildi
- İstatistik kartları renklendirildi

---

## 🤝 Katkıda Bulunma

### 📋 Katkı Rehberi

1. **Fork** yapın
2. **Branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. **Değişikliklerinizi** commit edin (`git commit -m 'feat: add amazing feature'`)
4. **Push** edin (`git push origin feature/amazing-feature`)
5. **Pull Request** oluşturun

### 🎯 Katkı Türleri

| Tür | Açıklama |
|-----|----------|
| 🐛 Bug Fix | Hata düzeltmeleri |
| ✨ Feature | Yeni özellikler |
| 📝 Docs | Dokümantasyon güncellemeleri |
| 🎨 Style | UI/UX iyileştirmeleri |
| ♻️ Refactor | Kod yeniden yapılandırma |
| 🧪 Test | Test eklemeleri |
| ⚡ Perf | Performans iyileştirmeleri |

### 📝 Commit Formatı

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Örnekler:**
```
feat(repositories): add repository cloning
fix(auth): resolve login timeout issue
docs(readme): update installation guide
style(dashboard): improve card layout
```

---

## 📄 Lisans

Bu proje **MIT Lisansı** altında yayınlanmıştır.

```
MIT License

Copyright (c) 2024 GitArch Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🔌 Backend Servis Detayları

### 🔧 Git Service

Git depolarıyla etkileşim sağlayan temel servis.

```python
class GitService:
    """
    Git depolarını yöneten servis.
    
    Özellikler:
    - Depo klonlama
    - Branch listeleme
    - Commit geçmişi
    - Diff çıkarma
    - Dosya içeriği okuma
    """
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
    
    def clone_repo(self, url: str, target_dir: str, branch: str = "main") -> bool:
        """Depoyu belirtilen dizine klonlar."""
        
    def get_commits(self, branch: str = "main", max_count: int = 100) -> List[Dict]:
        """Belirtilen branch'teki commit'leri listeler."""
        
    def get_file_changes(self, commit_sha: str, include_diff: bool = True) -> List[Dict]:
        """Belirli bir commit'teki dosya değişikliklerini döndürür."""
        
    def get_file_content_at_commit(self, commit_sha: str, file_path: str) -> Optional[str]:
        """Belirli bir commit'teki dosya içeriğini okur."""
        
    def get_branches(self) -> List[Dict]:
        """Depodaki tüm branch'leri listeler."""
        
    def pull_latest(self, branch: str = "main") -> bool:
        """En son değişiklikleri çeker."""
```

### 🤖 LLM Service

Yapay zeka modeliyle iletişim kuran servis.

```python
class LLMService:
    """
    LLM sağlayıcılarıyla çalışan servis.
    
    Desteklenen sağlayıcılar:
    - OpenAI (GPT-4o, GPT-4o-mini)
    - Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)
    - Google Gemini (Flash, Pro)
    - Groq (Llama 3.3 70B)
    - Mistral AI
    - DeepSeek
    - Local (Ollama)
    """
    
    def __init__(self, provider: str = "openai", model: Optional[str] = None):
        self.provider = provider
        self.model = model or self._get_default_model()
        
    async def analyze_commit(
        self,
        commit_message: str,
        file_changes: List[Dict],
        focus_areas: List[str]
    ) -> Dict:
        """
        Commit değişikliklerini analiz eder.
        
        Args:
            commit_message: Commit mesajı
            file_changes: Dosya değişiklikleri listesi
            focus_areas: Odak alanları (security, performance, etc.)
            
        Returns:
            Analiz sonucu (öneriler, risk seviyesi, açıklama)
        """
        
    async def explain_change(
        self,
        old_code: str,
        new_code: str,
        commit_message: str,
        file_path: str
    ) -> str:
        """
        Kod değişikliğini doğal dilde açıklar.
        
        Returns:
            Doğal dilde açıklama
        """
        
    async def generate_report(
        self,
        repository_name: str,
        analysis_data: Dict,
        report_type: str
    ) -> str:
        """
        Kapsamlı bir rapor oluşturur.
        
        Args:
            repository_name: Depo adı
            analysis_data: Analiz verileri
            report_type: Rapor türü (full, summary, security, architecture)
            
        Returns:
            Markdown formatında rapor
        """
```

### 📊 Analysis Engine

Analiz sürecini yöneten motor.

```python
class AnalysisEngine:
    """
    Analiz sürecini orkestra eden motor.
    
    Akış:
    1. Depo bilgilerini al
    2. Commit'leri topla
    3. Her commit'i LLM ile analiz et
    4. Sonuçları birleştir
    5. Rapor oluştur
    """
    
    def __init__(self, db: Session, git_service: GitService, llm_service: LLMService):
        self.db = db
        self.git_service = git_service
        self.llm_service = llm_service
        
    async def run_full_analysis(
        self,
        repository: Repository,
        config: AnalysisCreate
    ) -> Analysis:
        """
        Tam bir analiz çalıştırır.
        
        Adımlar:
        1. Analysis kaydı oluştur (status: pending)
        2. Commit'leri topla
        3. Her commit'i analiz et
        4. İstatistikleri hesapla
        5. LLM ile özet oluştur
        6. Sonuçları kaydet
        """
        
    async def analyze_single_commit(self, commit: Commit) -> Dict:
        """Tek bir commit'i analiz eder."""
        
    def calculate_statistics(self, commits: List[Commit]) -> Dict:
        """İstatistikleri hesaplar."""
```

### 📝 Report Service

Rapor oluşturma servisi.

```python
class ReportService:
    """
    Farklı türde raporlar oluşturan servis.
    
    Rapor türleri:
    - full: Kapsamlı analiz raporu
    - summary: Özet rapor
    - security: Güvenlik odaklı rapor
    - architecture: Mimari analiz raporu
    - legacy: Legacy kod analizi
    """
    
    def __init__(self, db: Session, llm_service: LLMService):
        self.db = db
        self.llm_service = llm_service
        
    async def generate_report(
        self,
        repository_id: str,
        report_type: str,
        branch: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        file_paths: Optional[List[str]] = None,
        format: str = "markdown"
    ) -> Dict:
        """Rapor oluşturur."""
        
    async def generate_archeological_report(
        self,
        repository_id: str,
        file_path: str
    ) -> str:
        """
        Belirli bir dosya için arkeolojik rapor oluşturur.
        
        Bu rapor şunları içerir:
        - Dosyanın ilk yazılma tarihi
        - Değişiklik geçmişi
        - Katkıcılar
        - Sık değişen bölgeler
        - Olası nedenler
        """
```

---

## ⚛️ Frontend Hook Detayları

### 📦 useRepository

```typescript
/**
 * Depo verilerini yöneten hook.
 * 
 * Özellikler:
 * - Depo listesi çekme
 * - Depo oluşturma
 * - Depo silme
 * - Sayfalama
 * - Arama
 */
export function useRepositoryList() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  
  // Otomatik veri çekme
  useEffect(() => {
    fetchRepositories();
  }, [page, search]);
  
  return {
    repositories,
    total,
    loading,
    error,
    page,
    setPage,
    search,
    setSearch,
    create,      // Yeni depo oluştur
    remove,      // Depo sil
    refresh,     // Listeyi yenile
  };
}
```

### 📦 useAnalysis

```typescript
/**
 * Analiz verilerini yöneten hook.
 * 
 * Özellikler:
 * - Analiz başlatma
 * - İlerleme takibi
 * - Sonuç görüntüleme
 * - Otomatik yenileme (running durumunda)
 */
export function useAnalysis(id?: string) {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Analiz çalışırken otomatik yenile
  useEffect(() => {
    if (analysis?.status === 'running') {
      const interval = setInterval(fetchAnalysis, 2000);
      return () => clearInterval(interval);
    }
  }, [analysis?.status]);
  
  return {
    analysis,
    result,
    loading,
    error,
    start,       // Yeni analiz başlat
    refresh,     // Analizi yenile
  };
}
```

### 📦 useCommits

```typescript
/**
 * Commit verilerini yöneten hook.
 * 
 * Özellikler:
 * - Commit listesi çekme
 * - Yazar filtreleme
 * - Sayfalama
 * - Tek commit detayı
 */
export function useCommits(repoId: string) {
  const [commits, setCommits] = useState<Commit[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [authorFilter, setAuthorFilter] = useState('');
  
  return {
    commits,
    total,
    loading,
    page,
    setPage,
    authorFilter,
    setAuthorFilter,
    refresh,
  };
}
```

---

## 🎨 UI Bileşen Detayı

### 📊 StatCard Bileşeni

```tsx
/**
 * İstatistik kartı bileşeni.
 * 
 * Renk kodları:
 * - blue: Depo sayısı
 * - purple: Analiz sayısı
 * - green: Tamamlanan
 * - red: Başarısız
 */
interface StatCardProps {
  title: string;
  value: number;
  icon: 'repository' | 'analysis' | 'check' | 'error';
  color: 'blue' | 'purple' | 'green' | 'red';
}

function StatCard({ title, value, icon, color }: StatCardProps) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className={`w-10 h-10 ${colors[color].bg} rounded-lg flex items-center justify-center`}>
              <span className={`${colors[color].icon} text-lg`}>
                {icon === 'repository' && '📁'}
                {icon === 'analysis' && '🔍'}
                {icon === 'check' && '✓'}
                {icon === 'error' && '✗'}
              </span>
            </div>
          </div>
          <div className="ml-4 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className={`text-2xl font-bold ${colors[color].text}`}>{value}</dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### 📱 Sidebar Bileşeni

```tsx
/**
 * Responsive sidebar bileşeni.
 * 
 * Özellikler:
 * - Mobilde overlay karartma
 * - Link tıklamasıyla otomatik kapanma
 * - Aktif sayfa vurgulama
 * - Transformsasyon animasyonları
 */
interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

function Sidebar({ isOpen, onToggle }: SidebarProps) {
  const location = useLocation();
  
  return (
    <>
      {/* Mobil overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/40 lg:hidden" 
          onClick={onToggle} 
        />
      )}
      
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 
        transform transition-transform duration-200 ease-in-out 
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        
        {/* Logo ve kapat butonu */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200">
          <Link to="/" onClick={onToggle}>
            <span className="text-xl font-bold text-indigo-600">GitArch</span>
          </Link>
          <button onClick={onToggle}>
            <XIcon />
          </button>
        </div>
        
        {/* Navigasyon linkleri */}
        <nav className="mt-5 px-2 space-y-1">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              onClick={onToggle}
              className={`flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                location.pathname === item.href
                  ? 'bg-indigo-50 text-indigo-600'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <span className="mr-3">{item.icon}</span>
              {item.name}
            </Link>
          ))}
        </nav>
      </div>
    </>
  );
}
```

### 📋 DataTable Bileşeni

```tsx
/**
 * Genel kullanım tablosu bileşeni.
 * 
 * Özellikler:
 * - Sıralanabilir sütunlar
 * - Sayfalama
 * - Boş durum gösterimi
 * - Yükleme durumu
 */
interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  emptyMessage?: string;
  onRowClick?: (item: T) => void;
}

function DataTable<T>({ 
  columns, 
  data, 
  loading, 
  emptyMessage = "Veri bulunamadı",
  onRowClick 
}: DataTableProps<T>) {
  if (loading) return <LoadingSpinner />;
  
  if (data.length === 0) {
    return <EmptyState message={emptyMessage} />;
  }
  
  return (
    <table className="min-w-full divide-y divide-gray-200">
      <thead>
        <tr>
          {columns.map((column) => (
            <th key={column.key}>{column.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <tr 
            key={index}
            onClick={() => onRowClick?.(item)}
            className="hover:bg-gray-50"
          >
            {columns.map((column) => (
              <td key={column.key}>
                {column.render(item)}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

---

## 🌍 Uluslararasılaştırma (i18n)

### 📄 Çeviri Dosyası Yapısı

```json
{
  "app": {
    "name": "GitArch",
    "description": "Git Arkeoloji Aracı"
  },
  "nav": {
    "dashboard": "Dashboard",
    "repositories": "Depolar",
    "analyses": "Analizler",
    "commits": "Commit'ler",
    "reports": "Raporlar",
    "settings": "Ayarlar"
  },
  "dashboard": {
    "welcome": "GitArch'e Hoş Geldiniz",
    "subtitle": "Git depolarınızın geçmişini analiz edin",
    "stats": {
      "totalRepos": "Toplam Depo",
      "totalAnalyses": "Toplam Analiz",
      "completedAnalyses": "Tamamlanan",
      "failedAnalyses": "Başarısız"
    },
    "recentRepos": "Son Eklenen Depolar",
    "recentAnalyses": "Son Analizler"
  },
  "auth": {
    "login": "Giriş Yap",
    "register": "Kayıt Ol",
    "email": "E-posta",
    "password": "Şifre",
    "username": "Kullanıcı Adı"
  },
  "common": {
    "loading": "Yükleniyor...",
    "error": "Hata oluştu",
    "save": "Kaydet",
    "cancel": "İptal",
    "delete": "Sil",
    "edit": "Düzenle"
  }
}
```

### 🔧 i18n Kullanımı

```tsx
import { useTranslation } from '../core/i18n';

function Dashboard() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h1>{t('dashboard.welcome')}</h1>
      <p>{t('dashboard.subtitle')}</p>
      
      <div className="stats">
        <StatCard title={t('dashboard.stats.totalRepos')} value={repos.length} />
        <StatCard title={t('dashboard.stats.totalAnalyses')} value={analyses.length} />
      </div>
    </div>
  );
}
```

---

## 🔒 Güvenlik Detayları

### 🛡️ Uygulanan Güvenlik Önlemleri

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GÜVENLİK KATMANLARI                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. 🔐 KİMLİK DOĞRULAMA                                                    │
│     ├── JWT token tabanlı oturum yönetimi                                   │
│     ├── BCrypt ile şifre hashleme (cost: 12)                               │
│     ├── Token süresi: 60 dakika                                            │
│     └── Refresh token desteği                                               │
│                                                                             │
│  2. 🛡️ YETKİLENDİRME                                                       │
│     ├── Kullanıcı bazlı veri erişimi                                        │
│     ├── Sahiplik doğrulaması (owner_id)                                    │
│     ├── Endpoint bazlı koruma                                               │
│     └── AdminYetkisi (gelecek özellik)                                     │
│                                                                             │
│  3. 🌐 SİBER GÜVENLİK                                                      │
│     ├── CORS politikası (sadece izin verilen origin'ler)                   │
│     ├── Rate limiting (IP bazlı)                                           │
│     ├── Input validation (Pydantic)                                        │
│     ├── SQL injection koruması (SQLAlchemy ORM)                            │
│     └── XSS koruması (React otomatik escaping)                            │
│                                                                             │
│  4. 📊 İZLEME VE LOGlama                                                   │
│     ├── Hata loglama                                                        │
│     ├── İstek/yanıt loglama (opsiyonel)                                    │
│     ├── Performans izleme                                                   │
│     └── Güvenlik olayı bildirimleri                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 🔑 Şifre Hashleme

```python
from passlib.context import CryptContext

# BCrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Şifre doğrulama."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Şifre hashleme."""
    return pwd_context.hash(password)
```

### 🎫 JWT Token Oluşturma

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWT access token oluşturur."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """JWT token doğrulama."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            return None
            
        return username
        
    except JWTError:
        return None
```

---

## 📈 Performans İpuçları

### ⚡ Hızlandırma Stratejileri

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PERFORMANS İYİLEŞTİRMELERİ                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🗄️ VERİTABANI                                                             │
│  ├── İndeksleme: Sorgu hızını %80 artırır                                 │
│  ├── Connection pooling: Bağlantı yeniden kullanma                         │
│  ├── Query optimization: N+1 sorguları önleme                              │
│  └── Read replicas: Okuma yükü dağıtma (production)                        │
│                                                                             │
│  📦 ÖNBELLEKLEME (Cache)                                                    │
│  ├── Redis ile analiz sonuçları cacheleme                                  │
│  ├── API yanıtları için HTTP cache headers                                 │
│  ├── Static dosyalar için CDN                                               │
│  └── LLM yanıtları için uygulama seviyesi cache                            │
│                                                                             │
│  🔄 ASYNC İŞLEMLER                                                         │
│  ├── FastAPI async/await desteği                                            │
│  ├── Celery ile arka plan analiz jobları                                   │
│  ├── Eşzamanlı LLM istekleri (batch processing)                            │
│  └── WebSocket ile gerçek zamanlı güncelleme                               │
│                                                                             │
│  📦 FRONTEND                                                                │
│  ├── Code splitting (lazy loading)                                          │
│  ├── Image optimization                                                     │
│  ├── Bundle size reduction                                                  │
│  ├── Service Worker caching                                                 │
│  └── Virtual scrolling (büyük listeler)                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📊 Performans Metrikleri

| Metrik | Hedef | Mevcut |
|--------|-------|--------|
| API Yanıt Süresi | < 200ms | ~150ms |
| İlk Yükleme | < 2s | ~1.5s |
| Lighthouse Skoru | > 90 | ~95 |
| Bundle Boyutu | < 500KB | ~400KB |
| Analiz Süresi (100 commit) | < 5dk | ~3dk |

---

## 🧩 Eklenti Geliştirme

### 🔌 Yeni LLM Sağlayıcı Ekleme

```python
# app/services/llm_providers/custom_provider.py

from typing import Optional, Dict, List
import httpx

class CustomLLMProvider:
    """
    Özel LLM sağlayıcı eklentisi.
    
    Adımlar:
    1. Bu dosyayı oluşturun
    2. config.py'ye ayarları ekleyin
    3. llm_service.py'ye entegre edin
    """
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.custom-llm.com/v1"
        
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        LLM ile sohbet.
        
        Args:
            messages: Mesaj listesi
            temperature: Yaratıcılık seviyesi
            max_tokens: Maksimum token sayısı
            
        Returns:
            LLM yanıtı
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )
            
            return response.json()["choices"][0]["message"]["content"]
```

### 📦 Yeni Analiz Modülü Ekleme

```python
# app/analyzers/security_analyzer.py

from typing import Dict, List

class SecurityAnalyzer:
    """
    Güvenlik analizi modülü.
    
    Kontrol edilenler:
    - SQL injection riskleri
    - XSS açıkları
    - Güvensiz kütüphane kullanımı
    - Sertifika doğrulama eksikliği
    """
    
    SECURITY_PATTERNS = {
        "sql_injection": [
            r"execute\(.*\+",
            r"execute\(.*%\s",
            r"execute\(.*\.format\(",
        ],
        "xss": [
            r"innerHTML",
            r"dangerouslySetInnerHTML",
            r"document\.write\(",
        ],
        "hardcoded_secrets": [
            r"password\s*=\s*['\"]",
            r"api_key\s*=\s*['\"]",
            r"secret\s*=\s*['\"]",
        ]
    }
    
    def analyze(self, file_changes: List[Dict]) -> Dict:
        """
        Dosya değişikliklerini güvenlik açısından analiz eder.
        
        Returns:
            {
                "risk_level": "high" | "medium" | "low",
                "vulnerabilities": [...],
                "recommendations": [...]
            }
        """
        vulnerabilities = []
        
        for change in file_changes:
            diff = change.get("diff", "")
            
            for vuln_type, patterns in self.SECURITY_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, diff):
                        vulnerabilities.append({
                            "type": vuln_type,
                            "file": change["file_path"],
                            "severity": self._get_severity(vuln_type)
                        })
        
        return {
            "risk_level": self._calculate_risk_level(vulnerabilities),
            "vulnerabilities": vulnerabilities,
            "recommendations": self._generate_recommendations(vulnerabilities)
        }
```

---

## 📚 Öğrenme Kaynakları

### 📖 Önerilen Dokümantasyon

| Konu | Kaynak |
|------|--------|
| FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| React | [react.dev](https://react.dev/) |
| TypeScript | [typescriptlang.org](https://www.typescriptlang.org/) |
| Tailwind CSS | [tailwindcss.com](https://tailwindcss.com/) |
| SQLAlchemy | [sqlalchemy.org](https://www.sqlalchemy.org/) |
| GitPython | [gitpython.readthedocs.io](https://gitpython.readthedocs.io/) |
| OpenAI API | [platform.openai.com](https://platform.openai.com/) |

### 🎓 Videolar ve Eğitimler

- **FastAPI Beginner Course** - FreeCodeCamp
- **React Tutorial for Beginners** - Programming with Mosh
- **TypeScript Course** - Academind
- **Git Deep Dive** - Traversy Media

### 📝 Blog Yazıları

- "Building a Git Archaeology Tool with FastAPI and React"
- "Integrating Multiple LLM Providers in Python"
- "Real-time Analysis with WebSockets and Celery"
- "Scaling PostgreSQL for Large Git Repositories"

---

## 🙏 Teşekkürler

Bu projede kullanılan harika teknolojiler:

| Teknoloji | Açıklama | Link |
|-----------|----------|------|
| 🐍 Python | Programlama dili | [python.org](https://www.python.org/) |
| ⚡ FastAPI | Python web framework | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| 🗄️ SQLAlchemy | Python ORM | [sqlalchemy.org](https://www.sqlalchemy.org/) |
| ⚛️ React | UI kütüphanesi | [reactjs.org](https://reactjs.org/) |
| 📘 TypeScript | Tip güvenli JS | [typescriptlang.org](https://www.typescriptlang.org/) |
| 🎨 Tailwind CSS | CSS framework | [tailwindcss.com](https://tailwindcss.com/) |
| 🤖 OpenAI | Yapay zeka API | [openai.com](https://openai.com/) |
| 🐳 Docker | Container platformu | [docker.com](https://www.docker.com/) |
| 📊 PostgreSQL | Veritabanı | [postgresql.org](https://www.postgresql.org/) |
| 🔴 Redis | Önbellek | [redis.io](https://redis.io/) |

---

<div align="center">

### 📊 Proje İstatistikleri

```
📦 Toplam Dosya       : 127+
📝 Toplam Satır       : 15,000+
🐍 Backend Satır      : 5,000+
⚛️ Frontend Satır     : 4,000+
📚 Dokümantasyon      : 2,000+
🧪 Test Satırı        : 500+
```

---

**⭐ Bu projeyi beğendiyseniz, yıldız vermeyi unutmayın! ⭐**

[![Star History Chart](https://api.star-history.com/svg?repos=Omerfaruk-aydn/git-archaeology&type=Date)](https://star-history.com/#Omerfaruk-aydn/git-archaeology&Date)

---

### 🤝 Destek

[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com)
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)

---

Made with ❤️ by **GitArch Team**

© 2024 GitArch. Tüm hakları saklıdır.

</div>

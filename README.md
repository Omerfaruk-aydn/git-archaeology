# Git Arkeoloji Aracı (GitArch)

Git depo geçmişini analiz ederek kodun neden, ne zaman ve kim tarafından değiştirildiğini anlayan, bunu doğal dilde açıklayan bir araç.

## Özellikler

- Git depolarını analiz etme
- LLM destekli kod değişiklik analizi
- Kapsamlı rapor oluşturma
- Web tabanlı arayüz
- REST API
- **24+ yapay zeka sağlayıcısı desteği**

## Desteklenen Yapay Zeka Sağlayıcıları

### Bulut Modelleri
| Sağlayıcı | Modeller | SDK |
|---|---|---|
| **OpenAI** | GPT-4o, GPT-4.1 | `openai` |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus | `anthropic` |
| **Google Gemini** | Gemini 2.5 Flash | `google-genai` |
| **Azure OpenAI** | GPT-4o (Azure üzerinden) | `openai` |
| **AWS Bedrock** | Claude, Llama, AI21 (AWS üzerinden) | `boto3` |

### Aggregatör & Router
| Sağlayıcı | Modeller | SDK |
|---|---|---|
| **OpenRouter** | 100+ model (GPT, Claude, Llama, Mistral...) | `openai` (uyumlu) |
| **Together AI** | Llama, Mistral, CodeLlama | `together` |
| **Groq** | Llama 3.3 70B, Mixtral (ultra hızlı) | `groq` |
| **Fireworks AI** | Llama, Mixtral, özel Fine-tune | `fireworks-ai` |
| **DeepInfra** | Uygun fiyatlı bulut inference | `openai` (uyumlu) |

### Avrupa & ABD Sağlayıcıları
| Sağlayıcı | Modeller | SDK |
|---|---|---|
| **Mistral AI** | Mistral Large, Mixtral | `mistralai` |
| **Cohere** | Command R+ | `cohere` |
| **xAI (Grok)** | Grok-2 | `openai` (uyumlu) |
| **Perplexity** | Sonar Pro (internet aramalı) | `openai` (uyumlu) |

### Çin Sağlayıcıları
| Sağlayıcı | Modeller | SDK |
|---|---|---|
| **DeepSeek** | DeepSeek V3, DeepSeek Coder | `openai` (uyumlu) |
| **Baidu (ERNIE)** | ERNIE 4.0 | `qianfan` |
| **Alibaba (Qwen)** | Qwen Plus | `dashscope` |
| **Moonshot (Kimi)** | Moonshot V1 8K | `openai` (uyumlu) |
| **Zhipu AI (GLM)** | GLM-4 | `zhipuai` |
| **MiniMax** | MiniMax-Text-01 | `openai` (uyumlu) |

### Açık Kaynak & Bulut Inference
| Sağlayıcı | Modeller | SDK |
|---|---|---|
| **Hugging Face** | 100.000+ model | `huggingface_hub` |
| **Replicate** | Llama, Stable Diffusion | `replicate` |
| **Cloudflare Workers AI** | Edge tabanlı inference | REST API |
| **Local (Ollama)** | Tüm yerel modeller | REST API |

## Kurulum

### Ön Gereksinimler

- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- Redis 7
- Docker (opsiyonel)

### Hızlı Başlangıç

```bash
# Depoyu klonlayın
git clone https://github.com/yourusername/git-archaeology.git
cd git-archaeology

# .env dosyasını oluşturun
cp .env.example .env

# API anahtarınızı ayarlayın (en az bir tane)
# Örnek: OPENAI_API_KEY=sk-...

# Docker ile çalıştırın
docker-compose up -d
```

### Manuel Kurulum

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Endpoint | Açıklama |
|---|---|
| `GET /api/v1/llm/providers` | Tüm LLM sağlayıcılarını listele |
| `GET /api/v1/llm/providers/available` | Aktif sağlayıcıları listele |
| `POST /api/v1/auth/register` | Kullanıcı kaydı |
| `POST /api/v1/auth/login` | Giriş |
| `GET /api/v1/repositories` | Depoları listele |
| `POST /api/v1/repositories` | Depo ekle |
| `POST /api/v1/analyses` | Analiz başlat |
| `GET /api/v1/reports` | Raporları listele |

## Teknoloji Yığını

- **Backend**: Python, FastAPI, SQLAlchemy, Celery
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Veritabanı**: PostgreSQL
- **Cache**: Redis
- **LLM**: 24+ sağlayıcı (OpenAI, Anthropic, Gemini, Groq, Mistral, DeepSeek, Qwen, vb.)

## Yapılandırma

Tüm yapılandırma ayarları `.env` dosyasında yapılabilir. En az bir LLM sağlayıcı API anahtarı gereklidir.

```bash
# En popüler kombinasyonlar:

# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Groq (en hızlı, ücretsiz tier mevcut)
GROQ_API_KEY=gsk_...

# OpenRouter (100+ modele erişim)
OPENROUTER_API_KEY=sk-or-...

# DeepSeek (uygun fiyatlı)
DEEPSEEK_API_KEY=sk-...

# Yerel model (ücretsiz, API anahtarı gerektirmez)
# LOCAL_LLM_URL=http://localhost:11434
DEFAULT_LLM_PROVIDER=local
```

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

MIT License

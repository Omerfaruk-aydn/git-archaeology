# Ortam Değişkenleri

## Zorunlu Değişkenler

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| DATABASE_URL | PostgreSQL bağlantı URL | postgresql://user:pass@host:5432/db |
| REDIS_URL | Redis bağlantı URL | redis://localhost:6379/0 |
| JWT_SECRET_KEY | JWT anahtarı | your-super-secret-key |

## Opsiyonel Değişkenler

| Değişken | Varsayılan | Açıklama |
|----------|------------|----------|
| DEBUG | false | Debug modu |
| OPENAI_API_KEY | - | OpenAI API anahtarı |
| OPENAI_MODEL | gpt-4o | OpenAI model |
| ANTHROPIC_API_KEY | - | Anthropic API anahtarı |
| ANTHROPIC_MODEL | claude-3-5-sonnet-20241022 | Anthropic model |
| LOCAL_LLM_URL | http://localhost:11434 | Yerel LLM URL |
| LOCAL_LLM_MODEL | llama3 | Yerel LLM model |
| CORS_ORIGINS | ["http://localhost:3000"] | CORS izinleri |
| RATE_LIMIT_PER_MINUTE | 60 | İstek limiti |

## .env Dosyası

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gitarchaeology

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# OpenAI (opsiyonel)
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o

# Anthropic (opsiyonel)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Local LLM (opsiyonel)
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3

# App
DEBUG=true
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

## Güvenlik Notları

- Üretim ortamında JWT_SECRET_KEY mutlaka değiştirilmeli
- API anahtarları commit edilmemeli
- .env dosyası .gitignore'da olmalı
- Hassas veriler loglanmamalı

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Git Archaeology Tool"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///./gitarch.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    REPO_STORAGE_PATH: str = "/data/repos"

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    RATE_LIMIT_PER_MINUTE: int = 60

    DEFAULT_LLM_PROVIDER: str = "openai"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"

    # Google Gemini
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Azure OpenAI
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"
    AZURE_OPENAI_MODEL: str = "gpt-4o"

    # AWS Bedrock
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_BEDROCK_MODEL: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"

    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_MODEL: str = "openai/gpt-4o"

    # Together AI
    TOGETHER_API_KEY: Optional[str] = None
    TOGETHER_MODEL: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

    # Groq
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Mistral AI
    MISTRAL_API_KEY: Optional[str] = None
    MISTRAL_MODEL: str = "mistral-large-latest"

    # Cohere
    COHERE_API_KEY: Optional[str] = None
    COHERE_MODEL: str = "command-r-plus-08-2024"

    # DeepSeek
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # xAI (Grok)
    XAI_API_KEY: Optional[str] = None
    XAI_MODEL: str = "grok-2"

    # Fireworks AI
    FIREWORKS_API_KEY: Optional[str] = None
    FIREWORKS_MODEL: str = "accounts/fireworks/models/llama-v3p1-70b-instruct"

    # Hugging Face
    HF_TOKEN: Optional[str] = None
    HF_MODEL: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"

    # Replicate
    REPLICATE_API_TOKEN: Optional[str] = None
    REPLICATE_MODEL: str = "meta/meta-llama-3-70b-instruct"

    # Baidu Qianfan
    QIANFAN_ACCESS_KEY: Optional[str] = None
    QIANFAN_SECRET_KEY: Optional[str] = None
    QIANFAN_MODEL: str = "ERNIE-4.0-8K"

    # Alibaba DashScope (Qwen)
    DASHSCOPE_API_KEY: Optional[str] = None
    DASHSCOPE_MODEL: str = "qwen-plus"

    # Moonshot (Kimi)
    MOONSHOT_API_KEY: Optional[str] = None
    MOONSHOT_MODEL: str = "moonshot-v1-8k"

    # Zhipu AI (GLM)
    ZHIPUAI_API_KEY: Optional[str] = None
    ZHIPUAI_MODEL: str = "glm-4"

    # MiniMax
    MINIMAX_API_KEY: Optional[str] = None
    MINIMAX_MODEL: str = "MiniMax-Text-01"

    # DeepInfra
    DEEPINFRA_API_KEY: Optional[str] = None
    DEEPINFRA_MODEL: str = "meta-llama/Meta-Llama-3.1-70B-Instruct"

    # Perplexity
    PERPLEXITY_API_KEY: Optional[str] = None
    PERPLEXITY_MODEL: str = "sonar-pro"

    # Cloudflare Workers AI
    CLOUDFLARE_API_TOKEN: Optional[str] = None
    CLOUDFLARE_ACCOUNT_ID: Optional[str] = None
    CLOUDFLARE_MODEL: str = "@cf/meta/llama-3.1-8b-instruct"

    # Local LLM (Ollama / vLLM / LM Studio)
    LOCAL_LLM_URL: str = "http://localhost:11434"
    LOCAL_LLM_MODEL: str = "llama3"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

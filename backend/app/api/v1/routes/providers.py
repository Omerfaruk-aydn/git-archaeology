from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.llm_service import LLMService, PROVIDER_REGISTRY

router = APIRouter(prefix="/llm", tags=["LLM Provider"])

PROVIDER_INFO = {
    "openai": {"name": "OpenAI", "description": "GPT-4o, GPT-4.1 ve diğer OpenAI modelleri", "website": "https://openai.com"},
    "azure": {"name": "Azure OpenAI", "description": "Microsoft Azure üzerinden OpenAI modelleri", "website": "https://azure.microsoft.com/ai"},
    "anthropic": {"name": "Anthropic", "description": "Claude 3.5 Sonnet, Claude 3 Opus ve diğer modeller", "website": "https://anthropic.com"},
    "gemini": {"name": "Google Gemini", "description": "Gemini 2.5 Flash ve diğer Google modelleri", "website": "https://ai.google.dev"},
    "bedrock": {"name": "AWS Bedrock", "description": "AWS üzerinden Anthropic, Meta, AI21 ve diğer modeller", "website": "https://aws.amazon.com/bedrock"},
    "openrouter": {"name": "OpenRouter", "description": "100+ modeli tek API ile erişin (GPT, Claude, Llama, Mistral...)", "website": "https://openrouter.ai"},
    "together": {"name": "Together AI", "description": "Llama, Mistral ve diğer açık kaynak modeller", "website": "https://together.ai"},
    "groq": {"name": "Groq", "description": "Ultra hızlı inference (Llama, Mixtral)", "website": "https://groq.com"},
    "mistral": {"name": "Mistral AI", "description": "Mistral Large, Mistral Medium ve Mixtral", "website": "https://mistral.ai"},
    "cohere": {"name": "Cohere", "description": "Command R+ ve Cohere modelleri", "website": "https://cohere.com"},
    "deepseek": {"name": "DeepSeek", "description": "DeepSeek V3 ve DeepSeek Coder", "website": "https://deepseek.com"},
    "xai": {"name": "xAI (Grok)", "description": "Grok-2 ve xAI modelleri", "website": "https://x.ai"},
    "fireworks": {"name": "Fireworks AI", "description": "Llama, Mixtral ve özel Fine-tune modeller", "website": "https://fireworks.ai"},
    "huggingface": {"name": "Hugging Face", "description": "100.000+ açık kaynak model", "website": "https://huggingface.co"},
    "replicate": {"name": "Replicate", "description": "Bulut tabanlı açık kaynak model çalıştırma", "website": "https://replicate.com"},
    "baidu": {"name": "Baidu (ERNIE)", "description": "ERNIE 4.0 ve Baidu modelleri", "website": "https://cloud.baidu.com"},
    "dashscope": {"name": "Alibaba (Qwen)", "description": "Qwen ve Tongyi modelleri", "website": "https://dashscope.aliyun.com"},
    "moonshot": {"name": "Moonshot (Kimi)", "description": "Kimi ve Moonshot modelleri", "website": "https://moonshot.ai"},
    "zhipuai": {"name": "Zhipu AI (GLM)", "description": "GLM-4 ve Zhipu modelleri", "website": "https://zhipuai.cn"},
    "minimax": {"name": "MiniMax", "description": "MiniMax-Text ve ABAB modelleri", "website": "https://minimax.chat"},
    "deepinfra": {"name": "DeepInfra", "description": "Uygun fiyatlı bulut model inference", "website": "https://deepinfra.com"},
    "perplexity": {"name": "Perplexity", "description": "Sonar modelleri (internet aramalı)", "website": "https://perplexity.ai"},
    "cloudflare": {"name": "Cloudflare Workers AI", "description": "Edge tabanlı model inference", "website": "https://developers.cloudflare.com/workers-ai"},
    "local": {"name": "Local (Ollama)", "description": "Yerel modeller (Ollama, vLLM, LM Studio)", "website": "https://ollama.ai"},
}


@router.get("/providers")
async def list_providers(current_user: User = Depends(get_current_user)):
    providers = []
    for name in sorted(PROVIDER_REGISTRY.keys()):
        info = PROVIDER_INFO.get(name, {"name": name, "description": "", "website": ""})
        providers.append({
            "name": name,
            "display_name": info["name"],
            "description": info["description"],
            "website": info["website"],
            "available": PROVIDER_REGISTRY[name].is_available(),
        })
    return {"providers": providers, "count": len(providers)}


@router.get("/providers/available")
async def list_available_providers(current_user: User = Depends(get_current_user)):
    available = LLMService.get_available_providers()
    return {"providers": available, "count": len(available)}

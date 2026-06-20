import json
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

import httpx
from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

PROVIDER_REGISTRY: Dict[str, type] = {}


def register_provider(name: str):
    def decorator(cls):
        PROVIDER_REGISTRY[name] = cls
        return cls
    return decorator


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        pass

    @abstractmethod
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        pass

    @staticmethod
    def _parse_json(text: str) -> Dict[str, Any]:
        try:
            if "```json" in text:
                json_str = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                json_str = text.split("```")[1].split("```")[0]
            else:
                json_str = text
            return json.loads(json_str.strip())
        except (json.JSONDecodeError, IndexError):
            return {"raw_response": text}


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.3, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)


# ─── OpenAI ──────────────────────────────────────────────

@register_provider("openai")
class OpenAIProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            model=settings.OPENAI_MODEL,
        )

    @staticmethod
    def is_available() -> bool:
        return bool(settings.OPENAI_API_KEY)


# ─── Azure OpenAI ────────────────────────────────────────

@register_provider("azure")
class AzureOpenAIProvider(LLMProvider):
    def __init__(self):
        from openai import AsyncAzureOpenAI
        self.client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )
        self.model = settings.AZURE_OPENAI_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.3, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.AZURE_OPENAI_API_KEY and settings.AZURE_OPENAI_ENDPOINT)


# ─── Anthropic ───────────────────────────────────────────

@register_provider("anthropic")
class AnthropicProvider(LLMProvider):
    def __init__(self):
        import anthropic
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        kwargs = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        response = await self.client.messages.create(**kwargs)
        return response.content[0].text

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.ANTHROPIC_API_KEY)


# ─── Google Gemini ───────────────────────────────────────

@register_provider("gemini")
class GeminiProvider(LLMProvider):
    def __init__(self):
        from google import genai
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        contents = prompt
        config = None
        if system_prompt:
            config = {"system_instruction": system_prompt}
        response = await self.client.aio.models.generate_content(
            model=self.model, contents=contents, config=config,
        )
        return response.text

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.GEMINI_API_KEY)


# ─── AWS Bedrock ─────────────────────────────────────────

@register_provider("bedrock")
class BedrockProvider(LLMProvider):
    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(
            api_key=settings.AWS_SECRET_ACCESS_KEY,
            base_url=f"https://bedrock-runtime.{settings.AWS_REGION}.amazonaws.com",
        )
        self.model = settings.AWS_BEDROCK_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "user", "content": f"{system_prompt}\n\n{prompt}"})
        else:
            messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.3, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY)


# ─── OpenRouter ──────────────────────────────────────────

@register_provider("openrouter")
class OpenRouterProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model=settings.OPENROUTER_MODEL,
        )

    @staticmethod
    def is_available() -> bool:
        return bool(settings.OPENROUTER_API_KEY)


# ─── Together AI ─────────────────────────────────────────

@register_provider("together")
class TogetherProvider(LLMProvider):
    def __init__(self):
        from together import AsyncTogether
        self.client = AsyncTogether(api_key=settings.TOGETHER_API_KEY)
        self.model = settings.TOGETHER_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.3, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.TOGETHER_API_KEY)


# ─── Groq ────────────────────────────────────────────────

@register_provider("groq")
class GroqProvider(LLMProvider):
    def __init__(self):
        from groq import AsyncGroq
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.3, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.GROQ_API_KEY)


# ─── Mistral AI ──────────────────────────────────────────

@register_provider("mistral")
class MistralProvider(LLMProvider):
    def __init__(self):
        from mistralai import MistralAsync
        self.client = MistralAsync(api_key=settings.MISTRAL_API_KEY)
        self.model = settings.MISTRAL_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.complete_async(
            model=self.model, messages=messages, temperature=0.3, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.MISTRAL_API_KEY)


# ─── Cohere ──────────────────────────────────────────────

@register_provider("cohere")
class CohereProvider(LLMProvider):
    def __init__(self):
        import cohere
        self.client = cohere.AsyncClientV2(api_key=settings.COHERE_API_KEY)
        self.model = settings.COHERE_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        kwargs: dict[str, Any] = {"model": self.model, "messages": messages}
        if system_prompt:
            kwargs["preamble"] = system_prompt
        response = await self.client.chat(**kwargs)
        return response.message.content[0].text

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.COHERE_API_KEY)


# ─── DeepSeek ────────────────────────────────────────────

@register_provider("deepseek")
class DeepSeekProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
            model=settings.DEEPSEEK_MODEL,
        )

    @staticmethod
    def is_available() -> bool:
        return bool(settings.DEEPSEEK_API_KEY)


# ─── xAI (Grok) ─────────────────────────────────────────

@register_provider("xai")
class XAIProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            api_key=settings.XAI_API_KEY,
            base_url="https://api.x.ai/v1",
            model=settings.XAI_MODEL,
        )

    @staticmethod
    def is_available() -> bool:
        return bool(settings.XAI_API_KEY)


# ─── Fireworks AI ────────────────────────────────────────

@register_provider("fireworks")
class FireworksProvider(LLMProvider):
    def __init__(self):
        from fireworks.client import AsyncFireworks
        self.client = AsyncFireworks(api_key=settings.FIREWORKS_API_KEY)
        self.model = settings.FIREWORKS_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.3, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.FIREWORKS_API_KEY)


# ─── Hugging Face ────────────────────────────────────────

@register_provider("huggingface")
class HuggingFaceProvider(LLMProvider):
    def __init__(self):
        from huggingface_hub import AsyncInferenceClient
        self.client = AsyncInferenceClient(token=settings.HF_TOKEN)
        self.model = settings.HF_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat_completion(
            model=self.model, messages=messages, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.HF_TOKEN)


# ─── Replicate ───────────────────────────────────────────

@register_provider("replicate")
class ReplicateProvider(LLMProvider):
    def __init__(self):
        import replicate
        self.model = settings.REPLICATE_MODEL
        self._replicate = replicate

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        input_data = {"prompt": prompt}
        if system_prompt:
            input_data["system_prompt"] = system_prompt
        output = await self._replicate.async_run(self.model, input=input_data)
        return "".join(output)

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.REPLICATE_API_TOKEN)


# ─── Baidu Qianfan (ERNIE) ──────────────────────────────

@register_provider("baidu")
class BaiduProvider(LLMProvider):
    def __init__(self):
        import qianfan
        self.client = qianfan.ChatCompletion(
            access_key=settings.QIANFAN_ACCESS_KEY,
            secret_key=settings.QIANFAN_SECRET_KEY,
        )
        self.model = settings.QIANFAN_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        response = await self.client.ado(model=self.model, messages=messages)
        return response["result"]

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.QIANFAN_ACCESS_KEY and settings.QIANFAN_SECRET_KEY)


# ─── Alibaba DashScope (Qwen) ───────────────────────────

@register_provider("dashscope")
class DashScopeProvider(LLMProvider):
    def __init__(self):
        from dashscope.aio import Generation
        self.client = Generation()
        self.model = settings.DASHSCOPE_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        response = await self.client.call(model=self.model, messages=messages)
        return response.output.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.DASHSCOPE_API_KEY)


# ─── Moonshot (Kimi) ────────────────────────────────────

@register_provider("moonshot")
class MoonshotProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            api_key=settings.MOONSHOT_API_KEY,
            base_url="https://api.moonshot.cn/v1",
            model=settings.MOONSHOT_MODEL,
        )

    @staticmethod
    def is_available() -> bool:
        return bool(settings.MOONSHOT_API_KEY)


# ─── Zhipu AI (GLM) ─────────────────────────────────────

@register_provider("zhipuai")
class ZhipuAIProvider(LLMProvider):
    def __init__(self):
        from zhipuai import ZhipuAI
        self.client = ZhipuAI(api_key=settings.ZHIPUAI_API_KEY)
        self.model = settings.ZHIPUAI_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = await self.client.chat.completions.acreate(
            model=self.model, messages=messages, temperature=0.3, max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.ZHIPUAI_API_KEY)


# ─── MiniMax ─────────────────────────────────────────────

@register_provider("minimax")
class MiniMaxProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            api_key=settings.MINIMAX_API_KEY,
            base_url="https://api.minimax.chat/v1",
            model=settings.MINIMAX_MODEL,
        )

    @staticmethod
    def is_available() -> bool:
        return bool(settings.MINIMAX_API_KEY)


# ─── DeepInfra ───────────────────────────────────────────

@register_provider("deepinfra")
class DeepInfraProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            api_key=settings.DEEPINFRA_API_KEY,
            base_url="https://api.deepinfra.com/v1/openai",
            model=settings.DEEPINFRA_MODEL,
        )

    @staticmethod
    def is_available() -> bool:
        return bool(settings.DEEPINFRA_API_KEY)


# ─── Perplexity ──────────────────────────────────────────

@register_provider("perplexity")
class PerplexityProvider(OpenAICompatibleProvider):
    def __init__(self):
        super().__init__(
            api_key=settings.PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai",
            model=settings.PERPLEXITY_MODEL,
        )

    @staticmethod
    def is_available() -> bool:
        return bool(settings.PERPLEXITY_API_KEY)


# ─── Cloudflare Workers AI ───────────────────────────────

@register_provider("cloudflare")
class CloudflareProvider(LLMProvider):
    def __init__(self):
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/{settings.CLOUDFLARE_MODEL}"
        self.token = settings.CLOUDFLARE_API_TOKEN

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.token}"},
                json={"messages": messages},
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["result"]["response"]

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return bool(settings.CLOUDFLARE_API_TOKEN and settings.CLOUDFLARE_ACCOUNT_ID)


# ─── Local (Ollama / vLLM / LM Studio) ──────────────────

@register_provider("local")
class LocalProvider(LLMProvider):
    def __init__(self):
        self.base_url = settings.LOCAL_LLM_URL
        self.model = settings.LOCAL_LLM_MODEL

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt or "",
                    "stream": False,
                },
                timeout=120.0,
            )
            response.raise_for_status()
            return response.json()["response"]

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        result = await self.generate(prompt, system_prompt)
        return self._parse_json(result)

    @staticmethod
    def is_available() -> bool:
        return True


# ─── Service ─────────────────────────────────────────────

class LLMService:
    def __init__(self, provider: str = None, model: Optional[str] = None):
        self.provider_name = provider or settings.DEFAULT_LLM_PROVIDER

        if self.provider_name not in PROVIDER_REGISTRY:
            raise ValueError(
                f"Desteklenmeyen LLM provider: {self.provider_name}. "
                f"Mevcut provider'lar: {', '.join(sorted(PROVIDER_REGISTRY.keys()))}"
            )

        provider_cls = PROVIDER_REGISTRY[self.provider_name]
        if not provider_cls.is_available():
            raise ValueError(
                f"{self.provider_name} API anahtarı yapılandırılmamış. "
                f"Lütfen .env dosyasında gerekli API anahtarını ayarlayın."
            )

        self.provider = provider_cls()

    @staticmethod
    def get_available_providers() -> List[str]:
        return [
            name for name, cls in PROVIDER_REGISTRY.items()
            if cls.is_available()
        ]

    @staticmethod
    def get_all_providers() -> List[Dict[str, Any]]:
        providers = []
        for name, cls in sorted(PROVIDER_REGISTRY.items()):
            providers.append({
                "name": name,
                "available": cls.is_available(),
            })
        return providers

    async def analyze_commit(
        self,
        commit_message: str,
        file_changes: List[Dict[str, Any]],
        focus_areas: List[str],
    ) -> Dict[str, Any]:
        system_prompt = """Sen bir Git arkeoloğu ve kod analiz uzmanısın.
Görevin, Git commit'lerini analiz ederek:
- Kodun neden değiştiğini anlamak
- Değişikliklerin etkilerini değerlendirmek
- Güvenlik, performans ve mimari riskleri tespit etmek
- Gelecekteki bakım için ipuçları sağlamak

Yanıtların her zaman JSON formatında olmalı ve Türkçe yazılmalı."""

        focus_str = ", ".join(focus_areas)
        files_summary = "\n".join([
            f"- {fc.get('file_path', 'unknown')} ({fc.get('change_type', 'unknown')}): +{fc.get('additions', 0)} -{fc.get('deletions', 0)}"
            for fc in file_changes[:15]
        ])

        prompt = f"""Bu commit'u analiz et:

Commit Mesajı: {commit_message}

Değişen Dosyalar:
{files_summary}

Odak Alanları: {focus_str}

Lütfen şu JSON yapısında yanıt ver:
{{
  "summary": "Bu commit'un kısa özeti (1-2 cümle)",
  "category": "security|performance|architecture|dependency|refactor|feature|bugfix|other",
  "importance": "high|medium|low",
  "tags": ["ilgili etiketler"],
  "insights": ["Bu değişiklikle ilgili önemli gözlemler"],
  "related_files": ["İlişkili dosya yolları"],
  "potential_issues": ["Olası sorunlar veya riskler"],
  "recommendations": ["Öneriler"]
}}"""

        return await self.provider.generate_json(prompt, system_prompt)

    async def generate_summary(self, prompt: str) -> Dict[str, Any]:
        system_prompt = """Sen bir Git arkeoloğu ve raporlama uzmanısın.
Verilen analiz sonuçlarını kullanarak kapsamlı ve anlamlı özetler oluştur.
Yanıtların her zaman JSON formatında olmalı ve Türkçe yazılmalı."""

        return await self.provider.generate_json(prompt, system_prompt)

    async def generate_report(self, analysis_data: Dict[str, Any], report_type: str) -> str:
        system_prompt = """Sen bir teknik rapor yazarısın.
Verilen analiz sonuçlarını kullanarak profesyonel ve detaylı raporlar oluştur.
Raporlar Markdown formatında ve Türkçe olmalı."""

        prompts = {
            "full": "Kapsamlı bir arkeolojik analiz raporu oluştur",
            "summary": "Kısa bir özet rapor oluştur",
            "security": "Güvenlik odaklı bir rapor oluştur",
            "architecture": "Mimari analiz raporu oluştur",
            "legacy": "Legacy kod analiz raporu oluştur",
        }

        prompt = f"""{prompts.get(report_type, 'Genel bir rapor oluştur')}

Analiz Verileri:
{json.dumps(analysis_data, indent=2, ensure_ascii=False)}

Raporu şu bölümlerle oluştur:
1. Yönetici Özeti
2. Genel Bakış
3. Detaylı Analiz Bulguları
4. Risk Değerlendirmesi
5. Öneriler
6. Sonuç"""

        return await self.provider.generate(prompt, system_prompt)

    async def explain_change(
        self,
        old_code: str,
        new_code: str,
        commit_message: str,
        file_path: str,
    ) -> str:
        system_prompt = """Sen bir kod arkeoloğusun.
İki kod sürümü arasındaki farkları açıkça ve detaylı şekilde açıkla.
Neden böyle bir değişiklik yapılmış olabileceğini analiz et.
Türkçe yaz."""

        prompt = f"""Bu kod değişikliğini açıkla:

Dosya: {file_path}
Commit Mesajı: {commit_message}

Eski Kod:
```
{old_code[:3000]}
```

Yeni Kod:
```
{new_code[:3000]}
```

Bu değişikliği şu açılardan açıkla:
1. Ne değişti? (Somut değişiklikler)
2. Neden değişti? (Muhtemel sebepler)
3. Etkisi ne? (Kod üzerindeki etki)
4. Riskler neler? (Olası sorunlar)"""

        return await self.provider.generate(prompt, system_prompt)

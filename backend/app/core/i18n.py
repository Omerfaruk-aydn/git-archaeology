from typing import Dict, Any
import json
from pathlib import Path


class I18n:
    def __init__(self, locale: str = "tr"):
        self.locale = locale
        self.translations = self._load_translations()

    def _load_translations(self) -> Dict[str, Any]:
        trans_file = Path(f"locales/{self.locale}.json")
        if trans_file.exists():
            return json.loads(trans_file.read_text(encoding="utf-8"))
        return {}

    def t(self, key: str, **kwargs) -> str:
        value = self.translations.get(key, key)
        if kwargs:
            value = value.format(**kwargs)
        return value

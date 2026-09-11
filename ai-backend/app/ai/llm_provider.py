"""
LLM provider abstraction.

`LLMProvider.generate()` / `generate_json()` are the only two methods the
rest of the codebase ever calls. This means:

- Assessment/RAG/assistant logic never imports `openai` (or any SDK)
  directly.
- Adding a second provider (Anthropic, local Ollama, etc.) means writing
  one new class here and adding a branch in `get_llm_provider()` — nothing
  else changes.
- DEMO_MODE=true (or a missing API key) transparently falls back to
  `DemoLLMProvider`, which never makes a network call, so the whole
  platform is demo-able offline.
"""

from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 800) -> str:
        """Return a free-text completion for `prompt`."""

    @abstractmethod
    def generate_json(
        self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 1500
    ) -> Dict[str, Any]:
        """Return a parsed JSON object. Implementations should ask the model
        for JSON-only output and validate/repair as needed."""


class DemoLLMProvider(LLMProvider):
    """
    A deterministic, offline "LLM".

    It does not call any network API. It produces templated, still-useful
    text (qualitative feedback, assistant answers) so the whole product
    works end-to-end without any credentials — this is what backs
    DEMO_MODE=true. It is intentionally simple: real language generation is
    delegated to a configured OpenAI-compatible provider when available.
    """

    def generate(self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 800) -> str:
        logger.info("DemoLLMProvider.generate called (no external API used).")
        return (
            "This is a templated response generated in DEMO_MODE (no LLM API key configured). "
            "The underlying data and scoring behind this answer are real and computed by the "
            "platform's deterministic engines; only this sentence of natural-language phrasing "
            "is a placeholder."
        )

    def generate_json(
        self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 1500
    ) -> Dict[str, Any]:
        logger.info("DemoLLMProvider.generate_json called (no external API used).")
        return {"demo_mode": True, "message": "No LLM configured; structured demo logic was used instead."}


class OpenAIProvider(LLMProvider):
    """Calls an OpenAI-compatible Chat Completions endpoint."""

    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set.")
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("The 'openai' package is not installed.") from exc
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
        self._model = settings.OPENAI_MODEL

    def generate(self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 800) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = self._client.chat.completions.create(
            model=self._model, messages=messages, max_tokens=max_tokens, temperature=0.4
        )
        return response.choices[0].message.content or ""

    def generate_json(
        self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 1500
    ) -> Dict[str, Any]:
        json_system = (system or "") + (
            "\nRespond with ONLY a single valid JSON object. No markdown fences, no preamble."
        )
        raw = self.generate(prompt, system=json_system, max_tokens=max_tokens)
        return _parse_json_with_repair(raw, self)


class AnthropicProvider(LLMProvider):
    """Calls the Anthropic Messages API (Claude)."""

    def __init__(self) -> None:
        if not settings.ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY is not set.")
        try:
            from anthropic import Anthropic
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("The 'anthropic' package is not installed.") from exc
        self._client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self._model = settings.ANTHROPIC_MODEL

    def generate(self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 800) -> str:
        kwargs: Dict[str, Any] = {
            "model": self._model,
            "max_tokens": max_tokens,
            "temperature": 0.4,
            "messages": [{"role": "user", "content": prompt}],
        }
        # Anthropic takes the system prompt as a top-level parameter rather
        # than as a message with role="system".
        if system:
            kwargs["system"] = system
        response = self._client.messages.create(**kwargs)
        return "".join(block.text for block in response.content if block.type == "text")

    def generate_json(
        self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 1500
    ) -> Dict[str, Any]:
        json_system = (system or "") + (
            "\nRespond with ONLY a single valid JSON object. No markdown fences, no preamble."
        )
        raw = self.generate(prompt, system=json_system, max_tokens=max_tokens)
        return _parse_json_with_repair(raw, self)


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text.strip(), flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text.strip()).strip()
    return text


def _parse_json_with_repair(raw: str, provider: LLMProvider, retries: int = 1) -> Dict[str, Any]:
    """Try to parse `raw` as JSON; on failure ask the LLM to repair it."""
    candidate = _strip_code_fences(raw)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    # attempt to locate the outermost {...} block
    match = re.search(r"\{.*\}", candidate, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    if retries > 0:
        repair_prompt = (
            "The following text was supposed to be valid JSON but failed to parse. "
            "Return ONLY the corrected, valid JSON object, nothing else:\n\n" + candidate
        )
        repaired = provider.generate(repair_prompt, max_tokens=1500)
        return _parse_json_with_repair(repaired, provider, retries=retries - 1)

    raise ValueError("LLM did not return valid JSON after repair attempts.")


_PROVIDERS = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
}


def get_llm_provider() -> LLMProvider:
    """Factory used by every service that needs an LLM."""
    if settings.DEMO_MODE:
        return DemoLLMProvider()

    provider_cls = _PROVIDERS.get(settings.LLM_PROVIDER.lower())
    if provider_cls is None:
        if settings.LLM_PROVIDER.lower() != "demo":
            logger.warning(
                "Unknown LLM_PROVIDER=%r (expected one of: demo, %s). Using DemoLLMProvider.",
                settings.LLM_PROVIDER,
                ", ".join(sorted(_PROVIDERS)),
            )
        return DemoLLMProvider()

    try:
        return provider_cls()
    except Exception as exc:  # noqa: BLE001
        # A missing key or SDK must degrade to the offline provider rather
        # than take the whole API down mid-demo.
        logger.warning("Falling back to DemoLLMProvider: %s", exc)
        return DemoLLMProvider()

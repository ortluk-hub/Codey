"""FastAPI UI entrypoint for Cody."""

from cody.config import DEFAULT_SETTINGS
from cody.llm import LLMRouter, OllamaClient
from cody.status import get_phase_1_status, get_phase_2_status


def _build_router() -> LLMRouter:
    return LLMRouter(
        intent_client=OllamaClient(DEFAULT_SETTINGS.ollama_intent_url),
        primary_client=OllamaClient(DEFAULT_SETTINGS.ollama_primary_url),
        fallback_client=OllamaClient(DEFAULT_SETTINGS.ollama_fallback_url),
    )


try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:
    FastAPI = None
    BaseModel = object


if FastAPI:
    app = FastAPI(title="Cody API UI")

    class ChatRequest(BaseModel):
        message: str

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "service": "cody"}

    @app.get("/status")
    def status() -> dict:
        return {"phase_1": get_phase_1_status(), "phase_2": get_phase_2_status()}

    @app.post("/chat")
    def chat(body: ChatRequest) -> dict:
        return _build_router().route_chat(body.message)
else:
    app = None


def main() -> None:
    if app is None:
        print("FastAPI/uvicorn not installed. Install requirements and run: python -m cody.api_ui")
        return

    try:
        import uvicorn
    except ImportError:
        print("uvicorn not installed. Install uvicorn and rerun.")
        return

    uvicorn.run("cody.api_ui:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()

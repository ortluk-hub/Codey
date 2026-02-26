#FastAPI UI entrypoint for Cody.

from textwrap import dedent

from config import DEFAULT_SETTINGS
from llm import LLMRouter, OllamaClient
from status import get_phase_1_status, get_phase_2_status, get_phase_3_status


def _build_router() -> LLMRouter:
    return LLMRouter(
        intent_client=OllamaClient(DEFAULT_SETTINGS.ollama_intent_url),
        primary_client=OllamaClient(DEFAULT_SETTINGS.ollama_primary_url),
        fallback_client=OllamaClient(DEFAULT_SETTINGS.ollama_fallback_url),
    )


try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel
except ImportError:
    FastAPI = None
    HTMLResponse = None
    BaseModel = object


def render_chat_page() -> str:
    """Render a lightweight in-browser chat client for the /chat API."""

    return dedent(
        """\
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Cody Chat</title>
            <style>
              :root {
                color-scheme: light dark;
                font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
              }
              body {
                margin: 0;
                padding: 24px;
                background: #0b1020;
                color: #eef2ff;
              }
              .chat {
                margin: 0 auto;
                max-width: 820px;
                background: #141b34;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 16px;
              }
              #log {
                min-height: 320px;
                max-height: 56vh;
                overflow-y: auto;
                padding: 12px;
                border-radius: 8px;
                background: #020617;
                margin-bottom: 12px;
              }
              .message {
                margin: 0 0 10px;
                line-height: 1.4;
              }
              .user { color: #7dd3fc; }
              .assistant { color: #c4b5fd; }
              form { display: flex; gap: 8px; }
              input {
                flex: 1;
                border-radius: 8px;
                border: 1px solid #475569;
                padding: 10px 12px;
                background: #0f172a;
                color: #e2e8f0;
              }
              button {
                border: 0;
                border-radius: 8px;
                padding: 10px 16px;
                background: #2563eb;
                color: white;
                cursor: pointer;
              }
            </style>
          </head>
          <body>
            <main class="chat">
              <h1>Cody Chat</h1>
              <div id="log" aria-live="polite"></div>
              <form id="chat-form">
                <input id="message" autocomplete="off" placeholder="Ask Cody for coding help..." required />
                <button type="submit">Send</button>
              </form>
            </main>
            <script>
              const log = document.getElementById('log');
              const form = document.getElementById('chat-form');
              const input = document.getElementById('message');

              const append = (role, content) => {
                const p = document.createElement('p');
                p.className = `message ${role}`;
                p.textContent = `${role === 'user' ? 'You' : 'Cody'}: ${content}`;
                log.appendChild(p);
                log.scrollTop = log.scrollHeight;
              };

              form.addEventListener('submit', async (event) => {
                event.preventDefault();
                const message = input.value.trim();
                if (!message) return;
                append('user', message);
                input.value = '';

                try {
                  const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'content-type': 'application/json' },
                    body: JSON.stringify({ message }),
                  });
                  const data = await response.json();
                  append('assistant', `${data.reply} [${data.provider}]`);
                } catch (error) {
                  append('assistant', `Request failed: ${error}`);
                }
              });
            </script>
          </body>
        </html>
        """
    )


if FastAPI:
    app = FastAPI(title="Cody API UI")

    class ChatRequest(BaseModel):
        message: str

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "service": "cody"}

    @app.get("/", response_class=HTMLResponse)
    def chat_ui() -> str:
        return render_chat_page()

    @app.get("/status")
    def status() -> dict:
        return {"phase_1": get_phase_1_status(), "phase_2": get_phase_2_status(), "phase_3": get_phase_3_status()}

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

    uvicorn.run("api_ui:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
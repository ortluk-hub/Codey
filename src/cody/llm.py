"""LLM plumbing for Ollama-backed routing with resilient fallbacks and tool execution."""

from dataclasses import dataclass, field
import json
import logging
import re
import uuid
from urllib import error, request

from . import sandbox


@dataclass
class ToolExecutor:
    """Executes code in the sandbox and returns results."""

    logger: logging.Logger = field(default_factory=lambda: logging.getLogger("cody.llm.tools"))

    def execute_python(self, code: str, request_id: str) -> dict:
        """Execute Python code in the sandbox."""
        self.logger.info(
            "tool.execute.start request_id=%s tool=python code_length=%s",
            request_id,
            len(code),
        )
        result = sandbox.run_python_in_docker(code)
        if result.get("ok"):
            self.logger.info(
                "tool.execute.success request_id=%s tool=python exit_code=%s",
                request_id,
                result.get("exit_code"),
            )
        else:
            self.logger.info(
                "tool.execute.error request_id=%s tool=python error=%s",
                request_id,
                result.get("error", "unknown"),
            )
        return result


def extract_code_block(text: str) -> str | None:
    """Extract Python code from markdown code blocks."""
    # Match ```python ... ``` or ``` ... ```
    pattern = r"```(?:python)?\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


@dataclass
class OllamaClient:
    endpoint: str | None
    timeout: float = 30.0  # Increased timeout for larger models

    def chat(self, message: str, model: str) -> str | None:
        if not self.endpoint:
            return None

        payload = json.dumps({"model": model, "prompt": message, "stream": False}).encode()
        req = request.Request(
            self.endpoint.rstrip("/") + "/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            return data.get("response")
        except (error.URLError, TimeoutError, json.JSONDecodeError):
            return None


@dataclass
class LLMRouter:
    intent_client: OllamaClient
    primary_client: OllamaClient
    fallback_client: OllamaClient
    tool_executor: ToolExecutor = field(default_factory=ToolExecutor)

    intent_model: str = "qwen3:0.6b"
    primary_model: str = "qwen3-coder:480b-cloud"
    fallback_model: str = "deepseek-coder:6.7b"
    pending_messages: list[str] = field(default_factory=list)
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger("cody.llm"))

    def _resolve_intent(self, message: str, request_id: str) -> tuple[str, bool]:
        """Use keyword matching to detect simple computation requests.

        Returns:
            Tuple of (code_or_prompt, can_handle_with_tools)
        """
        message_lower = message.lower().strip()
        
        # Pattern 1: "what is <math expression>" with numbers and operators
        import re
        math_pattern = r'^what is\s+([\d\s\+\-\*\/\(\)\.]+)\??$'
        match = re.match(math_pattern, message_lower)
        
        if match:
            expression = match.group(1).strip()
            code = f"print({expression})"
            self.logger.info(
                "llm.intent.tool_request request_id=%s expression=%s",
                request_id,
                expression,
            )
            return code, True
        
        # Pattern 2: "what is <number> divided by <number>"
        div_pattern = r'^what is\s+(\d+)\s+divided\s+by\s+(\d+)\??$'
        match = re.match(div_pattern, message_lower)
        
        if match:
            num1, num2 = match.groups()
            code = f"print({num1} / {num2})"
            self.logger.info(
                "llm.intent.tool_request request_id=%s expression=%s/%s",
                request_id,
                num1,
                num2,
            )
            return code, True
        
        # Everything else goes to LLM
        self.logger.info(
            "llm.intent.llm_routing request_id=%s",
            request_id,
        )
        return "You are Cody, a helpful coding assistant. Provide clear, accurate answers.", False

    def _execute_tool_and_respond(self, code: str, request_id: str) -> dict:
        """Execute code directly and return result without using cloud."""
        result = self.tool_executor.execute_python(code, request_id)
        if result.get("ok"):
            output = result.get("stdout", "").strip() or result.get("stderr", "").strip()
            return {
                "reply": f"Result:\n```\n{output}\n```",
                "provider": "local-tool",
                "executed_code": code,
                "exit_code": result.get("exit_code"),
            }
        else:
            error_msg = result.get("stderr", result.get("message", "Unknown error"))
            return {
                "reply": f"Error executing code:\n```\n{error_msg}\n```",
                "provider": "local-tool-error",
                "executed_code": code,
            }

    def _compose_message(self, message: str) -> str:
        if not self.pending_messages:
            return message

        queued_messages = "\n".join(f"- {queued}" for queued in self.pending_messages)
        return (
            "System note: these user messages were queued while no LLM provider was available. "
            "Please process them as oldest-to-newest context before answering the latest request.\n\n"
            f"Queued messages:\n{queued_messages}\n\n"
            f"Latest user message:\n{message}"
        )

    def _route_to_provider(
        self, message: str, system_prompt: str, request_id: str
    ) -> tuple[str | None, str | None]:
        """Send message with system prompt to primary/fallback providers."""
        full_message = f"{system_prompt}\n\nUser: {message}"

        self.logger.info(
            "llm.call.start request_id=%s provider=%s model=%s",
            request_id,
            "ollama-cloud",
            self.primary_model,
        )
        primary_reply = self.primary_client.chat(full_message, model=self.primary_model)
        if primary_reply:
            self.logger.info(
                "llm.call.success request_id=%s provider=%s model=%s",
                request_id,
                "ollama-cloud",
                self.primary_model,
            )
            return primary_reply, "ollama-cloud"
        self.logger.info(
            "llm.call.unavailable request_id=%s provider=%s model=%s",
            request_id,
            "ollama-cloud",
            self.primary_model,
        )

        self.logger.info(
            "llm.call.start request_id=%s provider=%s model=%s",
            request_id,
            "ollama-local",
            self.fallback_model,
        )
        fallback_reply = self.fallback_client.chat(full_message, model=self.fallback_model)
        if fallback_reply:
            self.logger.info(
                "llm.call.success request_id=%s provider=%s model=%s",
                request_id,
                "ollama-local",
                self.fallback_model,
            )
            return fallback_reply, "ollama-local"
        self.logger.info(
            "llm.call.unavailable request_id=%s provider=%s model=%s",
            request_id,
            "ollama-local",
            self.fallback_model,
        )

        return None, None

    def route_chat(self, message: str, request_id: str | None = None, recipient: str = "unknown") -> dict:
        """Route a chat message through intent resolver to tools or LLM."""
        trace_id = request_id or uuid.uuid4().hex
        self.logger.info(
            "llm.request.received request_id=%s recipient=%s queued_messages=%s",
            trace_id,
            recipient,
            len(self.pending_messages),
        )

        # Stage 1: Resolve intent with tiny model
        intent_result, can_handle_with_tools = self._resolve_intent(message, request_id=trace_id)

        # Stage 1b: If intent resolver detected a tool opportunity, execute directly
        if can_handle_with_tools:
            self.logger.info(
                "llm.intent.tool_executing request_id=%s",
                trace_id,
            )
            return self._execute_tool_and_respond(intent_result, trace_id)

        # Stage 2: Send to primary/fallback with system prompt
        composed_message = self._compose_message(message)
        reply, provider = self._route_to_provider(
            composed_message, intent_result, request_id=trace_id
        )

        if reply and provider:
            self.pending_messages.clear()
            self.logger.info(
                "llm.response.sent request_id=%s recipient=%s provider=%s queued_messages=%s",
                trace_id,
                recipient,
                provider,
                len(self.pending_messages),
            )
            return {"reply": reply, "provider": provider}

        # All providers failed - queue message and return stub
        self.pending_messages.append(message)
        self.logger.info(
            "llm.response.sent request_id=%s recipient=%s provider=%s queued_messages=%s",
            trace_id,
            recipient,
            "stub",
            len(self.pending_messages),
        )
        return {
            "reply": f"[stub] Cody saved your message while providers are unavailable: {message}",
            "provider": "stub",
            "queued": True,
            "queued_messages": len(self.pending_messages),
        }

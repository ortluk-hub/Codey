"""Core project model for Cody/Codey agent architecture."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    """Defines a model backend served by Ollama."""

    role: str
    model: str
    served_via: str = "ollama"


@dataclass(frozen=True)
class MemoryStrategy:
    """Defines short-term and long-term memory responsibilities."""

    short_term: str
    long_term: str


@dataclass(frozen=True)
class RuntimePolicy:
    """Runtime policy for tool usage and process isolation."""

    tools_available: bool
    filesystem_access: str
    execution_boundary: str


@dataclass(frozen=True)
class AgentArchitecture:
    """Canonical architecture for the Cody coding agent."""

    name: str
    mission: str
    modular: bool
    intent_resolver: LLMConfig
    primary_llm: LLMConfig
    fallback_llm: LLMConfig
    runtime_policy: RuntimePolicy
    memory: MemoryStrategy



def get_agent_architecture() -> AgentArchitecture:
    """Return the architecture contract for Cody."""

    return AgentArchitecture(
        name="Cody",
        mission="A modular coding agent for containerized sandbox execution.",
        modular=True,
        intent_resolver=LLMConfig(
            role="intent_resolver_and_tool_caller",
            model="small-llm",
        ),
        primary_llm=LLMConfig(
            role="main_reasoning",
            model="qwen3-coder:480b-cloud",
        ),
        fallback_llm=LLMConfig(
            role="local_fallback",
            model="qwen2.5:1.5b",
        ),
        runtime_policy=RuntimePolicy(
            tools_available=True,
            filesystem_access="containerized_sandbox",
            execution_boundary="restricted_to_assigned_context",
        ),
        memory=MemoryStrategy(
            short_term="full_context_window",
            long_term="summarized_memory",
        ),
    )

"""Core project model for Cody/Codey agent framework."""

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
    code_execution_environment: str


@dataclass(frozen=True)
class CommunicationConfig:
    """External communication channels for the agent."""

    tcp_port: int
    web_ui: str


@dataclass(frozen=True)
class AgentArchitecture:
    """Canonical architecture for the Cody coder agent framework."""

    name: str
    mission: str
    modular: bool
    intent_resolver: LLMConfig
    primary_llm: LLMConfig
    fallback_llm: LLMConfig
    runtime_policy: RuntimePolicy
    memory: MemoryStrategy
    communication: CommunicationConfig


@dataclass(frozen=True)
class RoadmapMilestone:
    """Represents a planned milestone for the Cody framework."""

    phase: str
    focus: str
    outcomes: tuple[str, ...]



def get_agent_architecture() -> AgentArchitecture:
    """Return the architecture contract for Cody."""

    return AgentArchitecture(
        name="Cody",
        mission="A modular coder agent with TCP communication and sandboxed execution.",
        modular=True,
        intent_resolver=LLMConfig(
            role="intent_resolver",
            model="ollama-local-tiny",
        ),
        primary_llm=LLMConfig(
            role="main_reasoning",
            model="ollama-cloud",
        ),
        fallback_llm=LLMConfig(
            role="local_fallback",
            model="ollama-local",
        ),
        runtime_policy=RuntimePolicy(
            tools_available=True,
            filesystem_access="containerized_sandbox",
            execution_boundary="restricted_to_assigned_context",
            code_execution_environment="docker",
        ),
        memory=MemoryStrategy(
            short_term="full_context_window",
            long_term="summarized_memory",
        ),
        communication=CommunicationConfig(
            tcp_port=8888,
            web_ui="fastapi_chat_with_provider_badges",
        ),
    )


def get_roadmap() -> tuple[RoadmapMilestone, ...]:
    """Return the near-term roadmap for Cody."""

    return (
        RoadmapMilestone(
            phase="Phase 1: Foundation hardening",
            focus="Stabilize core architecture contract and runtime constraints.",
            outcomes=(
                "Lock communication contract for TCP port 8888 and FastAPI chat UI.",
                "Validate Docker sandbox runtime policies through automated unit checks.",
                "Keep modular architecture metadata versioned through changelog updates.",
            ),
        ),
        RoadmapMilestone(
            phase="Phase 2: Tooling and memory maturity",
            focus="Expand capability coverage while preserving predictable behavior.",
            outcomes=(
                "Broaden tool contract to support richer coding workflows.",
                "Refine summarized long-term memory strategy quality controls.",
                "Add test coverage around architecture regressions and memory expectations.",
            ),
        ),
        RoadmapMilestone(
            phase="Phase 3: Delivery and operator visibility",
            focus="Improve deployment ergonomics and operational confidence.",
            outcomes=(
                "Expose roadmap-aligned status reporting in project documentation.",
                "Define release readiness criteria for model fallback behavior.",
                "Document production runbooks for Cody service operators.",
            ),
        ),
    )

"""Core project model for Cody/Codey agent framework."""

from dataclasses import dataclass
from pathlib import Path


def _get_changelog_path() -> Path:
    """Resolve CHANGELOG.md from the project root."""
    this_file = Path(__file__).resolve()
    for parent in this_file.parents:
        candidate = parent / "CHANGELOG.md"
        if candidate.exists():
            return candidate
    return this_file.parents[2] / "CHANGELOG.md"


def _count_changelog_versions() -> int:
    """Count version headers in CHANGELOG.md."""
    changelog = _get_changelog_path()
    if not changelog.exists():
        return 0
    content = changelog.read_text(encoding="utf-8")
    return sum(1 for line in content.splitlines() if line.startswith("## ["))


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


@dataclass(frozen=True)
class PhaseStatus:
    """Represents completion state for a roadmap phase."""

    phase: str
    completed: bool
    checks: tuple[str, ...]



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


def get_phase_1_status() -> PhaseStatus:
    """Evaluate completion status for Phase 1 foundation hardening goals."""

    architecture = get_agent_architecture()
    has_communication_contract = (
        architecture.communication.tcp_port == 8888
        and architecture.communication.web_ui == "fastapi_chat_with_provider_badges"
    )
    has_runtime_constraints = (
        architecture.runtime_policy.code_execution_environment == "docker"
        and architecture.runtime_policy.tools_available
        and architecture.runtime_policy.filesystem_access == "containerized_sandbox"
    )
    has_versioned_phase_metadata = architecture.modular and _count_changelog_versions() >= 1

    checks = (
        "Communication contract fixed to TCP port 8888 and FastAPI chat UI."
        if has_communication_contract
        else "Communication contract is not fully aligned with Phase 1.",
        "Runtime policy enforces Docker-based sandbox execution with tool access."
        if has_runtime_constraints
        else "Runtime policy does not fully satisfy Phase 1 sandbox expectations.",
        "Architecture remains modular with versioned roadmap metadata."
        if has_versioned_phase_metadata
        else "Architecture metadata is missing expected Phase 1 versioning signals.",
    )

    return PhaseStatus(
        phase="Phase 1: Foundation hardening",
        completed=(
            has_communication_contract
            and has_runtime_constraints
            and has_versioned_phase_metadata
        ),
        checks=checks,
    )


def get_phase_2_status() -> PhaseStatus:
    """Evaluate completion status for Phase 2 tooling and memory maturity goals."""

    architecture = get_agent_architecture()
    roadmap = get_roadmap()

    has_tooling_contract = (
        architecture.runtime_policy.tools_available
        and architecture.runtime_policy.execution_boundary
        == "restricted_to_assigned_context"
    )
    has_memory_quality_controls = (
        architecture.memory.long_term == "summarized_memory"
        and architecture.memory.short_term == "full_context_window"
    )
    has_regression_coverage_signals = any(
        milestone.phase.startswith("Phase 2")
        and any("test coverage" in outcome.lower() for outcome in milestone.outcomes)
        and any("memory" in outcome.lower() for outcome in milestone.outcomes)
        for milestone in roadmap
    )

    checks = (
        "Tooling contract supports controlled coding workflows through enabled tools and execution boundaries."
        if has_tooling_contract
        else "Tooling contract is not fully aligned with Phase 2 workflow requirements.",
        "Memory strategy pairs summarized long-term memory with full-context short-term retention."
        if has_memory_quality_controls
        else "Memory strategy does not fully satisfy Phase 2 quality-control expectations.",
        "Roadmap tracks Phase 2 regression coverage across architecture and memory expectations."
        if has_regression_coverage_signals
        else "Roadmap metadata is missing Phase 2 regression and memory coverage signals.",
    )

    return PhaseStatus(
        phase="Phase 2: Tooling and memory maturity",
        completed=(
            has_tooling_contract
            and has_memory_quality_controls
            and has_regression_coverage_signals
        ),
        checks=checks,
    )


def get_phase_3_status() -> PhaseStatus:
    """Evaluate completion status for Phase 3 delivery and operator visibility goals."""

    architecture = get_agent_architecture()
    roadmap = get_roadmap()

    has_status_visibility = architecture.modular and any(
        milestone.phase.startswith("Phase 3")
        and any("status reporting" in outcome.lower() for outcome in milestone.outcomes)
        for milestone in roadmap
    )
    has_release_readiness_criteria = any(
        milestone.phase.startswith("Phase 3")
        and any("release readiness" in outcome.lower() for outcome in milestone.outcomes)
        and any("fallback" in outcome.lower() for outcome in milestone.outcomes)
        for milestone in roadmap
    )
    has_operator_runbook_signal = any(
        milestone.phase.startswith("Phase 3")
        and any("runbooks" in outcome.lower() for outcome in milestone.outcomes)
        and any("operators" in outcome.lower() for outcome in milestone.outcomes)
        for milestone in roadmap
    )

    checks = (
        "Phase 3 roadmap captures status-reporting visibility requirements for operators."
        if has_status_visibility
        else "Phase 3 visibility requirements are not fully represented in roadmap metadata.",
        "Phase 3 roadmap defines release readiness criteria for fallback model behavior."
        if has_release_readiness_criteria
        else "Phase 3 roadmap is missing release-readiness fallback criteria.",
        "Phase 3 roadmap includes production runbook guidance for Cody operators."
        if has_operator_runbook_signal
        else "Phase 3 roadmap lacks operator-facing production runbook guidance.",
    )

    return PhaseStatus(
        phase="Phase 3: Delivery and operator visibility",
        completed=(
            has_status_visibility
            and has_release_readiness_criteria
            and has_operator_runbook_signal
        ),
        checks=checks,
    )

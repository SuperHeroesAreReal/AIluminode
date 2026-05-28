from __future__ import annotations

from dataclasses import dataclass


PROTECTION_MARKERS = (
    "without",
    "do not",
    "don't",
    "avoid",
    "protect",
    "leave",
    "preserve",
    "no ",
)


@dataclass(frozen=True)
class RouteDecision:
    route: str
    polarity: str
    reason: str


@dataclass(frozen=True)
class EegReport:
    trace_id: str
    active_terrain: list[str]
    stance: str
    compass_guidance: list[str]
    route_decisions: list[RouteDecision]
    drift_risk: list[str]
    next_safe_action: str


def scan(prompt: str) -> EegReport:
    clean_prompt = prompt.strip()
    lower_prompt = clean_prompt.lower()
    active_terrain = _detect_terrain(lower_prompt)
    stance = _detect_stance(lower_prompt, active_terrain)
    compass_guidance = _compass_guidance(active_terrain)
    route_decisions = _route_decisions(lower_prompt, active_terrain, compass_guidance)
    drift_risk = _drift_risk(lower_prompt, active_terrain)

    return EegReport(
        trace_id=f"ailuminode_{_stable_trace_suffix(clean_prompt)}",
        active_terrain=active_terrain,
        stance=stance,
        compass_guidance=compass_guidance,
        route_decisions=route_decisions,
        drift_risk=drift_risk,
        next_safe_action=_next_safe_action(stance, drift_risk, route_decisions),
    )


def render(report: EegReport) -> str:
    return "\n".join(
        [
            f"AIluminode TRACE {report.trace_id}",
            "",
            "ACTIVE_TERRAIN:",
            *_bullets(report.active_terrain),
            "",
            "STANCE:",
            report.stance,
            "",
            "COMPASS_GUIDANCE:",
            *_bullets(report.compass_guidance),
            "",
            "ROUTE_POLARITY:",
            *[
                f"- {decision.polarity}: {decision.route} ({decision.reason})"
                for decision in report.route_decisions
            ],
            "",
            "DRIFT_RISK:",
            *_bullets(report.drift_risk),
            "",
            "NEXT_SAFE_ACTION:",
            report.next_safe_action,
        ]
    )


def _detect_terrain(prompt: str) -> list[str]:
    terrain: list[str] = []
    if _contains_any(prompt, "paula", "memory", "sqlite", "vector", "chroma", "logs"):
        terrain.append("paula_memory_pipeline")
    if _contains_any(prompt, "topography", "terrain", "switchbox", "airlock", "orientation"):
        terrain.append("contextual_topography")
    if _contains_any(prompt, "ohbuoy", "recce", "plotter", "s+r", "search and rescue"):
        terrain.append("nodaiity_s+r")
    if _contains_any(prompt, "epub", "book", "chapter", "section", "source", "shared", "books"):
        terrain.append("source_terrain")
    if _contains_any(prompt, "code", "refactor", "test", "compile", ".kt", ".py", "repo"):
        terrain.append("codebase")
    return _distinct(terrain) or ["general_context"]


def _detect_stance(prompt: str, terrain: list[str]) -> str:
    if _contains_any(prompt, "audit", "check", "inspect", "trace", "recce"):
        return "reconnaissance"
    if _contains_any(prompt, "fix", "refactor", "patch", "remove", "wire", "add"):
        return "surgical_refactor"
    if _contains_any(prompt, "explain", "what happens", "possibilities", "outcomes"):
        return "explainer"
    if "source_terrain" in terrain:
        return "bounded_source_reader"
    return "orientation"


def _compass_guidance(terrain: list[str]) -> list[str]:
    if "paula_memory_pipeline" not in terrain:
        return []
    return [
        "route=paula_memory_pipeline",
        "howler=RECENT_SQLITE_MEMORY bypasses STANCE_GATE and TERRAIN_GATE.",
        "likely_fix=Move recent memory retrieval behind topology filtering.",
        "codex_targets=prompt assembly,recent conversation loader,sqlite retrieval function,topography packet builder",
    ]


def _route_decisions(prompt: str, terrain: list[str], compass_guidance: list[str]) -> list[RouteDecision]:
    decisions = [
        RouteDecision("current_prompt", "OPEN", "declared task is the active entry point"),
    ]

    if "paula_memory_pipeline" in terrain:
        decisions.append(RouteDecision("paula_memory_files", "OPEN", "Paula memory terrain is active"))
    if "contextual_topography" in terrain:
        decisions.append(RouteDecision("topology_packet", "OPEN", "topography or route language is active"))
    if "nodaiity_s+r" in terrain:
        decisions.append(RouteDecision("s+r_doctrine", "OPEN", "S+R doctrine is explicitly named"))
    if "source_terrain" in terrain:
        decisions.append(RouteDecision("bounded_source_index", "OPEN", "source terrain is active; use bounded source access"))
    if "codebase" in terrain:
        decisions.append(RouteDecision("declared_code_surface", "OPEN", "code work is explicitly requested"))

    decisions.append(_memory_route(prompt, "saved_memory", "save", "saving", "saved memory"))
    decisions.append(_memory_route(prompt, "vector_memory", "vector", "learn", "ingest"))
    decisions.append(_archive_route(prompt))
    decisions.append(_full_source_route(prompt))
    decisions.append(_dashboard_route(prompt))

    if compass_guidance:
        decisions.extend(
            RouteDecision(f"compass:{target}", "AUDIT", "Compass target for observed propagation drift")
            for target in (
                "prompt_assembly",
                "recent_conversation_loader",
                "sqlite_retrieval_function",
                "topography_packet_builder",
            )
        )

    decisions.append(RouteDecision("autonomous_crawling", "BLOCK", "AIluminode stays declared-task only"))
    decisions.append(RouteDecision("telemetry_empire", "BLOCK", "no telemetry, retention, or dashboard drift"))

    if "source_terrain" not in terrain:
        decisions.append(RouteDecision("literary_terrain", "BLOCK", "book/source terrain is not active"))
    if not _contains_any(prompt, "creative", "roleplay", "fiction", "book"):
        decisions.append(RouteDecision("creative_immersion", "BLOCK", "creative terrain was not requested"))
    if _contains_any(prompt, "rewrite from scratch", "rebuild"):
        decisions.append(RouteDecision("full_rewrite", "AUDIT", "large rewrite language requires explicit confirmation"))
    else:
        decisions.append(RouteDecision("full_rewrite", "BLOCK", "preserve surgical change boundaries"))

    return _distinct_decisions(decisions)


def _drift_risk(prompt: str, terrain: list[str]) -> list[str]:
    risks: list[str] = []
    if "source_terrain" in terrain:
        risks.append("source_terrain_mistaken_for_memory")
    if "paula_memory_pipeline" in terrain and "source_terrain" in terrain:
        risks.append("book_context_bleeding_into_primary_continuity")
    if _contains_any(prompt, "personality", "stance", "identity", "who am i"):
        risks.append("stance_identity_overlap")
    if _contains_any(prompt, "logs", "archive", "recent"):
        risks.append("archive_recent_memory_confusion")
    if _contains_any(prompt, "chapter", "section"):
        risks.append("section_numbers_mistaken_for_chapters")
    return _distinct(risks) or ["low_observed_drift"]


def _next_safe_action(stance: str, risks: list[str], decisions: list[RouteDecision]) -> str:
    if "section_numbers_mistaken_for_chapters" in risks:
        return "List source sections or search source text before summarizing."
    if _has_route(decisions, "saved_memory", "PROTECT"):
        return "Protect saved memory; inspect adjacent route logic without modifying it."
    if "source_terrain_mistaken_for_memory" in risks:
        return "Open bounded source snippets; do not save or ingest unless asked."
    if stance == "surgical_refactor":
        return "Inspect declared files first, then make the smallest route-preserving patch."
    if stance == "reconnaissance":
        return "Observe and report expected vs observed terrain before changing behavior."
    return "Return a compact orientation packet before acting."


def _memory_route(prompt: str, route: str, *markers: str) -> RouteDecision:
    touched = _contains_any(prompt, *markers)
    protected = touched and _protected_near_any(prompt, *markers)
    if protected:
        return RouteDecision(route, "PROTECT", f"{route} is named under a protection/avoidance phrase")
    if touched:
        return RouteDecision(route, "OPEN", f"{route} is explicitly requested or relevant")
    return RouteDecision(route, "DEFER", f"{route} is not needed for this task")


def _archive_route(prompt: str) -> RouteDecision:
    touched = _contains_any(prompt, "logs", "archive")
    protected = touched and _protected_near_any(prompt, "logs", "archive")
    if protected:
        return RouteDecision("archive_logs", "PROTECT", "archive/log route is named under protection")
    if touched:
        return RouteDecision("archive_logs", "AUDIT", "archive/log route should be inspected as evidence")
    return RouteDecision("archive_logs", "DEFER", "archive route not requested")


def _full_source_route(prompt: str) -> RouteDecision:
    markers = ("full book", "whole book", "full source", "all sections")
    touched = _contains_any(prompt, *markers)
    protected = touched and _protected_near_any(prompt, *markers)
    if protected:
        return RouteDecision("full_source_ingestion", "PROTECT", "full-source ingestion is explicitly avoided")
    if touched:
        return RouteDecision("full_source_ingestion", "AUDIT", "full-source ingestion requires confirmation")
    return RouteDecision("full_source_ingestion", "DEFER", "bounded source access is safer")


def _dashboard_route(prompt: str) -> RouteDecision:
    touched = _contains_any(prompt, "dashboard", "ui")
    protected = touched and _protected_near_any(prompt, "dashboard", "ui")
    if protected:
        return RouteDecision("dashboard", "PROTECT", "dashboard/UI route is explicitly avoided")
    if touched:
        return RouteDecision("dashboard", "AUDIT", "dashboard/UI route requires scope confirmation")
    return RouteDecision("dashboard", "DEFER", "dashboard not requested")


def _protected_near_any(prompt: str, *needles: str) -> bool:
    for needle in needles:
        index = prompt.find(needle)
        if index < 0:
            continue
        start = max(0, index - 42)
        end = min(len(prompt), index + len(needle) + 24)
        if _contains_any(prompt[start:end], *PROTECTION_MARKERS):
            return True
    return False


def _contains_any(text: str, *needles: str) -> bool:
    return any(needle in text for needle in needles)


def _has_route(decisions: list[RouteDecision], route: str, polarity: str) -> bool:
    return any(decision.route == route and decision.polarity == polarity for decision in decisions)


def _distinct(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _distinct_decisions(decisions: list[RouteDecision]) -> list[RouteDecision]:
    seen: set[tuple[str, str]] = set()
    kept: list[RouteDecision] = []
    for decision in decisions:
        key = (decision.route, decision.polarity)
        if key in seen:
            continue
        seen.add(key)
        kept.append(decision)
    return kept


def _bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values] if values else ["- none"]


def _stable_trace_suffix(prompt: str) -> str:
    if not prompt:
        return "0000"
    value = 17
    for char in prompt:
        value = (value * 31 + ord(char)) & 0x7FFFFFFF
    return str(value)[-4:].zfill(4)

"""Render paper-ready figures and table layouts from existing P1 source artifacts."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path

from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "P1_paper_readiness"

FAILURE_COLORS = {
    "memory_value_root_cause": "#d95f02",
    "downstream_nontermination_after_semantic_error": "#7570b3",
}
BOUNDARY_COLORS = {
    "pass": "#c7e9c0",
    64: "#fee08b",
    16: "#fdae61",
    4: "#f46d43",
    1: "#d73027",
}


def read_json(path: str | Path) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def svg_text(x: float, y: float, text: str, *, size: int = 16, weight: str = "normal", fill: str = "#111827", anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Segoe UI, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(text)}</text>'
    )


def svg_rect(x: float, y: float, width: float, height: float, *, fill: str = "#ffffff", stroke: str = "#d1d5db", rx: int = 8, dash: str | None = None) -> str:
    dash_attr = "" if dash is None else f' stroke-dasharray="{dash}"'
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1"{dash_attr}/>'
    )


def svg_line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#6b7280", width: int = 2, dash: str | None = None) -> str:
    dash_attr = "" if dash is None else f' stroke-dasharray="{dash}"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"{dash_attr}/>'


def svg_arrow(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#4b5563", width: int = 2, dash: str | None = None) -> str:
    angle = 0.0
    if x2 != x1 or y2 != y1:
        from math import atan2, cos, sin

        angle = atan2(y2 - y1, x2 - x1)
        head = 10
        left_x = x2 - head * cos(angle - 0.5)
        left_y = y2 - head * sin(angle - 0.5)
        right_x = x2 - head * cos(angle + 0.5)
        right_y = y2 - head * sin(angle + 0.5)
        return (
            svg_line(x1, y1, x2, y2, stroke=stroke, width=width, dash=dash)
            + svg_line(left_x, left_y, x2, y2, stroke=stroke, width=width)
            + svg_line(right_x, right_y, x2, y2, stroke=stroke, width=width)
        )
    return svg_line(x1, y1, x2, y2, stroke=stroke, width=width, dash=dash)


def wrap_svg(width: int, height: int, body: list[str]) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">'
        + "".join(body)
        + "</svg>"
    )


def build_failure_taxonomy_figure_svg(summary: dict[str, object]) -> str:
    families: list[dict[str, object]] = summary["by_family"]  # type: ignore[assignment]
    width = 1100
    height = 170 + len(families) * 52
    bar_left = 420
    bar_width = 520
    top = 110
    max_count = max(int(item["program_count"]) for item in families)

    body = [
        svg_rect(0, 0, width, height, fill="#ffffff", stroke="#ffffff", rx=0),
        svg_text(40, 48, "M4 staged-pointer held-out failure taxonomy", size=26, weight="bold"),
        svg_text(40, 76, "Target slice: opcode_shape mask on held-out programs. Each family bar shows failed programs by first attributed provenance class.", size=14, fill="#374151"),
    ]

    provenance_counts = {
        item["provenance_class"]: int(item["count"])
        for item in summary["by_provenance_class"]  # type: ignore[index]
    }
    body.extend(
        [
            svg_rect(40, 92, 18, 18, fill=FAILURE_COLORS["memory_value_root_cause"], stroke=FAILURE_COLORS["memory_value_root_cause"], rx=3),
            svg_text(66, 106, "direct memory-value root cause", size=13),
            svg_rect(290, 92, 18, 18, fill=FAILURE_COLORS["downstream_nontermination_after_semantic_error"], stroke=FAILURE_COLORS["downstream_nontermination_after_semantic_error"], rx=3),
            svg_text(316, 106, "downstream nontermination after earlier semantic error", size=13),
            svg_text(980, 106, f"{provenance_counts['memory_value_root_cause']} vs {provenance_counts['downstream_nontermination_after_semantic_error']}", size=18, weight="bold", anchor="end"),
        ]
    )

    for tick in range(max_count + 1):
        x = bar_left + bar_width * tick / max_count
        body.append(svg_line(x, top - 14, x, top + len(families) * 52 - 8, stroke="#e5e7eb", width=1))
        body.append(svg_text(x, top - 24, str(tick), size=12, fill="#6b7280", anchor="middle"))

    for index, family in enumerate(families):
        row_y = top + index * 52
        label = str(family["family"])
        program_count = int(family["program_count"])
        body.append(svg_text(40, row_y + 18, label, size=15, weight="bold"))
        body.append(svg_text(40, row_y + 36, f"{family['failed_program_count']} / {program_count} failed", size=12, fill="#6b7280"))
        body.append(svg_rect(bar_left, row_y, bar_width, 26, fill="#f3f4f6", stroke="#e5e7eb", rx=4))

        running_x = bar_left
        total_segment_count = 0
        for entry in family["by_provenance_class"]:  # type: ignore[index]
            provenance_class = str(entry["provenance_class"])
            count = int(entry["count"])
            total_segment_count += count
            segment_width = bar_width * count / max_count
            color = FAILURE_COLORS[provenance_class]
            body.append(svg_rect(running_x, row_y, segment_width, 26, fill=color, stroke=color, rx=4))
            body.append(svg_text(running_x + segment_width / 2, row_y + 18, str(count), size=12, weight="bold", fill="#ffffff", anchor="middle"))
            running_x += segment_width
        if total_segment_count < program_count:
            remaining_width = bar_width * (program_count - total_segment_count) / max_count
            body.append(svg_rect(running_x, row_y, remaining_width, 26, fill="#d1fae5", stroke="#10b981", rx=4))

    body.append(svg_text(40, height - 28, "All 15 held-out opcode_shape programs fail. The split is narrow: 8 direct memory-value failures and 7 downstream nontermination rows.", size=13, fill="#374151"))
    return wrap_svg(width, height, body)


def boundary_cell_label(item: dict[str, object]) -> tuple[str, str]:
    if bool(item["all_rows_passed"]):
        return "64x+", "pass"
    failure_horizon = int(item["min_failed_horizon_multiplier"])
    return f"{failure_horizon}x", str(failure_horizon)


def build_real_trace_boundary_figure_svg(summary: dict[str, object]) -> str:
    rows: list[dict[str, object]] = summary["by_stream_boundary"]  # type: ignore[assignment]
    schemes = ["single_head", "radix2", "block_recentered"]
    grouped: dict[tuple[str, str], dict[str, dict[str, object]]] = {}
    for row in rows:
        key = (str(row["suite_bundle"]), str(row["stream_name"]))
        grouped.setdefault(key, {})[str(row["scheme"])] = row

    ordered_keys = sorted(grouped, key=lambda item: (0 if item[0] == "offset" else 1, item[1]))
    width = 1180
    row_height = 32
    height = 210 + len(ordered_keys) * row_height
    label_left = 40
    grid_left = 500
    cell_width = 180
    top = 140

    body = [
        svg_rect(0, 0, width, height, fill="#ffffff", stroke="#ffffff", rx=0),
        svg_text(40, 44, "M4 real-trace precision boundary", size=26, weight="bold"),
        svg_text(40, 72, "Earliest failing horizon multiplier by stream and scheme. Green cells stay stable through the exported 64x horizon. All failures are tie_collapse.", size=14, fill="#374151"),
    ]

    legend = [("64x+", BOUNDARY_COLORS["pass"]), ("64x", BOUNDARY_COLORS[64]), ("16x", BOUNDARY_COLORS[16]), ("4x", BOUNDARY_COLORS[4]), ("1x", BOUNDARY_COLORS[1])]
    legend_x = 40
    for label, color in legend:
        body.append(svg_rect(legend_x, 92, 22, 18, fill=color, stroke=color, rx=3))
        body.append(svg_text(legend_x + 30, 106, label, size=13))
        legend_x += 95

    for scheme_index, scheme in enumerate(schemes):
        x = grid_left + scheme_index * cell_width
        body.append(svg_text(x + cell_width / 2, top - 18, scheme, size=14, weight="bold", anchor="middle"))

    current_suite = None
    for row_index, key in enumerate(ordered_keys):
        suite_bundle, stream_name = key
        y = top + row_index * row_height
        if current_suite != suite_bundle:
            current_suite = suite_bundle
            body.append(svg_text(label_left, y - 8, current_suite.upper(), size=13, weight="bold", fill="#2563eb"))
        body.append(svg_text(label_left, y + 20, stream_name, size=13))
        for scheme_index, scheme in enumerate(schemes):
            item = grouped[key][scheme]
            label, color_key = boundary_cell_label(item)
            fill = BOUNDARY_COLORS["pass"] if color_key == "pass" else BOUNDARY_COLORS[int(color_key)]
            x = grid_left + scheme_index * cell_width
            body.append(svg_rect(x, y, cell_width - 12, 24, fill=fill, stroke="#d1d5db", rx=4))
            body.append(svg_text(x + (cell_width - 12) / 2, y + 17, label, size=13, weight="bold", anchor="middle"))
        body.append(svg_line(label_left, y + 28, width - 40, y + 28, stroke="#f3f4f6", width=1))

    body.append(svg_text(40, height - 28, "Single-head float32 is the only failing scheme in the current bundle. Radix-2 and block-recentered stay stable through the exported 64x sweep on all current rows.", size=13, fill="#374151"))
    return wrap_svg(width, height, body)


def build_frontend_boundary_diagram_svg(exact_table: dict[str, object]) -> str:
    summary: dict[str, object] = exact_table["summary"]  # type: ignore[assignment]
    by_mode = {
        str(item["comparison_mode"]): int(item["count"])
        for item in summary["by_comparison_mode"]  # type: ignore[index]
    }
    short_medium_count = by_mode.get("short_exact_trace", 0) + by_mode.get("medium_exact_trace", 0)
    long_count = by_mode.get("long_exact_final_state", 0)
    width = 1200
    height = 720
    body = [
        svg_rect(0, 0, width, height, fill="#ffffff", stroke="#ffffff", rx=0),
        svg_text(40, 46, "M6 frontend boundary: tiny typed bytecode, not arbitrary C", size=26, weight="bold"),
        svg_text(40, 74, "The first compiled step is a verifier-visible bytecode that lowers into the current exact exec_trace substrate. Wider compiled frontends stay blocked behind this boundary.", size=14, fill="#374151"),
    ]

    body.extend(
        [
            svg_rect(90, 170, 260, 110, fill="#eff6ff", stroke="#93c5fd"),
            svg_text(220, 205, "Current exact substrate", size=20, weight="bold", anchor="middle"),
            svg_text(220, 232, "append-only trace semantics", size=14, anchor="middle"),
            svg_text(220, 254, "current exec_trace interpreter", size=14, anchor="middle"),
            svg_text(220, 276, "no new VM in v1", size=14, anchor="middle"),

            svg_rect(455, 120, 290, 170, fill="#f5f3ff", stroke="#c4b5fd"),
            svg_text(600, 155, "Tiny typed bytecode v1", size=22, weight="bold", anchor="middle"),
            svg_text(600, 184, "types: i32, addr, flag", size=14, anchor="middle"),
            svg_text(600, 208, "ops: const, dup/pop, add/sub/eq", size=14, anchor="middle"),
            svg_text(600, 232, "load/store static + indirect", size=14, anchor="middle"),
            svg_text(600, 256, "jmp, jz_zero, static-target call/ret, halt", size=14, anchor="middle"),
            svg_text(600, 280, "differentially checked against reference", size=14, anchor="middle"),

            svg_rect(455, 340, 290, 120, fill="#ecfeff", stroke="#67e8f9"),
            svg_text(600, 374, "Verifier + lowering", size=20, weight="bold", anchor="middle"),
            svg_text(600, 402, "deterministic first-error reports", size=14, anchor="middle"),
            svg_text(600, 426, "lower to current exec_trace program", size=14, anchor="middle"),

            svg_rect(850, 170, 260, 160, fill="#f0fdf4", stroke="#86efac"),
            svg_text(980, 204, "Current evidence", size=20, weight="bold", anchor="middle"),
            svg_text(980, 232, f"{summary['verifier_pass_count']} verifier-passing rows", size=14, anchor="middle"),
            svg_text(980, 256, f"{short_medium_count} short/medium exact-trace matches", size=14, anchor="middle"),
            svg_text(980, 280, f"{long_count} long exact-final-state matches", size=14, anchor="middle"),
            svg_text(980, 304, f"{summary['total_rows']} paper-table rows in scope", size=14, anchor="middle"),

            svg_rect(850, 420, 260, 120, fill="#fff7ed", stroke="#fdba74", dash="8 6"),
            svg_text(980, 454, "Later compiled frontends", size=20, weight="bold", anchor="middle"),
            svg_text(980, 482, "remain blocked until this tiny", size=14, anchor="middle"),
            svg_text(980, 504, "typed-bytecode boundary widens safely", size=14, anchor="middle"),

            svg_rect(90, 500, 655, 140, fill="#fef2f2", stroke="#fca5a5"),
            svg_text(418, 536, "Explicitly out of scope in v1", size=20, weight="bold", anchor="middle"),
            svg_text(418, 566, "floating point  •  heap allocation  •  general recursion  •  locals", size=14, anchor="middle"),
            svg_text(418, 592, "host effects/syscalls  •  concurrency  •  arbitrary C support", size=14, anchor="middle"),
        ]
    )

    body.extend(
        [
            svg_arrow(350, 225, 455, 205),
            svg_arrow(600, 290, 600, 340),
            svg_arrow(745, 225, 850, 225),
            svg_arrow(745, 430, 850, 450, dash="8 6"),
            svg_arrow(600, 460, 350, 500),
        ]
    )
    return wrap_svg(width, height, body)


def pretty_result_label(row: dict[str, object]) -> str:
    return "exact trace" if str(row["success_target"]) == "exact_trace" else "exact final state"


def pretty_bool(flag: object) -> str:
    return "pass" if bool(flag) else "fail"


def pretty_addresses(value: object) -> str:
    text = str(value)
    return text if text else "-"


def build_exact_trace_final_state_markdown(exact_table: dict[str, object]) -> str:
    rows: list[dict[str, object]] = exact_table["rows"]  # type: ignore[assignment]
    summary: dict[str, object] = exact_table["summary"]  # type: ignore[assignment]

    lines = [
        "# Exact Trace / Final State Table",
        "",
        "Current scope: initial typed-bytecode families only. This remains a partial paper table because later compiled families are still absent.",
        "",
        f"- Total rows: `{summary['total_rows']}`",
        f"- Exact-trace matches: `{summary['trace_match_count']}`",
        f"- Exact-final-state matches: `{summary['final_state_match_count']}`",
        f"- Verifier-passing rows: `{summary['verifier_pass_count']}`",
        "",
        "| Program | Suite | Length | Target | Verifier | Bytecode instr | Lowered instr | Result |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        result = "exact"
        if row["failure_class"] is not None:
            result = f"mismatch: {row['failure_class']}"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["program_name"]),
                    str(row["suite"]),
                    str(row["length_bucket"]),
                    pretty_result_label(row),
                    "pass" if bool(row["verifier_passed"]) else "fail",
                    str(row["bytecode_instruction_count"]),
                    str(row["lowered_instruction_count"]),
                    result,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Scope note",
            "",
            str(summary["pending_scope_note"]),
            "",
        ]
    )
    return "\n".join(lines)


def build_memory_surface_diagnostic_markdown(memory_surface: dict[str, object]) -> str:
    rows: list[dict[str, object]] = memory_surface["rows"]  # type: ignore[assignment]
    summary: dict[str, object] = memory_surface["summary"]  # type: ignore[assignment]
    negative_controls: list[dict[str, object]] = memory_surface["negative_controls"]  # type: ignore[assignment]

    lines = [
        "# Memory Surface Diagnostic Table",
        "",
        "Current scope: appendix-level D0 diagnostic on the same control-flow-first typed-bytecode slice. This does not widen the compiled-frontend claim boundary.",
        "",
        f"- Annotated rows: `{summary['row_count']}`",
        f"- Surface verifier passes: `{summary['surface_verifier_pass_count']}`",
        f"- Surface matches: `{summary['surface_match_count']}`",
        f"- Negative controls: `{summary['negative_control_count']}`",
        "",
        "| Program | Mode | Base exact | Surface verifier | Surface match | Boundary snaps | Max depth | Frame addrs | Heap addrs |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        base_exact = bool(row["base_trace_match"]) and bool(row["base_final_state_match"])
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["program_name"]),
                    str(row["comparison_mode"]),
                    "exact" if base_exact else "drift",
                    pretty_bool(row["memory_surface_verifier_passed"]),
                    pretty_bool(row["memory_surface_match"]),
                    str(row["boundary_snapshot_count"]),
                    str(row["max_call_depth"]),
                    pretty_addresses(row["touched_frame_addresses"]),
                    pretty_addresses(row["touched_heap_addresses"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Negative controls",
            "",
            "| Program | Error class | First error pc | Max depth |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in negative_controls:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["program_name"]),
                    str(row["error_class"]),
                    str(row["first_error_pc"]),
                    str(row["max_call_depth"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Scope note",
            "",
            str(memory_surface["coverage_note"]),
            "",
        ]
    )
    return "\n".join(lines)


def build_layout_manifest() -> dict[str, object]:
    environment = detect_runtime_environment()
    return {
        "experiment": "p1_render_bundle_artifacts",
        "environment": environment.as_dict(),
        "source_artifacts": [
            "results/P1_paper_readiness/m4_failure_taxonomy_summary.json",
            "results/P1_paper_readiness/m4_real_trace_boundary_summary.json",
            "results/P1_paper_readiness/exact_trace_final_state_table.json",
            "results/P1_paper_readiness/m6_memory_surface_diagnostic_summary.json",
        ],
        "rendered_assets": [
            {
                "bundle_item": "Provenance-backed staged failure taxonomy",
                "path": "results/P1_paper_readiness/m4_failure_taxonomy_figure.svg",
                "kind": "figure_svg",
            },
            {
                "bundle_item": "Real-trace precision boundary",
                "path": "results/P1_paper_readiness/m4_real_trace_boundary_figure.svg",
                "kind": "figure_svg",
            },
            {
                "bundle_item": "Frontend boundary diagram",
                "path": "results/P1_paper_readiness/m6_frontend_boundary_diagram.svg",
                "kind": "figure_svg",
            },
            {
                "bundle_item": "Exact-trace / final-state success table",
                "path": "results/P1_paper_readiness/exact_trace_final_state_table.md",
                "kind": "table_markdown",
            },
            {
                "bundle_item": "Memory-surface diagnostic companion table",
                "path": "results/P1_paper_readiness/m6_memory_surface_diagnostic_table.md",
                "kind": "table_markdown",
            },
        ],
        "notes": [
            "These rendered assets are layout companions only; they do not widen the scientific scope.",
            "The exact-trace table remains partial because later compiled frontend families are still absent.",
            "The memory-surface table is appendix-level only and stays attached to the same D0 boundary.",
        ],
    }


def main() -> None:
    failure_summary = read_json(OUT_DIR / "m4_failure_taxonomy_summary.json")
    boundary_summary = read_json(OUT_DIR / "m4_real_trace_boundary_summary.json")
    exact_table = read_json(OUT_DIR / "exact_trace_final_state_table.json")
    memory_surface = read_json(OUT_DIR / "m6_memory_surface_diagnostic_summary.json")

    (OUT_DIR / "m4_failure_taxonomy_figure.svg").write_text(
        build_failure_taxonomy_figure_svg(failure_summary),
        encoding="utf-8",
    )
    (OUT_DIR / "m4_real_trace_boundary_figure.svg").write_text(
        build_real_trace_boundary_figure_svg(boundary_summary),
        encoding="utf-8",
    )
    (OUT_DIR / "m6_frontend_boundary_diagram.svg").write_text(
        build_frontend_boundary_diagram_svg(exact_table),
        encoding="utf-8",
    )
    (OUT_DIR / "exact_trace_final_state_table.md").write_text(
        build_exact_trace_final_state_markdown(exact_table),
        encoding="utf-8",
    )
    (OUT_DIR / "m6_memory_surface_diagnostic_table.md").write_text(
        build_memory_surface_diagnostic_markdown(memory_surface),
        encoding="utf-8",
    )
    (OUT_DIR / "layout_manifest.json").write_text(
        json.dumps(build_layout_manifest(), indent=2),
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()

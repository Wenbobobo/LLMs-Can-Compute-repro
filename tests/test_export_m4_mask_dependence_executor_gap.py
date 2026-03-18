from __future__ import annotations

from dataclasses import replace
import importlib.util
from pathlib import Path
import sys

from exec_trace import TraceInterpreter, countdown_program
from model import FactorizedEventModelConfig, PointerEventCodec


def _load_export_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "export_m4_mask_dependence_executor_gap.py"
    spec = importlib.util.spec_from_file_location("export_m4_mask_dependence_executor_gap", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_compare_events_handles_push_expr_slots_without_attribute_errors() -> None:
    module = _load_export_module()
    program = countdown_program(0)
    interpreter = TraceInterpreter()
    reference_events = interpreter.run(program).events
    produced_events = (replace(reference_events[0], pushed=(reference_events[0].pushed[0] + 1,)), *reference_events[1:])
    codec = PointerEventCodec(FactorizedEventModelConfig(history_window=4))

    diagnostic = module.compare_events(
        codec,
        program,
        reference_events,
        produced_events,
        first_mismatch_step=0,
    )

    assert diagnostic["diagnostic_source"] == "trace_mismatch"
    assert diagnostic["first_error_head"] == "push_expr_0"


def test_classify_runtime_exception_exposes_step_budget_as_runtime_bucket() -> None:
    module = _load_export_module()
    program = countdown_program(0)

    diagnostic = module.classify_runtime_exception(
        program,
        "Maximum step budget exceeded for program 'countdown_0'.",
    )

    assert diagnostic["diagnostic_source"] == "runtime_exception"
    assert diagnostic["first_error_class"] == "rollout_nontermination"
    assert diagnostic["first_error_head"] == "step_budget"

"""Export exact hard-max decode checks for the current trace examples."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from exec_trace import TraceInterpreter, latest_write_program, memory_accumulator_program
from model import run_latest_write_decode_for_events


def encode_program(program_factory):
    result = TraceInterpreter().run(program_factory())
    decode_run = run_latest_write_decode_for_events(result.events)
    return {
        "program": result.program.name,
        "final_state": {
            "pc": result.final_state.pc,
            "stack": list(result.final_state.stack),
            "memory": [list(item) for item in result.final_state.memory],
            "halted": result.final_state.halted,
            "steps": result.final_state.steps,
        },
        "decode": {
            "addresses": list(decode_run.config.addresses),
            "max_steps": decode_run.config.max_steps,
            "epsilon": str(decode_run.config.epsilon),
            "observations": [asdict(observation) for observation in decode_run.observations],
        },
    }


def main() -> None:
    output = {
        "latest_write": encode_program(latest_write_program),
        "memory_accumulator": encode_program(memory_accumulator_program),
    }
    out_path = Path("results/M4_exact_hardmax_model/decode_examples.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path.as_posix())


if __name__ == "__main__":
    main()

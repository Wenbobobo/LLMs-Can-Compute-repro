"""Materialize the organic-trace milestone from the current broadened M4-E precision batch."""

from __future__ import annotations

import json
from pathlib import Path


def load_json(path: str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    screening = load_json("results/M4_precision_generalization/screening.json")
    boundary = load_json("results/M4_precision_generalization/boundary_sweep.json")
    catalog = load_json("results/M4_precision_generalization/stream_catalog.json")

    screening["experiment"] = "m4_precision_organic_traces_screening"
    boundary["experiment"] = "m4_precision_organic_traces_boundary_sweep"
    claim_impact = {
        "target_claim": "C3e",
        "status": "narrowed_positive_with_boundary",
        "evidence_basis": [
            "the organic-trace milestone reuses the current broadened M4-E batch instead of silently re-running an equivalent suite under a new name.",
            "all currently exported high-address memory families fail at 1x under float32 single_head.",
            "the deeper exported stack stream first fails at 4x, while the shallower stack stream stays stable through screening.",
            "observed failure type remains tie_collapse across the current broadened suite.",
        ],
        "concrete_stream_families": sorted({row["family"] for row in catalog}),
    }

    out_dir = Path("results/M4_precision_organic_traces")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "screening.json").write_text(json.dumps(screening, indent=2), encoding="utf-8")
    (out_dir / "boundary_sweep.json").write_text(json.dumps(boundary, indent=2), encoding="utf-8")
    (out_dir / "stream_catalog.json").write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    (out_dir / "claim_impact.json").write_text(json.dumps(claim_impact, indent=2), encoding="utf-8")
    print(out_dir.as_posix())


if __name__ == "__main__":
    main()

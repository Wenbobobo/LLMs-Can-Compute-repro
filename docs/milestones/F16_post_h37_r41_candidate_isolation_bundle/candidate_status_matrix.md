# Candidate Status Matrix

| Candidate id | Threat family | Fixed rows | Comparator set | Measurement rule | Stop rule | Status | Why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `helper_annotation_ablation_or_canonicalization` | `runtime_irrelevance_via_compiler_helper_overencoding` | landed admitted `R40` row plus landed boundary `R40` row | first four `F13` comparators only | helper-neutralization may count only if source meaning and lowered semantics stay fixed while accelerated behavior changes locally | stop on semantic drift, opcode drift, or non-unique attribution | `nonunique` | still overlaps materially with the control-surface-neutralization story and no one helper-neutralization currently dominates sharply enough over the already completed `R39` objection |
| `control_surface_neutralization_without_semantic_change` | `runtime_irrelevance_via_compiler_helper_overencoding` | landed admitted `R40` row plus landed boundary `R40` row | first four `F13` comparators only | one declared control-surface choice may count only if source meaning, workload role, and lowered semantics remain fixed | stop on semantic drift, opcode drift, or non-unique attribution | `nonunique` | remains a legitimate caution, but `F16` still cannot name one sharper same-row perturbation that dominates strongly enough to isolate runtime irrelevance by itself |
| `retrieval_critical_vs_local_easy_step_contrast_slicing` | `fast_path_only_helps_the_easy_part` | landed admitted `R40` row plus landed boundary `R40` row, but only with one slice pair per row | first four `F13` comparators plus per-slice trace-state measurements | slice asymmetry counts only if the same row has one mechanical retrieval-critical slice and one mechanical local-easy slice under the same source meaning | stop if either row lacks a predeclared mechanical slice pair | `inadmissible` | the current packet still lacks a row-locked mechanical slice pair on both landed rows, so the candidate is not execution-ready on the fixed `R40` pair |

## Bundle Verdict

`no_candidate_ready`

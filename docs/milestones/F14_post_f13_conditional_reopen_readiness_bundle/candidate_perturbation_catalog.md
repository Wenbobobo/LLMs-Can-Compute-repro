# Candidate Perturbation Catalog

Only same-row, same-opcode, same-substrate perturbations are admissible here.

| Candidate id | Perturbation shape | Allowed now? | Intended target risk |
| --- | --- | --- | --- |
| `helper_annotation_ablation_or_canonicalization` | remove, canonicalize, or neutralize helper annotations while keeping source meaning and opcode surface fixed | admissible in principle | `runtime_irrelevance_via_compiler_helper_overencoding` |
| `control_surface_neutralization_without_semantic_change` | alter one declared control-surface choice while preserving source semantics and workload shape | admissible in principle | `runtime_irrelevance_via_compiler_helper_overencoding` |
| `retrieval_critical_vs_local_easy_step_contrast_slicing` | compare one retrieval-critical slice against one locally easy slice on the same bounded family | admissible in principle | `fast_path_only_helps_the_easy_part` |

Current state:

- no candidate is yet uniquely isolated strongly enough to justify a future
  explicit packet.

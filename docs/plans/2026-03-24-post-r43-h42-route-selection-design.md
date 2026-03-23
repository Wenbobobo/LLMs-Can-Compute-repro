# Post-R43 H42 Route-Selection Design

## Objective

Convert the saved
`H42_post_r43_route_selection_packet` placeholder into one executable
docs-only packet that makes the next lane explicit. The packet must interpret
the landed `H41/F20/P27/R43/R45` stack without broadening claims, without
letting model evidence replace exact evidence, and without treating merge
posture as a scientific result. The concrete decision surface is narrow:
either authorize `R44`, hold at `R43` while strengthening bounded kernels, or
freeze again and continue planning-only work.

## Recommended Decision

Authorize exactly
`R44_origin_restricted_wasm_useful_case_execution_gate`.

This is the strongest route currently justified without inventing a wider
runtime thesis. `F19` already fixed the restricted useful-case ladder and its
stop rule. `R43` then validated bounded-memory exact execution on `5/5`
families, including the gated optional call/return family. `R45` added a
coequal model lane on that same contract family and stayed exact on both
admitted modes, but `F20` keeps that evidence non-substitutive. Together,
those results justify moving from bounded execution proof to the next exact
useful-case gate. They do not justify arbitrary `C`, general “LLMs are
computers”, or relaxing the restricted surface.

## Required Artifacts

Land one `H42` exporter plus focused pytest, write `summary/checklist/
claim_packet/snapshot` outputs, upgrade the `H42` milestone docs from saved to
completed, update `R44` from deferred to authorized-next, and refresh the
driver/index surfaces so `H42` becomes current and `R44` becomes the next
required order. Keep merge posture unchanged: `P27` still records
`merge_executed = false`, and `main` remains unmerged.

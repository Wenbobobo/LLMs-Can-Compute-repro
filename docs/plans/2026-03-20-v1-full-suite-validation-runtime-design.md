# V1 Full-Suite Validation Runtime Design

## Goal

Turn the slow or non-returning `uv run pytest -q` standing gate into a bounded,
machine-readable validation-hygiene question.

## Intended outputs

- one exporter that runs `pytest --collect-only -q` under a timeout and parses
  the collected test inventory;
- one heuristic file-level inventory that highlights likely heavy validation
  files before expensive reruns;
- one summary artifact that recommends the next bounded debugging step.

## Scope lock

- do not change scientific code or claim wording;
- do not declare the full-suite gate broken without evidence;
- do not silently replace the full-suite standing gate with a weaker one.

## Acceptance

- the audit reports collected test count and collection timing;
- the audit identifies a bounded shortlist of likely heavy files from the
  current suite;
- the audit leaves one explicit next debugging step for future unattended runs.

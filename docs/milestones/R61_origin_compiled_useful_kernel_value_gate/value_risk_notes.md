# Value Risk Notes

`R61` is not allowed to reuse the old negative/positive rhetoric loosely. It
must answer one bounded value question on the exact `R60` rows only.

Main risks to guard against:

- exact but operationally meaningless wins caused by compiler-side pre-work;
- exact internal execution that is slower than a plain transparent reference
  path by enough margin that the route has no practical bounded value;
- wins that disappear once export, lowering, or trace materialization cost is
  counted; and
- wins that depend on changing the admitted row mix after `R60`.

Interpretation rule:

- if the accelerated route only matches exactness but does not beat simpler
  baselines in a bounded and well-accounted way, that is a negative value
  result, not a partial systems success;
- if the route wins only by excluding compiler/export overhead, the result is
  not admissible as bounded value;
- if exactness breaks on any admitted row, the value question collapses back to
  an `R60`-level failure.

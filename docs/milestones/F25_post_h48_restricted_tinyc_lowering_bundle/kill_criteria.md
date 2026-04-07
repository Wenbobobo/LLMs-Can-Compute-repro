# F25 Kill Criteria

`H49` must freeze the post-`H48` tiny-`C` line as a practical falsifier if any
of the following occurs in `R50`:

1. exact lowering requires a new evaluator, heap, alias-heavy pointers,
   recursion, float semantics, IO, or hidden mutable state;
2. the source cannot lower instruction-faithfully onto the preserved
   useful-case bytecode contract without adding a broader runtime substrate;
3. success depends on comparator/model evidence, partial exactness, or looser
   scoring rather than the preserved exact `R47/R49` standard;
4. the first pass cannot stay exact on the preserved `8/8` useful-case
   variants across the fixed `3/3` kernel ladder;
5. bounded table updates such as `hist[16]` cannot stay inside explicit fixed
   windows with declared range guards; or
6. the interpretation would need arbitrary `C`, multi-function programs, or
   scope wording broader than `bounded_useful_cases_only`.

If none of these triggers fire, `H49` may interpret `R50` as the narrowest
admissible restricted tiny-`C` lowering result on the preserved useful-case
contract.

# R57 Value Rule

- a positive exactness result from `R55` or `R56` does not imply fast-path
  value automatically;
- the accelerated route must be compared against transparent references on the
  same exact row set;
- if the accelerated route remains exact but does not show bounded value, the
  scientific closeout should be "mechanism supported without fast-path value";
- and if exactness breaks anywhere in the comparator stack, the closeout
  should be "partial mechanism only" rather than a value win.

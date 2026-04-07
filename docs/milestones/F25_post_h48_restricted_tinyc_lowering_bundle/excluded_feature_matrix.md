# F25 Excluded Feature Matrix

| excluded feature | why excluded here | what would trigger stop |
| --- | --- | --- |
| heap allocation | would require a broader memory model than the preserved static-window contract | any need for dynamic allocation or free-store semantics |
| alias-heavy pointers | would require non-local pointer reasoning and hidden state interactions | any success path depending on pointer alias analysis beyond fixed windows |
| recursion or indirect calls | would widen control semantics beyond the preserved structured loop/branch surface | any need for recursive lowering, function pointers, or indirect dispatch |
| float semantics | would mix the already-separated numeric-scaling question into tiny-`C` lowering | any need to lower float arithmetic as part of the first `R50` pass |
| IO or external side effects | would move beyond the append-only exact runtime contract | any dependence on system calls, file/device IO, or ambient state |
| hidden mutable globals | would undermine the explicit state boundary used in `R46/R47/R49` | any dependence on undeclared mutable state outside declared buffers |
| library calls or arbitrary `C` wording | would inflate the claim from a restricted lowering probe to a broader language claim | any success claim phrased as arbitrary `C`, general TinyC, or libc support |
| multi-function program structure | would exceed the single-kernel useful-case contract being preserved first | any need for more than one top-level kernel function in the first gate |

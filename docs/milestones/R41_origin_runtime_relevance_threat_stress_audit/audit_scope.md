# Audit Scope

This future audit may touch only the two positive `R40` rows:

| Row role | Case id | Program name | Why it stays in scope |
| --- | --- | --- | --- |
| admitted | `bounded_scalar_admitted` | `bytecode_bounded_scalar_flag_loop_6_a320` | smallest landed bounded-scalar positive row |
| boundary stress | `bounded_scalar_boundary` | `bytecode_bounded_scalar_flag_loop_long_12_a336` | named same-family boundary row already preserved by `R40` |

The scope lock also includes:

- same family:
  `bounded scalar locals and flags`;
- same substrate:
  append-only trace, exact retrieval, small exact stack/VM executor;
- same opcode surface:
  `add_i32`, `const_i32`, `eq_i32`, `halt`, `jmp`, `jz_zero`,
  `load_static`, `store_static`, `sub_i32`.

Out of scope:

- `R40` negative controls as primary evidence;
- any new program family;
- any richer value family;
- any new opcode or external effect.

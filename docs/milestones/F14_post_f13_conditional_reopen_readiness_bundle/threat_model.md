# Threat Model

Only two same-substrate threat families remain active here:

| Threat id | Meaning | Why it still matters |
| --- | --- | --- |
| `runtime_irrelevance_via_compiler_helper_overencoding` | the current narrow positive result may depend too heavily on compiler/helper structuring rather than the runtime substrate itself | this is the strongest remaining caution after `R39/H34` |
| `fast_path_only_helps_the_easy_part` | the current acceleration story may matter only on mechanically easy spans while the hard semantic work still lives elsewhere | this is the nearest alternative explanation of the current narrow positive line |

Disallowed additions:

- broader family dissatisfaction;
- restricted-Wasm ambition;
- historical same-endpoint dissatisfaction;
- general LLM-computer rhetoric.

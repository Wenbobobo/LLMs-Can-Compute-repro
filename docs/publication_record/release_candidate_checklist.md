# Release Candidate Checklist

- current package must expose `H65/P56/P57/P58/P59/P66/P67/P68/F38`
- current control wording must also expose `P69/P70/P71` as hygiene-only
  cleanup sidecars
- preserved `H64/H58/H43` must remain explicit
- `P69/P70/P71` do not widen the evidence ladder beyond `H65/P66/P67/P68`
- No outward wording implies a new runtime lane
- dirty root `main` remains quarantine-only

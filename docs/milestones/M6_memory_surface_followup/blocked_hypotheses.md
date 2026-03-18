# Blocked Hypotheses

- Memory bugs will resolve themselves once the verifier is stable; instrumentation must prove otherwise.
- Introducing a new runtime boundary will remain invisible if we keep control-flow fixed; the evidence must come from instrumentation deltas.
- The existing exact-trace schema is sufficient for memory surfaces without adding new claim categories.

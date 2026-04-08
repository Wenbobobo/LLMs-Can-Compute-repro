## 2024-05-24 - Pre-coerce and inline dot products in hot loops
**Learning:** In exact 2D geometry calculations, calling `dot_2d` in hot loops introduces significant overhead because of repeated type coercion (`_coerce_key`) and function calls for `Fraction` objects.
**Action:** Always pre-coerce keys/values outside of hot loops and inline the dot product operation (e.g., `(kx * qx) + (ky * qy)`) directly on the pre-coerced tuples to maximize retrieval speed.

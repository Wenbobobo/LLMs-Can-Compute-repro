# F23 Length Bucket Plan

`R49` should execute exactly three widening buckets on the preserved three
useful-case kernels:

| bucket_id | target buffer span | target base-address span | target exact step budget | admission posture |
| --- | --- | --- | --- | --- |
| `bucket_a_2x` | roughly `2x` the preserved `R47` buffer lengths; admit up to `len16` on sum/histogram and up to `len18` on count kernels | up to `+256` above preserved shifted bases | up to `600` exact steps | required |
| `bucket_b_4x` | roughly `4x` the preserved `R47` buffer lengths; admit up to `len32` on sum/histogram and up to `len36` on count kernels | up to `+1024` base-span shift | up to `1600` exact steps | required |
| `bucket_c_8x` | roughly `8x` the preserved `R47` buffer lengths; admit up to `len64` on sum/histogram and up to `len72` on count kernels | up to `+4096` base-span shift | up to `4000` exact steps | required if earlier buckets stay exact |

`R49` may stop early only through the explicit kill criteria below, not by
informal discomfort with longer exact traces.

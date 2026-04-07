# F23 Addressability Strategy Table

| strategy_id | mechanism | planned `R49` role | keep / reject rule |
| --- | --- | --- | --- |
| `preserved_absolute_base` | current landed useful-case addressing with shifted static bases | baseline comparator for all `R49` rows | keep as the first run on each bucket |
| `radix2_address_split` | split higher address magnitude across structured sub-address components | primary recovery path when absolute-base control fails | keep if exactness survives without widening scope |
| `block_recentered_window` | recenter active address windows before retrieval | coequal recovery path for high-base buckets | keep if exactness survives without widening scope |
| `segment_rescaled_window` | explicit per-segment rescaling before retrieval | reserve fallback only | reject as the default path until admitted by later exact evidence |

# Brainstorm Log

- The first baseline run should answer whether teacher-forced success is hiding
  catastrophic rollout drift. It now does: the answer is yes.
- The current verbose serialization is interpretable but numerically brittle.
  It is suitable for a first scaffold and a first warning signal, not for a
  strong generalization claim.
- The next high-value `M5` ablation is probably representation, not model size.
  A larger model on the same serialization is likely to hide, rather than fix,
  the rollout problem.
- The factorized ablation confirmed part of this: vocabulary pressure drops and
  first error moves later, but zero exact rollout remains. The next move should
  probably change the rollout boundary or sequence compression rather than just
  keep factorizing.

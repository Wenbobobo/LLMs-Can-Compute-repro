# Open Questions

- Should the next learned step keep the current exact candidate-set abstraction
  and learn causal candidate generation, or jump to a tokenized decoder?
- Is mixed memory-plus-stack retrieval the right next target, or should the
  next experiment focus on free-running prediction inside the current stack
  family first?
- What is the smallest evaluation that would count as real rollout rather than
  another discriminative retrieval check?

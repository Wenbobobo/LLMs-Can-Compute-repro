# Ambiguities

## Public-Source Ambiguities

1. **Hard-max vs. standard softmax**
   The field note makes strong geometry claims for a hard-max style retrieval
   regime while also showing a standard PyTorch attention snippet. This repo
   treats them as distinct branches.

2. **"Arbitrary C"**
   The phrase is not actionable without semantic boundaries. The reproduction
   effort assumes a much narrower target until a restricted compiled subset is
   explicitly demonstrated.

3. **"Tool-free"**
   In-model execution may still rely on a specialized decoding/runtime path.
   That counts as a major systems component and should not be hidden.

4. **"Exponentially faster"**
   The credible interpretation is asymptotic improvement in trace-scaled
   retrieval, not universal wall-clock dominance on every task.

5. **Demo semantics**
   Sudoku and Hungarian-style examples may demonstrate internal execution of a
   compiled solver, not solver discovery.

## Local-Archive Note

`docs/Origin/` contains local-only source materials, including a Markdown
conversion of the PDF. Those files are intentionally excluded from the public
repo.

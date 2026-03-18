# 下一阶段无人值守总计划（Paper-First, Aggressive GPU, Worktree+Push）

  ## 摘要

  当前科学目标远景已经足够清晰：本工程不是去证明“LLM 就是通用计算机”，而是要把一个更窄、可证伪、可发表的结论闭合为论文级证据链：

  - 计算是否能被可靠地重写为 append-only execution trace；
  - 关键读操作是否能被编译成 exact latest-write / stack-depth retrieval；
  - 这些检索是否能在有限精度与专用 runtime 下稳定工作，并在系统层面有明确价值；
  - 一个极小前端边界（当前 D0 tiny typed bytecode）是否足以作为“第一 compiled frontend boundary”的严谨证据，而不是 demo 包装。

  当前仓库状态足以进入长时间无人值守推进：

  - origin 已配置，当前仅有 main worktree；
  - 全量测试基线为 109 passed, 1 warning；
  - 下一阶段已存在骨架：P3 / R1 / R2 / M7 / P4；
  - 用户偏好已锁定为：Aggressive GPU、worktree 并行、可以推送远端。

  默认执行原则：

  - 先做 claim freeze / mechanism closure / systems gate，再做任何 frontend widening；
  - paper/README/blog 必须严格下游于证据，不允许反向定义 claim；
  - 无人值守时优先保持高并行与持续工作量，但每一轮都必须留下可整合的 artifact、ledger 和 stop/go 结论。

  ## 执行编排

  ### 1. 固定工作树与职责分配

  创建 4 个长期工作树，写集严格隔离：

  - main：集成树
    只做合并、总体验证、README/STATUS/ledger 最终同步、release/commit/push。
  - wt-paper：文档与论文树
    负责 H0、P3、P4、后续 paper/blog/README 资产。
  - wt-precision：precision 机制树
    负责 R1，包括 sweep、summary、failure taxonomy、paper 源表。
  - wt-systems：systems baseline 树
    负责 R2，包括 baseline matrix、profiling、cost attribution、oracle/path 比较。
  - wt-frontier：条件性前端树
    初始不启用；仅当 M7 明确允许 widening 后再使用。

  ### 2. Agent 并行协议

  默认每一轮都按以下顺序运行：

  1. 主 Agent 在 main 读取：
      - STATUS.md
      - tmp/2026-03-18-next-stage-plan.md
      - docs/milestones/*/todo.md
      - docs/publication_record/*
      - docs/milestones/P1_paper_readiness/
  2. 主 Agent 根据未完成且未阻塞项，分派三个并行 worker：
      - Worker A：wt-paper
      - Worker B：wt-precision
      - Worker C：wt-systems
  3. 每个 worker 只修改自己负责的写集，不回退其他工作树的改动。
  4. 每个 worker 完成一小轮后必须交付：
      - status.md 更新
      - todo.md 勾选或细化
      - artifact_index.md 补全
      - 新 artifact / 表格 / 图 / JSON / CSV
      - 最小验证结果
  5. 主 Agent 只在以下条件满足时整合到 main：
      - 该 worker 的局部目标闭合；
      - 相关文档与 artifact 路径可点击、可复现；
      - 至少 targeted tests 通过；
      - 若触及公共 claim wording，则同步 publication_record。

  ### 3. Commit / Push 规则

  默认采用 worktree+local 高频提交，阶段性推送：

  - 每个 worker 在本地做小提交，提交粒度按 milestone 子任务切；
  - 每个 wave 结束时，主 Agent 在 main 做整合提交；
  - 推送规则：
      - 只推送 可解释的 reviewable branch 或已整合的 main；
      - 分支命名固定为 wip/<milestone>-<yyyymmdd>-<slice>；
      - 只有在相关测试通过、manifest 更新、ledger 同步后才允许推送；
  - 不允许把“只跑到一半的叙事文案”先推上远端再补证据。

  ### 4. 无人值守继续协议

  后续 Codex 若只收到固定消息 “Continue”，必须执行下列算法，而不是重新发散：

  1. 读取当前 todo/status/manifest/git status；
  2. 先完成当前 wave 中未完成的未阻塞项；
  3. 若某一 lane 被数据/结果阻塞，立即切换到同 wave 的其他 lane；
  4. 只有当当前 wave 的 acceptance 达成时，才进入下一 wave；
  5. 若出现高风险负结果，优先记录到 negative_results.md / blocked_hypotheses.md，再决定是否继续扩实验；
  6. 若所有研究 lane 均临时阻塞，则自动转去 paper/README/blog/manifest/commit hygiene，不闲置。

  ## 多轮 Milestone 计划

  ## Wave 0 — H0_repo_consolidation_and_release_hygiene（立即开始）

  ### 目标

  把当前“大脏树但计划内”的状态，整理成可长期无人值守推进的工程面。

  ### 具体 Todo

  - 整理根入口：
      - README.md 保持克制、研究工程语气、显式列出 claim 边界；
      - STATUS.md 只保留当前科学状态、下一 gate、明确 blocker；
  - 整理发布台账：
      - docs/publication_record/claim_ladder.md
      - docs/publication_record/claim_evidence_table.md
      - docs/publication_record/experiment_manifest.md
      - docs/publication_record/paper_bundle_status.md
  - 整理 P1/P2/M6 文档，使其与 M6-E 后状态一致；
  - 把当前已存在但未系统收口的 milestone 目录补成统一格式；
  - 把 commit 计划明确拆成三类：
      - docs/results sync
      - experiments
      - release hygiene

  ### Acceptance

  - 任何新 agent 进入仓库后，只看 README + STATUS + claim_ladder 就能知道当前边界；
  - experiment_manifest 足够支撑后续连续 unattended 批次；
  - 后续工作树创建和整合不会因文档混乱而产生歧义。

  ———

  ## Wave 1 — P3_paper_freeze_and_evidence_mapping（与 R1/R2 并行启动）

  ### 目标

  把已有成果冻结成论文级 claim/evidence map，禁止口径漂移。

  ### 具体 Todo

  - 冻结以下 claim 行：
      - A1 append-only trace substrate
      - B1 exact 2D hard-max retrieval
      - C2h staged mask-dependence closure
      - C3e broader real-trace precision taxonomy
      - D0 first compiled frontend boundary
  - 明确每行 claim 的：
      - 支持 artifact
      - 反例/负结果
      - 威胁与边界
      - 对应 paper figure/table
  - 把 M6-E stress/reference 结果并入 D0，但禁止单独升级为新 claim layer；
  - 重写 paper outline，使章节结构与当前证据真正一致；
  - 明确 unsupported claims 列表：
      - arbitrary C
      - general LLM computation
      - demo-first “LLMs be computers”
      - system-level superiority claim（若 R2 未完成）

  ### 需要生成的成果

  - 冻结版 supported/unsupported claim 表
  - canonical figure/table ownership 表
  - appendix 与 main-text 映射
  - README / STATUS / publication_record 一致化 wording

  ### Acceptance

  - 所有公共 claim 都有精确 artifact 路径；
  - 所有负结果都能在 paper 结构中定位；
  - README/blog 不能再“先写叙事再补证据”。

  ———

  ## Wave 2 — R1_precision_mechanism_closure（GPU 重实验主线）

  ### 目标

  把 finite-precision 机制故事从“若干结果”收口成“一个明确边界”。

  ### 具体 Todo

  - 统一现有 C3d + C3e 为单一 boundary story：
      - native horizon
      - first-failure multiplier
      - failure type
      - scheme sensitivity
  - 只扩 窄而有信息量 的 sweep，不做无界扩张：
      - family 优先级：
          1. 高地址 memory families
          2. alternating offset families
          3. deeper stack fanout
      - scheme 固定：
          - single_head
          - radix2
          - block_recentered
      - base 默认扫描：
          - 16, 32, 64, 128
      - horizon/multiplier 默认：
          - 1x, 2x, 4x, 8x, 16x, 32x, 64x
      - 一旦发现首次失败，继续补 +1 个更大点用于确认稳定转折，不无限延伸
  - 额外加入一个诊断性负对照：
      - 比较一个故意较弱的 addressing/recentering 变体，确认失败确实来自 tie-collapse 机制而不是数据偶然性；
  - 输出 paper-ready canonical 汇总：
      - summary JSON
      - per-family CSV
      - boundary table
      - figure source rows
      - failure taxonomy note

  ### 默认结论模板

  只允许产出三类表述：

  - “在当前验证套件上有效”
  - “在当前验证套件上无证据”
  - “在当前验证套件上被负结果否定”

  ### Acceptance

  - C3e 可以用一句严格的话讲清楚“哪里失败、哪里延缓、哪里仍未证实”；
  - 不再需要继续无上限刷 precision sweep 才能写论文；
  - P3 可以直接引用 R1 结果定稿。

  ———

  ## Wave 3 — R2_systems_baseline_gate（系统价值主线）

  ### 目标

  在任何 frontend widening 前，先搞清楚“有趣机制”与“有用系统”是不是一回事。

  ### 具体 Todo

  - 固定 baseline matrix：
      - linear scan retrieval
      - structured retrieval / specialized retrieval
      - lowered exec path
      - bytecode reference path
      - standalone Python spec oracle
  - 对同一正/负样本集合跑对照，至少覆盖：
      - smoke
      - loops
      - memory
      - control_flow
      - stress/reference family
  - 每个对照都记录：
      - correctness parity
      - total wall-clock
      - per-step time
      - retrieval cost
      - non-retrieval cost
      - where time actually goes
  - 对 M2/M3/M6 的系统层故事做一个 stop/go 表：
      - asymptotic win only
      - practical win on current scope
      - no demonstrated win yet
  - 若结论偏负，也要进入 paper，而不是静默忽略。

  ### 默认比较规则

  - 正确性优先于速度；
  - 所有性能比较都必须在相同 suite 上进行；
  - 不拿“更宽 frontend”偷换成“更快 runtime”。

  ### Acceptance

  - 有一张表明确回答：当前 specialized runtime 在现有 scope 下是否值得；
  - M7 可以基于 R2 做 frontend 决策；
  - 若 R2 结果偏负，后续 widening 默认更保守。

  ———

  ## Wave 4 — M7_frontend_candidate_decision（硬门控）

  ### 目标

  基于 P3 + R1 + R2，做一次明确的“要不要再扩 frontend”决定。

  ### 决策选项

  - No-go / Stay：停留在 tiny typed bytecode，转向论文与 release；
  - Minimal widen：只批准一个极小下一步，例如一类额外控制流或更窄 Wasm-like slice；
  - Hold：证据不足，继续补 R1/R2，不进入 widening。

  ### 决策标准

  只有在以下同时满足时才允许 widening：

  - P3 wording 已冻结；
  - R1 已给出清晰 precision boundary；
  - R2 至少证明 specialized machinery 在当前 scope 上不是空转；
  - widening 能增加新证据，而不是增加展示性。

  ### Acceptance

  - 生成一份单页决策记录；
  - 明确 claim impact、risk、non-goals；
  - 如果是 no-go，也必须写成正经结论，而不是“以后再说”。

  ———

  ## Wave 5A — 若 M7 = No-go：P5_paper_draft_assembly + P4_blog_release_gate

  ### 目标

  把工程转成成熟的论文/公开研究工程，而不是继续扩实验面。

  ### P5 Todo

  - 把 paper_outline 扩成章节化草稿：
      - abstract
      - introduction
      - claim ladder
      - methods
      - results
      - negative results
      - threats to validity
  - 为每张 figure/table 写 caption 和 narrative role；
  - 准备 appendix：
      - artifact map
      - reproducibility instructions
      - diagnostic companion tables
  - 形成完整“paper bundle draft”，即便不是最终 prose，也要可继续迭代。

  ### P4 Todo

  - 验证所有 public-facing claim 都有 paper-grade backing；
  - README 保持研究工程 landing page 风格；
  - blog 默认继续 blocked，除非 paper bundle 已足够稳定；
  - 若决定不写 blog，要明确记录 no-go 理由。

  ### Acceptance

  - 即使不再做新实验，仓库也已经具备论文/公开发布形态；
  - blog 不会抢跑论文；
  - README/STATUS/claim ladder/paper outline 四者完全同口径。

  ———

  ## Wave 5B — 若 M7 = Minimal widen：M8_minimal_frontend_probe（条件分支）

  ### 目标

  只在严格门控后，做一个最小 widened frontend probe。

  ### 默认范围

  只允许一种极小 widening，优先级：

  1. 微扩 typed bytecode，而不是直接跳 Wasm；
  2. 仍保持 deterministic、integer-first、no malloc/free、no float、no syscalls；
  3. 仍要求 differential testing / exact trace or exact final-state parity。

  ### Todo

  - 写新的 frontier spec 与 acceptance；
  - 先构建 verifier/lowering/oracle，再写任何 demo；
  - 必须与 R2 baseline 同步，不允许 widening 后脱离 systems gate；
  - 完成一轮后立即回到 P3/R2/P4 重新 freeze，而不是连续外扩。

  ### Acceptance

  - widening 带来的是新证据，而不是新叙事；
  - 未通过 differential/oracle 的内容不允许进入 README/blog。

  ## Paper / README / Blog 持续跟进规则

  ### README

  - 一直保持简短、克制、研究工程风格；
  - 只放已经稳定的结果图；
  - 不放未来路线图式营销语言。

  ### Paper

  - paper_outline 持续向 manuscript skeleton 逼近；
  - 每完成一个 wave，都同步：
      - claim mapping
      - figure/table status
      - threats
      - negative results
      - manifest

  ### Blog

  - 默认 blocked；
  - 只有在 P4 明确打开后才写；
  - 内容必须是 paper 的派生摘要，不是另起 claim。

  ## 验证计划

  - 更新相关 ledger；
  - 记录复现命令、环境、artifact 路径；
  - 若有新结果，补 experiment_manifest.md 一行。

  ### 每个 wave 结束时

  - 在 main 运行：
      - uv run pytest -q
      - 相关 export/render 脚本
      - git diff --check
  - 若 wave 触及公共 claim wording，还必须重新检查：
      - README.md
      - STATUS.md
      - docs/publication_record/*

  ### 当前默认基线

  - 全量测试绿：109 passed, 1 warning
  - 后续可把“每个大 wave 末尾全测”设为默认，不必每个极小实验后都全测。

  ## 明确假设与默认值

  - 默认采用 Aggressive GPU：优先填满实验、扫描、对照、论文整理，不因无人值守而降速。
  - 默认采用 worktree 并行 + 本地高频提交 + 阶段性推送远端。
  - 默认维持 paper-first, blog-blocked，直到 P4 明确放行。
  - 默认不重开 M5，除非公平比较面发生实质变化。
  - 默认不进入新的 frontend widening，直到 M7 明确正向决策。
  - 默认把任何高风险负结果当作有效产出，及时写入 negative_results.md 和相关 milestone 的 blocked_hypotheses.md。
  - 默认后续“Continue”消息触发的是按 gating order 自动续跑，而不是重新规划方向。
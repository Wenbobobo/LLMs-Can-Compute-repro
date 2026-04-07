# Merge Prep Rules

- preserved source branch:
  `wip/f37-post-h61-hygiene-first-reauth-prep`
- current planning branch:
  `wip/f38-post-h62-archive-first-closeout`
- merge posture:
  `clean_descendant_only_never_dirty_root_main`
- raw row dumps and artifacts above roughly `10 MiB` stay out of git by
  default on the clean descendant line
- no merge is executed in this sidecar

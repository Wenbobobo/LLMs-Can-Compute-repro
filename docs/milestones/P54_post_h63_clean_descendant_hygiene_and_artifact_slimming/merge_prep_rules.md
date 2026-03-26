# Merge Prep Rules

- preserved source branch:
  `wip/f38-post-h62-archive-first-closeout`
- current planning branch:
  `wip/h64-post-h63-archive-first-freeze`
- merge posture:
  `clean_descendant_only_never_dirty_root_main`
- raw row dumps and artifacts above roughly `10 MiB` stay out of git by
  default on the clean descendant line
- no merge is executed in this sidecar

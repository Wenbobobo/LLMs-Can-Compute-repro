param(
    [string]$BaseBranch = "main",
    [string]$WorktreeRoot = "",
    [switch]$AllowDirty,
    [switch]$PushBranches
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot

$gitCommonDir = Resolve-Path (git rev-parse --git-common-dir)
$projectRoot = Split-Path $gitCommonDir -Parent
$projectParent = Split-Path $projectRoot -Parent

$status = git status --porcelain
if (-not $AllowDirty -and $status) {
    throw "Refusing to create unattended worktrees from a dirty tree. Commit or stash first, or rerun with -AllowDirty."
}

if (-not $WorktreeRoot) {
    $WorktreeRoot = Join-Path $projectParent "wt"
}

New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null

$worktrees = @(
    @{ Name = "paper"; Branch = "wip/p3-paper-freeze"; Path = (Join-Path $WorktreeRoot "paper") },
    @{ Name = "precision"; Branch = "wip/r1-precision-closure"; Path = (Join-Path $WorktreeRoot "precision") },
    @{ Name = "systems"; Branch = "wip/r2-systems-gate"; Path = (Join-Path $WorktreeRoot "systems") }
)

foreach ($item in $worktrees) {
    $existingBranch = git branch --list $item.Branch
    if (-not $existingBranch) {
        git branch $item.Branch $BaseBranch | Out-Null
    }

    $alreadyPresent = git worktree list --porcelain | Select-String -Pattern ("branch refs/heads/" + [regex]::Escape($item.Branch))
    if (-not $alreadyPresent) {
        git worktree add $item.Path $item.Branch | Out-Null
    }

    if ($PushBranches) {
        git -C $item.Path push -u origin $item.Branch
    }
}

Write-Host "Configured unattended worktrees:"
git worktree list

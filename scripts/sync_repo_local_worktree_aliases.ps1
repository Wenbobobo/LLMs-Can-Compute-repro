param(
    [string]$AliasRoot = "",
    [switch]$MirrorLegacyShortcuts
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot

$gitCommonDir = Resolve-Path (git rev-parse --git-common-dir)
$projectRoot = Split-Path $gitCommonDir -Parent
$projectParent = Split-Path $projectRoot -Parent

if (-not $AliasRoot) {
    $AliasRoot = Join-Path $projectParent "wt"
}

New-Item -ItemType Directory -Force -Path $AliasRoot | Out-Null

function Resolve-NormalizedPath {
    param([string]$PathText)

    return (Resolve-Path $PathText).Path
}

function Ensure-Junction {
    param(
        [string]$AliasPath,
        [string]$TargetPath
    )

    $desiredTarget = Resolve-NormalizedPath $TargetPath

    if (Test-Path $AliasPath) {
        $item = Get-Item $AliasPath -Force
        $existingTarget = $null
        $rawTargetIsReparsePoint = $false
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            $rawTarget = @($item.Target) | Where-Object { $_ } | Select-Object -First 1
            if ($rawTarget) {
                if (Test-Path $rawTarget) {
                    $existingTarget = Resolve-NormalizedPath $rawTarget
                    $rawTargetItem = Get-Item $rawTarget -Force
                    $rawTargetIsReparsePoint = [bool]($rawTargetItem.Attributes -band [IO.FileAttributes]::ReparsePoint)
                }
                else {
                    $existingTarget = [IO.Path]::GetFullPath($rawTarget)
                }
            }
        }

        if (-not $existingTarget) {
            $existingTarget = $item.FullName
        }

        if ($existingTarget -eq $desiredTarget -and -not $rawTargetIsReparsePoint) {
            return [pscustomobject]@{
                Alias = $AliasPath
                Target = $desiredTarget
                Status = "existing"
            }
        }

        if (-not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Alias conflict at '$AliasPath': existing target '$existingTarget' != desired '$desiredTarget'."
        }

        cmd /c rmdir $AliasPath | Out-Null
        New-Item -ItemType Junction -Path $AliasPath -Target $desiredTarget | Out-Null
        return [pscustomobject]@{
            Alias = $AliasPath
            Target = $desiredTarget
            Status = "rewired"
        }
    }

    New-Item -ItemType Junction -Path $AliasPath -Target $desiredTarget | Out-Null
    return [pscustomobject]@{
        Alias = $AliasPath
        Target = $desiredTarget
        Status = "created"
    }
}

$shortAliasPattern = '^[A-Za-z]\d+[A-Za-z0-9]*$'

function Get-AliasNames {
    param([string]$NormalizedPath)

    $leaf = Split-Path $NormalizedPath -Leaf
    $aliasNames = [System.Collections.Generic.List[string]]::new()
    $aliasNames.Add($leaf)

    $prefix = $leaf.Split("-")[0]
    if ($prefix -ne $leaf -and $prefix -match $shortAliasPattern) {
        $aliasNames.Add($prefix)
    }

    return $aliasNames | Select-Object -Unique
}

$registeredAliases = @()
$seenAliasNames = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$projectRootNormalized = Resolve-NormalizedPath $projectRoot

$worktreeLines = git worktree list --porcelain
$worktreePaths = $worktreeLines | Where-Object { $_ -like "worktree *" } | ForEach-Object { $_.Substring(9) }

foreach ($worktreePath in $worktreePaths) {
    $normalized = Resolve-NormalizedPath $worktreePath
    if ($normalized -eq $projectRootNormalized) {
        continue
    }

    foreach ($aliasName in Get-AliasNames $normalized) {
        if ($seenAliasNames.Add($aliasName)) {
            $registeredAliases += Ensure-Junction (Join-Path $AliasRoot $aliasName) $normalized
        }
    }
}

if ($MirrorLegacyShortcuts -and (Test-Path "D:\wt")) {
    foreach ($item in Get-ChildItem "D:\wt" -Directory) {
        if (-not $seenAliasNames.Add($item.Name)) {
            continue
        }
        $registeredAliases += Ensure-Junction (Join-Path $AliasRoot $item.Name) $item.FullName
    }
}

Write-Host "Synchronized repo-local worktree aliases:"
$registeredAliases | Sort-Object Alias | Format-Table Alias, Target, Status -AutoSize

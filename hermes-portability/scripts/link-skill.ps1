<#
.SYNOPSIS
  Point every agent's skills directory at this skill's source folder (one copy on disk).

.DESCRIPTION
  A skill usually exists twice: the source repo you edit, and the copy an agent loads.
  Editing one leaves the other stale. This script replaces the loaded copy with a
  directory junction, so the source becomes the single source of truth.

  Existing REAL directories are renamed to "<name>.bak-<timestamp>" first - never deleted.
  Junctions on Windows need no administrator rights and are transparent to readers.

.PARAMETER Skill
  Skill directory name to link. Defaults to the skill that contains this script.

.PARAMETER Roots
  Extra skills roots to include (auto-discovered roots are always scanned).

.PARAMETER DryRun
  Show what would change without touching the filesystem.

.PARAMETER Install
  Also create links in agent roots that do not have this skill yet.
  Default is to only re-point copies that already exist (no surprise installs).

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File link-skill.ps1
.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File link-skill.ps1 -DryRun
#>
[CmdletBinding()]
param(
    [string[]]$Skill = @(),
    [string[]]$Roots = @(),
    [switch]$DryRun,
    [switch]$Install
)

$ErrorActionPreference = 'Stop'

$skillDir = Split-Path -Parent $PSScriptRoot          # .../<skill>
$repoRoot = Split-Path -Parent $skillDir               # .../  (parent of the skill)
if ($Skill.Count -eq 0) { $Skill = @(Split-Path -Leaf $skillDir) }

function Get-SkillsRoots {
    param([string[]]$extra)

    $homeDir = $env:USERPROFILE
    $candidates = New-Object System.Collections.Generic.List[string]

    # Known layouts (only used when they already exist - we never create agent dirs).
    $known = @(
        '.workbuddy\skills', '.claude\skills', '.codex\skills', '.agents\skills',
        '.cc-switch\skills', '.cursor\skills', 'Doubao\skills', 'DoubaoWork\skills'
    )
    foreach ($k in $known) {
        $p = Join-Path $homeDir $k
        if (Test-Path -LiteralPath $p -PathType Container) { $candidates.Add($p) }
    }

    # Auto-discovery: <home>\*\skills (one level deep, existing dirs only).
    Get-ChildItem -LiteralPath $homeDir -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
        $cand = Join-Path $_.FullName 'skills'
        if (Test-Path -LiteralPath $cand -PathType Container) { $candidates.Add($cand) }
    }

    foreach ($e in $extra) {
        if ($e -and (Test-Path -LiteralPath $e -PathType Container)) { $candidates.Add($e) }
    }

    $candidates | Sort-Object -Unique
}

function Get-FullPath {
    param([string]$p)
    return [System.IO.Path]::GetFullPath($p).TrimEnd('\')
}

$roots = Get-SkillsRoots -extra $Roots
if ($roots.Count -eq 0) {
    Write-Host 'No agent skills directory found.' -ForegroundColor Yellow
    exit 1
}

$results = New-Object System.Collections.Generic.List[object]
$failed = 0

foreach ($name in $Skill) {
    $src = Join-Path $repoRoot $name
    if (-not (Test-Path -LiteralPath (Join-Path $src 'SKILL.md') -PathType Leaf)) {
        Write-Host "Skip: $src has no SKILL.md" -ForegroundColor Yellow
        $failed++
        continue
    }
    $srcFull = Get-FullPath $src

    foreach ($root in $roots) {
        $dst = Join-Path $root $name
        $action = 'created'
        $note = ''

        $item = Get-Item -LiteralPath $dst -Force -ErrorAction SilentlyContinue
        if ($null -eq $item -and -not $Install) {
            # Nothing installed here: do not install silently. Use -Install to opt in.
            $results.Add([pscustomobject]@{ Action = 'skipped(not-installed)'; Path = $dst; Note = 'use -Install' })
            continue
        }
        if ($null -ne $item) {
            $isLink = ($item.LinkType -eq 'Junction') -or ($item.LinkType -eq 'SymbolicLink')
            if ($isLink) {
                $target = @($item.Target)[0]
                if ($target -and ((Get-FullPath $target) -ieq $srcFull)) {
                    $action = 'already-linked'
                } else {
                    $action = 'relinked'
                    $note = "was -> $target"
                    # No -Recurse: on a junction it would follow the link and delete the target.
                    if (-not $DryRun) { Remove-Item -LiteralPath $dst -Force }
                }
            } else {
                # Back up OUTSIDE the skills root: a "<name>.bak-*" folder inside it would be
                # scanned as a second skill by most agents.
                $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
                $backupDir = Join-Path $env:LOCALAPPDATA 'SkillLinkBackups'
                $backup = Join-Path $backupDir ("{0}-{1}" -f $name, $stamp)
                $action = 'linked'
                $note = "backup: $backup"
                if (-not $DryRun) {
                    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
                    Move-Item -LiteralPath $dst -Destination $backup
                }
            }
        }

        if (-not $DryRun -and $action -ne 'already-linked') {
            New-Item -ItemType Junction -Path $dst -Value $src | Out-Null
        }

        $results.Add([pscustomobject]@{
            Action = $action
            Path   = $dst
            Note   = $note
        })
    }
}

foreach ($r in $results) {
    if ($r.Note) {
        Write-Host ("{0,-22} {1}  ({2})" -f $r.Action, $r.Path, $r.Note)
    } else {
        Write-Host ("{0,-22} {1}" -f $r.Action, $r.Path)
    }
}
if ($DryRun) { Write-Host 'DryRun: nothing was changed.' -ForegroundColor Cyan }
Write-Host ("Roots scanned: {0} | entries: {1}" -f $roots.Count, $results.Count)
if ($failed -gt 0) { exit 1 }
exit 0

# install-all.ps1 — the whole kaanha stack in one command (Windows).
#
#   powershell -ExecutionPolicy Bypass -File scripts\install-all.ps1
#   powershell -ExecutionPolicy Bypass -File scripts\install-all.ps1 -WithCurated
#
# Registers the kaanha-stack marketplace and installs the four kaanha
# plugins (quality, dev, agents, ugc) plus watch-skill (the recommended
# kaanha-ugc engine). -WithCurated also installs the other curated
# third-party pointers. Requires the Claude Code CLI ("claude") on PATH —
# inside the Claude Code app you can instead run the /plugin commands
# from the README.
#
# NOTE before installing kaanha-agents: read docs/agents.md — the squads
# create scheduled tasks, launch a browser, and make local commits.

param([switch]$WithCurated)
# NOT "Stop": Windows PowerShell 5.1 wraps a native command's stderr into
# throwing ErrorRecords whenever the stream is redirected (2>$null here,
# or any CI/host capture) — with EAP=Stop a mere warning on stderr would
# kill the installer. Failures are tracked explicitly via $LASTEXITCODE.
$ErrorActionPreference = "Continue"

$env:Path = $env:Path + ";" +
            [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
            [Environment]::GetEnvironmentVariable("Path", "User")
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Host "[!!] The 'claude' CLI is not on PATH." -ForegroundColor Yellow
    Write-Host "     Install Claude Code first (https://claude.com/claude-code), or run the"
    Write-Host "     /plugin commands from the README inside the app instead."
    exit 1
}

Write-Host "[..] Registering the kaanha-stack marketplace"
claude plugin marketplace add kaanhaAI/kaanha-claude-stack 2>$null
# (already registered is fine - continue either way)

$core = @("kaanha-quality", "kaanha-dev", "kaanha-agents", "kaanha-factory", "kaanha-3d-web", "kaanha-ugc", "watch-skill")
$curated = @("ponytail", "impeccable", "ui-ux-pro-max", "andrej-karpathy-skills", "mempalace", "claude-video")
$list = if ($WithCurated) { $core + $curated } else { $core }

$failed = @()
foreach ($p in $list) {
    Write-Host "[..] Installing $p"
    claude plugin install "$p@kaanha-stack"
    if ($LASTEXITCODE -ne 0) { $failed += $p }
}

Write-Host ""
if ($failed.Count) {
    Write-Host "[!!] Failed: $($failed -join ', ') - re-run this script or install those via /plugin." -ForegroundColor Yellow
    exit 1
}
Write-Host "[ok] Everything installed." -ForegroundColor Green
Write-Host "Start (or restart) a Claude Code session: your first session prints a"
Write-Host "one-time 'what you now have' notice - then say 'give me the kaanha tour'."

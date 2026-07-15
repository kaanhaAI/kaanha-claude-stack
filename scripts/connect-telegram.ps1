# connect-telegram.ps1 — wire the cloud-fleet Telegram alert channel.
#
# The workflow templates in templates/workflows/ send failure alerts to a
# Telegram chat or group when two repo secrets exist: TELEGRAM_BOT_TOKEN +
# TELEGRAM_CHAT_ID. This script sets them on every repo you name, from one
# prompt, with the token validated against Telegram before anything is
# written. Values are piped straight to gh — never written to disk.
#
# Usage (PowerShell 5.1+):
#   .\connect-telegram.ps1 -Repos "you/repo1","you/repo2"
#   .\connect-telegram.ps1 -Repos "you/repo" -FireTest
#
# Prereqs: gh CLI installed + authenticated (winget install GitHub.cli;
# gh auth login). Create your bot with @BotFather and add it to your group.

param(
    [Parameter(Mandatory = $true)][string[]]$Repos,
    [switch]$FireTest
)
$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "gh CLI not found - install with: winget install GitHub.cli (then gh auth login)"
}
gh auth status 2>$null
if ($LASTEXITCODE -ne 0) { gh auth login; if ($LASTEXITCODE -ne 0) { throw "gh auth login failed" } }

# --- token, validated live (getMe) -------------------------------------------
# NOTE: in the classic PowerShell console paste with RIGHT-CLICK, not Ctrl+V.
# A real token is ~46 chars - you should see that many * echoes.
$token = $null
while (-not $token) {
    $sec  = Read-Host "Paste TELEGRAM_BOT_TOKEN (RIGHT-CLICK to paste)" -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
    $t    = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    $t = if ($t) { $t.Trim() } else { "" }
    if ($t.Length -lt 20) { Write-Host "[!!] Only $($t.Length) chars - paste failed? RIGHT-CLICK pastes here." -ForegroundColor Yellow; continue }
    try {
        $me = Invoke-RestMethod -Uri "https://api.telegram.org/bot$t/getMe" -TimeoutSec 15
        Write-Host "[ok] Token valid - this is @$($me.result.username)" -ForegroundColor Green
        $token = $t
    } catch { Write-Host "[!!] Telegram rejected that token - check @BotFather and retry." -ForegroundColor Yellow }
}

# --- chat id: manual, or auto-detect from the bot's updates -------------------
$chatId = Read-Host "Enter TELEGRAM_CHAT_ID (group ids are negative) - or press ENTER to auto-detect"
while (-not $chatId) {
    try { $updates = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getUpdates" -TimeoutSec 15 }
    catch { Read-Host "[!!] getUpdates failed - press ENTER to retry"; continue }
    $chats = @{}
    foreach ($u in $updates.result) {
        foreach ($c in @($u.message.chat, $u.edited_message.chat, $u.channel_post.chat, $u.my_chat_member.chat)) {
            if ($c -and $c.id) { $chats[[string]$c.id] = $c }
        }
    }
    if ($chats.Count -eq 0) {
        Write-Host "[!!] Bot has seen no activity. In your group send: /start@<YourBotName>" -ForegroundColor Yellow
        Write-Host "     (If another service polls this bot's updates, auto-detect may stay empty -"
        Write-Host "      add @getidsbot to the group instead; it posts the chat id, then remove it.)"
        Read-Host  "     Press ENTER to retry, or Ctrl+C to restart and type the id manually"
        continue
    }
    $i = 0; $keys = @($chats.Keys)
    foreach ($k in $keys) {
        $c = $chats[$k]; $i++
        $label = if ($c.title) { $c.title } else { "$($c.first_name) (private chat)" }
        Write-Host ("  [{0}] {1}  ->  {2}  ({3})" -f $i, $label, $c.id, $c.type)
    }
    $pick = Read-Host "Pick the chat by number"
    $idx = 0
    if ([int]::TryParse($pick, [ref]$idx) -and $idx -ge 1 -and $idx -le $keys.Count) { $chatId = $chats[$keys[$idx - 1]].id }
}

# --- set secrets on every repo ------------------------------------------------
foreach ($repo in $Repos) {
    Write-Host "[..] $repo"
    $token  | gh secret set TELEGRAM_BOT_TOKEN --repo $repo
    if ($LASTEXITCODE -ne 0) { throw "failed to set token on $repo" }
    $chatId | gh secret set TELEGRAM_CHAT_ID  --repo $repo
    if ($LASTEXITCODE -ne 0) { throw "failed to set chat id on $repo" }
    Write-Host "[ok] $repo secrets set." -ForegroundColor Green
}
$token = $null

# --- optional: fire the test workflow (templates/workflows/telegram-test.yml) -
if ($FireTest) {
    foreach ($repo in $Repos) {
        gh workflow run telegram-test --repo $repo
        if ($LASTEXITCODE -eq 0) { Write-Host "[ok] telegram-test fired on $repo - watch your group" }
        else { Write-Host "[!!] $repo has no telegram-test workflow (copy it from templates/workflows/)" }
    }
}
Write-Host "Done. Alerts from the fleet templates will now reach your Telegram." -ForegroundColor Cyan

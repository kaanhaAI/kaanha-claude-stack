#!/usr/bin/env bash
# install-all.sh — the whole kaanha stack in one command (macOS/Linux).
#
#   bash scripts/install-all.sh
#   bash scripts/install-all.sh --with-curated
#
# Registers the kaanha-stack marketplace and installs the four kaanha
# plugins (quality, dev, agents, ugc) plus watch-skill (the recommended
# kaanha-ugc engine). --with-curated also installs the other curated
# third-party pointers. Requires the Claude Code CLI ("claude") on PATH.
#
# NOTE before installing kaanha-agents: read docs/agents.md — the squads
# create scheduled tasks, launch a browser, and make local commits.
set -u

if ! command -v claude >/dev/null 2>&1; then
  echo "[!!] The 'claude' CLI is not on PATH."
  echo "     Install Claude Code first (https://claude.com/claude-code), or run the"
  echo "     /plugin commands from the README inside the app instead."
  exit 1
fi

echo "[..] Registering the kaanha-stack marketplace"
claude plugin marketplace add kaanhaAI/kaanha-claude-stack 2>/dev/null || true

plugins=(kaanha-quality kaanha-dev kaanha-agents kaanha-ugc watch-skill)
if [ "${1:-}" = "--with-curated" ]; then
  plugins+=(ponytail impeccable ui-ux-pro-max andrej-karpathy-skills mempalace claude-video)
fi

failed=()
for p in "${plugins[@]}"; do
  echo "[..] Installing $p"
  claude plugin install "$p@kaanha-stack" || failed+=("$p")
done

echo ""
if [ "${#failed[@]}" -gt 0 ]; then
  echo "[!!] Failed: ${failed[*]} - re-run this script or install those via /plugin."
else
  echo "[ok] Everything installed."
fi
echo "Start (or restart) a Claude Code session: your first session prints a"
echo "one-time 'what you now have' notice - then say 'give me the kaanha tour'."

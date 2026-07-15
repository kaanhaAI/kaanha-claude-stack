# Cloud fleet — GitHub Actions templates

The genuinely-24/7 version of the fleet. Local scheduled tasks die when the
Claude app closes; these run on GitHub's infrastructure on a cron whether
your machine is on or off. Wave 1 = the **mechanical** squads (no Claude
API key needed): uptime, dependency audit, e2e.

## What runs where

- **Per-repo** (`dependency-audit.yml`, and your existing CI's build/e2e):
  copy into that repo's `.github/workflows/`. GitHub checks out the repo
  automatically, so no cross-repo token is needed.
- **Uptime** (`site-sentinel.yml`): copy into any repo you control; it only
  needs public URLs, so it can live in an ops repo and watch several sites.

## Adopt

1. Copy the template into `<repo>/.github/workflows/`.
2. Replace the `<...>` placeholders (site URL + routes, or package manager).
3. Commit + push. The workflow appears in the repo's **Actions** tab; run it
   manually once via **Run workflow** to confirm it's green.

## Wave 2 — reasoning squads on Gemini / OpenAI / Grok

`cloud-reasoning.yml` is the provider-agnostic Wave 2 harness (Anthropic
dropped for cost). It gathers the last-24h diff, sends it to the chosen
provider, and files findings as an issue. Set `PROVIDER` + `MODEL` per squad
from `dev/fleet.json` → `cloud_models`, and add the one matching secret:

- `GEMINI_API_KEY` (provider `gemini`) · `OPENAI_API_KEY` (`openai`) · `XAI_API_KEY` (`grok`)

Suggested split (see `cloud_models` for the full map): code-reviewer /
security-auditor → OpenAI GPT-5.6; code-guardian / design / growth-marketer
→ Gemini; growth-scout → Grok (real-time web); daily-ops → Gemini Flash-Lite.

**Two honest limits:** (1) the **overnight-builder** does autonomous
multi-file code generation — that needs a real agent loop, not this
single-call harness; keep it on Claude Code. (2) The **local** fleet squads
run inside the Claude app on your flat subscription — they cost nothing
per-token and are unaffected by this switch; only these cloud workflows use
the paid provider APIs.

Wave 1 (site-sentinel, dependency-audit) still needs no secrets.

# Curated companion plugins

The marketplace also carries pointers to the best open-source Claude Code plugins we know — installed **from their authors' upstream repos**, with full credit. Our repo is the catalog, not a copy.

| Plugin | Author | What it does | Install |
|---|---|---|---|
| **ponytail** | [Dietrich Gebert](https://github.com/DietrichGebert/ponytail) | "Laziest senior dev" persona: a 7-rung YAGNI ladder before any code gets written (`/ponytail lite\|full\|ultra\|off`, plus review/audit/debt companions) | `/plugin install ponytail@kaanha-stack` |
| **impeccable** | [Paul Bakaus](https://github.com/pbakaus/impeccable) | Design lifecycle toolkit: `/impeccable` with 23 commands (craft, critique, audit, polish, live) + 44 deterministic anti-slop detectors | `/plugin install impeccable@kaanha-stack` |
| **ui-ux-pro-max** | [nextlevelbuilder](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Offline searchable design database (84 styles, 192 palettes, 74 font pairings, 22 stacks) with persistent per-project design systems | `/plugin install ui-ux-pro-max@kaanha-stack` |
| **karpathy-skills** | [forrestchang / multica-ai](https://github.com/multica-ai/andrej-karpathy-skills) | Four coding principles distilled from Karpathy's LLM-pitfall observations — a lighter alternative to ponytail (pick one, not both) | `/plugin install andrej-karpathy-skills@kaanha-stack` |
| **mempalace** | [MemPalace](https://github.com/MemPalace/mempalace) | Local-first AI memory: verbatim storage, semantic search, knowledge graph. Needs its engine installed separately (`uv tool install mempalace`, ~300 MB models) | `/plugin install mempalace@kaanha-stack` |

**Also recommended** (not a plugin, install separately): [hallmark](https://github.com/Nutlope/hallmark) by Hassan El Mghari / Together AI — anti-slop page building with 21 page structures, 20 themes, and a 58-gate slop test. Install: `npx skills add nutlope/hallmark`.

## How they compose

- **One coding-discipline plugin**: ponytail *or* karpathy — they overlap.
- **Design plugins have distinct jobs**: ui-ux-pro-max decides the *system* (palette, fonts, per-industry grounding), hallmark builds fresh *pages*, impeccable owns the *lifecycle* of existing UI. Enabling all three at once works but increases the chance of overlapping triggers — start with the one matching your work.
- **Everything composes with kaanha-quality**: ponytail writes less code, the ship pipeline verifies what's left, the gate enforces it.

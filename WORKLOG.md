# WORKLOG

## Purpose

This file is the shared handoff log for collaborators working on the public showcase version of this repository.
Keep entries short, factual, and client-safe.

## Current Direction

- The repository is positioned as an English-language public showcase.
- Marketplace references are generic: `Marketplace A`, `Marketplace B`, and `Demo`.
- Public materials avoid naming specific vendors or regions.
- The bot demonstrates architecture, operator flows, and integration patterns rather than a single production deployment.

## Decisions

### 2026-03-09 Codex

- Reframed the repository as a client-facing GitHub showcase for marketplace automation work.
- Rewrote the main public documentation in English.
- Removed provider-specific naming from onboarding, handlers, and configuration.
- Replaced provider-specific adapters with generic placeholders:
  - `bot/services/marketplace_a_api.py`
  - `bot/services/marketplace_b_api.py`
- Updated deployment configuration for generic provider flags.
- Kept the internal project structure intact so future private integrations can be added without another rewrite.

## Notes For Collaborators

- Keep copy in English.
- Keep provider naming generic in public files.
- If a real client implementation is needed later, add it in a private branch or private repository layer.
- Do not reintroduce vendor-specific claims into README or public marketing docs.

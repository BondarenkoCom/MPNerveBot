# MPNerveBot Master Plan

This repository is now maintained as a public-safe showcase for a Telegram-first marketplace operations bot.

## What We Are Building

A lightweight bot that helps marketplace merchants monitor daily performance, track urgent issues, and act from Telegram.

## Public Safe Rule

The public version of this repository does not name real marketplace vendors.
Use generic labels:

- `Marketplace A`
- `Marketplace B`
- `Demo Mode`

Provider-specific implementations can exist privately outside this public showcase.

## Stack

- Python 3.11+
- `python-telegram-bot`
- `httpx`
- `SQLite`
- optional AI provider integrations

## MVP Features

1. Onboarding
   connect one marketplace account or enter demo mode
2. Daily Digest
   orders, revenue, stock risk, review backlog, anomaly summary
3. Alerts
   low stock, sales drop, unanswered reviews
4. Review Support
   draft reply generation and operator review flow
5. Commands
   `/start`, `/digest`, `/alerts`, `/reviews`, `/status`, `/help`

## Project Principles

- keep it Telegram-first
- keep it mock-first
- keep the public repo generic and client-facing
- keep user-facing copy in English in this public showcase
- keep the code simple

## Execution Direction

Phase 1:
- stable bot skeleton
- docs and architecture
- demo mode

Phase 2:
- generic provider adapters
- persistence and onboarding
- scheduled jobs

Phase 3:
- AI-assisted workflows
- polish and stronger showcase quality

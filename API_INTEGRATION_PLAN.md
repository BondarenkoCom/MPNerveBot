# API Integration Plan

## Goal

Keep the public repository generic while preserving a believable integration architecture.

## Public Repository Strategy

In this showcase, provider adapters are represented as:

- `Marketplace A`
- `Marketplace B`

The public repo should demonstrate:

- adapter structure
- validation flow
- normalized response shapes
- service boundaries

It should not expose:

- private provider endpoints
- vendor-specific commercial assumptions
- account-specific production workflows

## Normalized Contract

Each provider adapter should support:

- credential validation
- daily digest snapshot
- unanswered review fetch
- alert snapshot

## Public Demo Behavior

For the showcase repo, generic adapters may be:

- mock-only
- partially stubbed
- or sanitized placeholder implementations

The important part is the system shape, not vendor-specific hardcoding.

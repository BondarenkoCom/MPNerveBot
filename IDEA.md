# Product Idea

## Working Name

MPNerveBot

## Positioning

A Telegram operations bot for Wildberries and Ozon sellers.

The product closes an operational pain, not a reporting pain. Sellers already have marketplace dashboards. They still miss important actions because the work is split between multiple apps, tabs, and team members.

## Main Problem

Small and mid sellers do not need another heavy dashboard.

They need:
- one daily picture of what matters today
- one place to catch urgent issues
- one fast way to react to reviews, questions, and stock problems
- one operational surface they can share with a manager

## Target Users

Primary:
- Wildberries and Ozon sellers with 20-300 SKU
- owner-operated stores
- small teams with 1-5 managers

Secondary:
- agencies or assistants managing multiple seller accounts

## Core Jobs To Be Done

1. Tell me what needs attention today without making me open two marketplace apps.
2. Warn me before stockouts or obvious sales drops hurt the business.
3. Show me unanswered feedback that should not sit untouched.
4. Let me act from Telegram, not from five separate dashboards.

## MVP

### Seller Onboarding

- choose marketplace: Wildberries / Ozon / both
- connect seller credentials
- choose Telegram destination: personal chat or team chat

### Daily Digest

- sales delta
- stock risk summary
- unanswered feedback summary
- top anomalies that need action

### Alerts

- low stock / probable stockout
- strong sales drop
- unanswered feedback over threshold

### AI Layer

- draft reply suggestions for feedback
- concise explanation of why an alert was raised

### Team Use

- owner can add a manager or use a shared Telegram group

## What We Explicitly Avoid In V1

- full dashboard clone
- deep finance/accounting
- complex BI
- full CRM
- mobile app
- public app store launch

## Monetization

Free:
- 1 marketplace
- limited SKU count
- one daily digest

Paid Basic:
- 1 marketplace
- alerts
- higher limits

Paid Pro:
- Wildberries + Ozon
- team chat
- AI drafts
- priority alerts

## Why This Can Work Fast

- Telegram is the natural interface for this audience
- the product can start as a bot plus a thin admin layer
- first sales can be manual
- distribution can start from seller communities, not app stores

## Why The Existing Job Bot Is Not The Model

The ENG job bot is a portfolio example.

This product is different:
- Russian-speaking market
- B2B pain
- daily operational use
- recurring value

## Build Principle

Ship the smallest useful control loop:

input -> signal -> action

Not:

input -> giant dashboard -> user fatigue

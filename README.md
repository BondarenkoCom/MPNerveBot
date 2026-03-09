# MPNerveBot

Telegram-first operations bot for Wildberries and Ozon sellers.

The product is not another analytics dashboard. It is a daily control layer in Telegram for sellers who already have data, but do not have a clean operational workflow.

Core idea:
- connect Wildberries and Ozon seller tokens
- send a daily digest into Telegram
- alert on stock risks, unanswered feedback, and sales anomalies
- generate AI draft replies for marketplace feedback
- support owner + manager workflows inside one chat

Why this direction:
- it fits current engineering speed
- it fits Russian-speaking СНГ users better than the existing ENG job bot
- it can be sold as a lightweight B2B tool before building a full web product
- it does not require app stores on day 1

Primary audience:
- Russian-speaking sellers on Wildberries and Ozon
- first pilots: small and mid sellers with 20-300 SKU
- first paying clients are easier to close in СНГ where foreign-bank/manual-payment friction is lower

Initial product shape:
- Telegram bot
- lightweight web admin page
- daily digest
- stock alerts
- feedback alerts
- AI reply drafts

See:
- `IDEA.md` for product scope
- `MARKETING.md` for go-to-market
- `AGENTS.md` for collaboration rules

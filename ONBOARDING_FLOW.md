# Onboarding Flow

## Paths

### Demo Mode

1. User sends `/start`
2. Bot offers `Marketplace A`, `Marketplace B`, or `Demo`
3. User selects `Demo`
4. Bot enables mock accounts and confirms available commands

### Marketplace A

1. User sends `/start`
2. User selects `Marketplace A`
3. Bot asks for account credentials
4. Bot validates or stores the connection

### Marketplace B

1. User sends `/start`
2. User selects `Marketplace B`
3. Bot asks for account credentials
4. Bot validates or stores the connection

## State Machine

- `idle`
- `choose_marketplace`
- `enter_marketplace_a_credentials`
- `enter_marketplace_b_credentials`
- `connected`
- `invalid`

## Copy Rules

- concise
- action-oriented
- English in the public showcase

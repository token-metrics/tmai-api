# Token Metrics QuickNode Add-On

This integration provides a QuickNode Add-On for the Token Metrics AI API, allowing QuickNode users to access cryptocurrency ratings, factors, and sentiment analysis.

## Features

- Express proxy for Token Metrics AI API
- Provision and deprovision hooks for user management
- JWT authentication with required claims
- Pricing tiers with 10% discount for TMAI token payments

## Components

### Express Proxy

The Express server provides endpoints for:
- `/ratings` - Get cryptocurrency ratings
- `/factors` - Get cryptocurrency factors
- `/sentiments` - Get cryptocurrency sentiment
- `/provision` - Hook for user subscription
- `/deprovision` - Hook for subscription cancellation
- `/status` - Health check endpoint

### Pricing Configuration

The `pricing.json` file defines:
- Multiple subscription tiers (Basic, Standard, Professional, Enterprise)
- Features and limits for each tier
- Payment methods with TMAI token discount

## Installation

```bash
# Install dependencies
npm install

# Start the server
npm start
```

## Environment Variables

- `PORT` - Server port (default: 3000)
- `TM_API_BASE_URL` - Token Metrics API base URL
- `JWT_SECRET` - Secret for JWT signing and verification

## Testing

```bash
# Run tests
npm test
```

## Acceptance Criteria

The QuickNode Add-On has been tested to ensure:
- QuickNode test invoice shows 10% pay-in break for TMAI token payments
- Tier caps are enforced based on subscription plan
- Provision and deprovision hooks work correctly

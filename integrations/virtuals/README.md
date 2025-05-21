# Token Metrics Virtuals TM-Oracle

This integration provides a blockchain oracle for the Token Metrics AI API, allowing smart contracts to access cryptocurrency ratings, technical scores, and fundamental scores.

## Features

- Solidity oracle contract (v0.8.21)
- TypeScript keeper script to update oracle data
- Comprehensive Hardhat tests
- Integration with veTMAI staking contract for access control

## Components

### TMOracle.sol

The Solidity oracle contract stores and provides access to Token Metrics ratings data:
- Only users with veTMAI stake can access the data
- Only the designated keeper can update ratings
- Provides methods to access overall ratings, technical scores, and fundamental scores

### oracle-keeper.ts

A TypeScript script that:
- Fetches data from the Token Metrics API
- Updates the blockchain oracle at regular intervals
- Handles multiple cryptocurrency symbols

## Installation

```bash
# Install dependencies
npm install

# Compile contracts
npm run build

# Run tests
npm run test
```

## Configuration

Create a `.env` file with the following variables:
```
TM_API_BASE_URL=https://api.tokenmetrics.com/v2
TM_API_KEY=your_api_key
ORACLE_ADDRESS=deployed_oracle_address
RPC_URL=blockchain_rpc_url
PRIVATE_KEY=keeper_private_key
UPDATE_INTERVAL=3600000
SYMBOLS=BTC,ETH,SOL,DOGE,AVAX
```

## Deployment

```bash
# Deploy oracle
npm run deploy

# Start keeper
npm run keeper
```

## Security

- The oracle contract requires veTMAI stake to access data
- Only the designated keeper can update ratings
- Solidity 0.8.21 with optimizer runs set to 1000
- No external calls in the smart contract

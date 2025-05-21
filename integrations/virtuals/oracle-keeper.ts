import { ethers } from 'ethers';
import axios from 'axios';
import * as dotenv from 'dotenv';
import * as TMOracle from './artifacts/contracts/TMOracle.sol/TMOracle.json';

dotenv.config();

// Configuration
const TM_API_BASE_URL = process.env.TM_API_BASE_URL || 'https://api.tokenmetrics.com/v2';
const TM_API_KEY = process.env.TM_API_KEY || '';
const ORACLE_ADDRESS = process.env.ORACLE_ADDRESS || '';
const RPC_URL = process.env.RPC_URL || '';
const PRIVATE_KEY = process.env.PRIVATE_KEY || '';
const UPDATE_INTERVAL = process.env.UPDATE_INTERVAL ? parseInt(process.env.UPDATE_INTERVAL) : 3600000; // 1 hour default
const SYMBOLS = (process.env.SYMBOLS || 'BTC,ETH,SOL,DOGE,AVAX').split(',');

// Validate configuration
if (!TM_API_KEY) {
  console.error('Error: Token Metrics API key not provided');
  process.exit(1);
}

if (!ORACLE_ADDRESS) {
  console.error('Error: Oracle contract address not provided');
  process.exit(1);
}

if (!PRIVATE_KEY) {
  console.error('Error: Private key not provided');
  process.exit(1);
}

// Initialize ethers provider and wallet
const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
const oracle = new ethers.Contract(ORACLE_ADDRESS, TMOracle.abi, wallet);

/**
 * Fetch ratings from Token Metrics API
 * @param symbol Token symbol
 * @returns Rating data
 */
async function fetchRating(symbol: string) {
  try {
    const response = await axios.get(`${TM_API_BASE_URL}/ratings`, {
      headers: {
        'accept': 'application/json',
        'api_key': TM_API_KEY
      },
      params: {
        symbol,
        limit: 1
      }
    });

    if (response.data?.data?.length > 0) {
      const ratingData = response.data.data[0];
      return {
        symbol: ratingData.symbol,
        rating: Math.round(ratingData.rating * 100),
        technical: Math.round(ratingData.technical_score * 100),
        fundamental: Math.round(ratingData.fundamental_score * 100)
      };
    }
    
    throw new Error(`No rating data found for ${symbol}`);
  } catch (error) {
    console.error(`Error fetching rating for ${symbol}:`, error);
    throw error;
  }
}

/**
 * Update oracle with latest ratings
 */
async function updateOracle() {
  try {
    console.log('Starting oracle update...');
    
    for (const symbol of SYMBOLS) {
      try {
        console.log(`Fetching rating for ${symbol}...`);
        const rating = await fetchRating(symbol);
        
        console.log(`Updating oracle for ${symbol}:`, rating);
        const tx = await oracle.updateRating(
          rating.symbol,
          rating.rating,
          rating.technical,
          rating.fundamental
        );
        
        console.log(`Transaction sent: ${tx.hash}`);
        await tx.wait();
        console.log(`Rating updated for ${symbol}`);
      } catch (error) {
        console.error(`Failed to update ${symbol}:`, error);
      }
    }
    
    console.log('Oracle update completed');
  } catch (error) {
    console.error('Error in updateOracle:', error);
  }
}

// Run initial update
updateOracle();

// Schedule regular updates
setInterval(updateOracle, UPDATE_INTERVAL);

console.log(`Oracle keeper started, updating every ${UPDATE_INTERVAL / 1000} seconds`);

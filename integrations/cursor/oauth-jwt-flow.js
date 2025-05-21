/**
 * OAuth to JWT conversion flow for Token Metrics API
 * 
 * This module handles the conversion of OAuth credentials to JWT tokens
 * with the required claims for the Token Metrics API:
 * - plan: User subscription plan
 * - payment_method: Payment method used
 * - stake_score: Staking score for discounts
 */

const axios = require('axios');
const jwt = require('jsonwebtoken');

/**
 * Convert OAuth token to JWT with required claims
 * 
 * @param {string} oauthToken - OAuth token from authentication flow
 * @returns {Promise<string>} - JWT token with required claims
 */
async function convertOAuthToJWT(oauthToken) {
  try {
    // Get user information from OAuth token
    const userResponse = await axios.get('https://api.tokenmetrics.com/v2/user', {
      headers: {
        'Authorization': `Bearer ${oauthToken}`
      }
    });
    
    const userData = userResponse.data;
    
    // Create JWT with required claims
    const jwtPayload = {
      sub: userData.id,
      plan: userData.subscription.plan,
      payment_method: userData.subscription.payment_method,
      stake_score: userData.stake_score || 0,
      exp: Math.floor(Date.now() / 1000) + (60 * 60) // 1 hour expiration
    };
    
    // Note: In a real implementation, the JWT would be signed with a private key
    // For this example, we're using a placeholder
    // The actual signing would happen on the Token Metrics server
    return jwt.sign(jwtPayload, 'PLACEHOLDER_PRIVATE_KEY');
  } catch (error) {
    console.error('Error converting OAuth token to JWT:', error);
    throw new Error('Failed to convert OAuth token to JWT');
  }
}

module.exports = {
  convertOAuthToJWT
};

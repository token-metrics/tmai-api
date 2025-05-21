/**
 * Token Metrics QuickNode Add-On
 * 
 * Express proxy for Token Metrics AI API with provision/deprovision hooks
 */

const express = require('express');
const axios = require('axios');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Environment variables (would be set via HashiCorp Vault in production)
const TM_API_BASE_URL = process.env.TM_API_BASE_URL || 'https://api.tokenmetrics.com/v2';
const JWT_SECRET = process.env.JWT_SECRET || 'development_secret';

/**
 * Provision hook - Called when a user subscribes to the add-on
 */
app.post('/provision', async (req, res) => {
  try {
    const { customerId, planId, apiKey } = req.body;
    
    // Validate required fields
    if (!customerId || !planId) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    // Map QuickNode plan to Token Metrics plan
    const tmPlan = mapPlanIdToTMPlan(planId);
    
    // Create JWT token with required claims
    const token = jwt.sign({
      customer_id: customerId,
      plan: tmPlan,
      payment_method: 'quicknode',
      stake_score: 0.1, // 10% discount for QuickNode users
      exp: Math.floor(Date.now() / 1000) + (365 * 24 * 60 * 60) // 1 year expiration
    }, JWT_SECRET);
    
    // Store token and customer info in database (simplified for this example)
    // In production, this would use a proper database
    console.log(`Provisioned customer ${customerId} with plan ${tmPlan}`);
    
    // Return success with token
    return res.status(200).json({
      success: true,
      token,
      message: 'Successfully provisioned Token Metrics API access'
    });
  } catch (error) {
    console.error('Provision error:', error);
    return res.status(500).json({ error: 'Internal server error during provisioning' });
  }
});

/**
 * Deprovision hook - Called when a user cancels their subscription
 */
app.post('/deprovision', async (req, res) => {
  try {
    const { customerId } = req.body;
    
    if (!customerId) {
      return res.status(400).json({ error: 'Missing customerId' });
    }
    
    // In production, this would revoke the token and update the database
    console.log(`Deprovisioned customer ${customerId}`);
    
    return res.status(200).json({
      success: true,
      message: 'Successfully deprovisioned Token Metrics API access'
    });
  } catch (error) {
    console.error('Deprovision error:', error);
    return res.status(500).json({ error: 'Internal server error during deprovisioning' });
  }
});

/**
 * Proxy endpoint for ratings
 */
app.get('/ratings', authenticateToken, async (req, res) => {
  try {
    const response = await axios.get(`${TM_API_BASE_URL}/ratings`, {
      headers: { Authorization: `Bearer ${req.token}` },
      params: req.query
    });
    
    return res.status(200).json(response.data);
  } catch (error) {
    console.error('Ratings proxy error:', error);
    return res.status(error.response?.status || 500).json(error.response?.data || { error: 'Internal server error' });
  }
});

/**
 * Proxy endpoint for factors
 */
app.get('/factors', authenticateToken, async (req, res) => {
  try {
    const response = await axios.get(`${TM_API_BASE_URL}/factors`, {
      headers: { Authorization: `Bearer ${req.token}` },
      params: req.query
    });
    
    return res.status(200).json(response.data);
  } catch (error) {
    console.error('Factors proxy error:', error);
    return res.status(error.response?.status || 500).json(error.response?.data || { error: 'Internal server error' });
  }
});

/**
 * Proxy endpoint for sentiment
 */
app.get('/sentiments', authenticateToken, async (req, res) => {
  try {
    const response = await axios.get(`${TM_API_BASE_URL}/sentiments`, {
      headers: { Authorization: `Bearer ${req.token}` },
      params: req.query
    });
    
    return res.status(200).json(response.data);
  } catch (error) {
    console.error('Sentiment proxy error:', error);
    return res.status(error.response?.status || 500).json(error.response?.data || { error: 'Internal server error' });
  }
});

/**
 * Status endpoint for health checks
 */
app.get('/status', (req, res) => {
  return res.status(200).json({ status: 'ok' });
});

/**
 * Middleware to authenticate JWT token
 */
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Missing authentication token' });
  }
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    req.token = token;
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Invalid or expired token' });
  }
}

/**
 * Map QuickNode plan ID to Token Metrics plan
 */
function mapPlanIdToTMPlan(planId) {
  const planMap = {
    'qn_basic': 'basic',
    'qn_standard': 'standard',
    'qn_professional': 'professional',
    'qn_enterprise': 'enterprise'
  };
  
  return planMap[planId] || 'basic';
}

// Start server
app.listen(PORT, () => {
  console.log(`Token Metrics QuickNode Add-On running on port ${PORT}`);
});

module.exports = app; // For testing

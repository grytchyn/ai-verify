require('dotenv').config();

const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const rateLimit = require('rate-limit-postgresql');
const { z } = require('zod');

const app = express();
app.use(cors());
app.use(express.json());

// Database connection
const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'ai_verify',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD,
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API routes
const apiRouter = require('./routes/api');
app.use('/api/v1', apiRouter);

// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`✅ AI-Verify Backend API running on port ${PORT}`);
  console.log(`🔗 Health: http://localhost:${PORT}/health`);
  console.log(`🔗 API: http://localhost:${PORT}/api/v1`);
});

module.exports = { app, pool };

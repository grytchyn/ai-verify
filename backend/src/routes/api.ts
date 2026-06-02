// AI-Verify Backend Routes (ESM-compatible)
import express from 'express';
import { complianceRouter } from './compliance.ts';
import { organizationRouter } from './organization.ts';
import { authRouter } from './auth.ts';
import { dpoRouter } from './dpo.ts';
import { webhooksRouter } from './webhooks.ts';

const router = express.Router();

// Health
router.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API routes
router.use('/compliance', complianceRouter);
router.use('/organizations', organizationRouter);
router.use('/auth', authRouter);
router.use('/dpo', dpoRouter);
router.use('/webhooks', webhooksRouter);

export default router;

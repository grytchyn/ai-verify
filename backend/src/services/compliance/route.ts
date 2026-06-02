// AI-Verify Backend — Compliance Service
import { Router, Request, Response } from 'express';
import { z } from 'zod';

const router = Router();

// Request Schema
const AnalyzeSchema = z.object({
  url: z.string().url({ message: 'Invalid URL format' }),
  formData: z.object({
    company_size: z.string(),
    sector: z.string(),
    annual_revenue: z.string(),
    country: z.string(),
    url: z.string().url(),
    ai_systems_count: z.string().optional(),
    deployment_type: z.string().optional(),
    decision_type: z.string().optional(),
    risk_self_assessment: z.string().optional(),
    has_documentation: z.string().optional(),
    dpo_appointed: z.string().optional(),
    previous_audits: z.string().optional(),
  }),
});

// POST /api/v1/compliance/analyze
router.post('/analyze', async (req: Request, res: Response) => {
  try {
    const { url, formData } = req.body;

    // Validate input
    const parsed = AnalyzeSchema.safeParse({ url, formData });
    if (!parsed.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: parsed.error.issues.map(i => ({ path: i.path.join('.'), message: i.message })),
      });
    }

    // Call AI Engine
    const aiEngineUrl = process.env.AI_ENGINE_URL || 'http://localhost:3002';
    const aiResponse = await fetch(`${aiEngineUrl}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, formData }),
    });

    if (!aiResponse.ok) {
      const error = await aiResponse.json();
      return res.status(500).json({ error: 'AI analysis failed', details: error });
    }

    const analysis = await aiResponse.json();

    // Save to database
    // TODO: Implement DB save
    console.log('Analysis saved:', analysis);

    // Return result
    res.json({
      success: true,
      data: {
        id: analysis.id,
        score: analysis.score,
        riskLevel: analysis.risk_level,
        recommendations: analysis.recommendations || [],
      },
    });
  } catch (e) {
    console.error('Compliance analysis failed:', e);
    res.status(500).json({ error: 'Internal server error', details: e.message });
  }
});

// GET /api/v1/compliance/checks (List user's compliance checks)
router.get('/checks', async (req: Request, res: Response) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const limit = parseInt(req.query.limit as string) || 20;
    const orgId = req.query.org_id as string;

    // TODO: Implement DB query
    const checks = [];

    res.json({
      success: true,
      data: {
        checks,
        pagination: {
          page,
          limit,
          total: checks.length,
        },
      },
    });
  } catch (e) {
    res.status(500).json({ error: 'Failed to fetch checks', details: e.message });
  }
});

// GET /api/v1/compliance/checks/:id
router.get('/checks/:id', async (req: Request, res: Response) => {
  try {
    const id = req.params.id;

    // TODO: Implement DB query
    const check = null;

    if (!check) {
      return res.status(404).json({ error: 'Check not found' });
    }

    res.json({ success: true, data: check });
  } catch (e) {
    res.status(500).json({ error: 'Failed to fetch check details', details: e.message });
  }
});

export { router as complianceRouter };

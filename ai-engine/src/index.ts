// AI-Verify AI Engine — Main Server
import express from 'express';
import cors from 'cors';
import { analyzeCompliance } from './analyze.js';

const app = express();
app.use(cors());
app.use(express.json());

// Health
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Analyze endpoint
app.post('/analyze', async (req, res) => {
  try {
    const { url, formData } = req.body;
    
    console.log('Analyzing:', url);
    const result = await analyzeCompliance(url, formData);
    
    res.json({
      success: true,
      data: {
        id: `check-${Date.now()}`,
        ...result,
      },
    });
  } catch (e) {
    console.error('Analysis error:', e);
    res.status(500).json({ error: 'Analysis failed', details: e.message });
  }
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
  console.log(`✅ AI Engine running on port ${PORT}`);
  console.log(`🔗 Health: http://localhost:${PORT}/health`);
});

export { app };

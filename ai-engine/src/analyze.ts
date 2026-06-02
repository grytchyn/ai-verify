// AI-Verify AI Engine — LLM Integration
import OpenAI from 'openai';
import { PineconeClient } from 'pinecone-client';
import 'dotenv/config';

const pinecone = new PineconeClient();
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Prompt templates
const COMPLIANCE_PROMPT = `
You are an AI Act Compliance Expert. Analyze a company's website and AI practices for EU AI Act compliance.

Form Data:
{form_data}

Website Content:
{website_title}
{website_content}

Analyze for:
1. AI Use Cases and deployment types
2. Risk classification (unacceptable/high/limited/minimal)
3. Required documentation (transparency, human oversight, etc.)
4. High-risk category alignment ( Annex III )

Respond in JSON:
{{
  "score": 0-100,
  "risk_level": "unacceptable"|"high"|"limited"|"minimal"|"unknown",
  "recommendations": ["string"],
  "ai_act_references": ["Article X"],
  "high_risk_categories": ["biometric", "crediting", "education", "employment", "law_enforcement", "critical_infra", "mig_asyl", "marshalling"],
  "ai_systems": [
    {{
      "name": "string",
      "deployment_type": "internal"|customer-facing|both|third-party,
      "decision_type": "fully-automated"|human-in-the-loop|decision-support|recommendation,
      "risk_self_assessment": "minimal"|"limited"|"high"|"unacceptable"|"unknown",
      "risk_factors": ["string"],
      "mitigation_measures": ["string"]
    }}
  ]
}};
`;

// Analyze function
export async function analyzeCompliance(url, formData) {
  try {
    // Fetch website content
    const websiteData = await fetchWebsiteData(url);
    
    // Build prompt
    const prompt = COMPLIANCE_PROMPT
      .replace('{form_data}', JSON.stringify(formData))
      .replace('{website_title}', websiteData.title)
      .replace('{website_content}', websiteData.content);

    // Call LLM
    const completion = await openai.chat.completions.create({
      model: process.env.LLM_MODEL || 'mistral-large-latest',
      messages: [
        { role: 'system', content: 'You are an EU AI Act compliance expert.' },
        { role: 'user', content: prompt }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.3,
    });

    const result = JSON.parse(completion.choices[0].message.content);
    
    // Vectorize for search
    await pinecone.upsertVectors([
      {
        id: `check-${Date.now()}`,
        values: await embed(JSON.stringify(result)),
        metadata: {
          url,
          score: result.score,
          risk_level: result.risk_level,
        }
      }
    ]);

    return result;
  } catch (e) {
    console.error('AI Engine analysis failed:', e);
    throw e;
  }
}

// Helper: Fetch website content
async function fetchWebsiteData(url) {
  try {
    const resp = await fetch(url);
    const html = await resp.text();
    
    // Extract title and body text (simplified)
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const bodyText = html.replace(/<script[^>]*>.*?<\/script>/gs, '').replace(/<style[^>]*>.*?<\/style>/gs, '').replace(/<[^>]+>/g, ' ').substring(0, 10000);
    
    return {
      title: titleMatch ? titleMatch[1].trim() : url,
      content: bodyText,
    };
  } catch (e) {
    console.error('Failed to fetch website:', e);
    return { title: url, content: '' };
  }
}

// Helper: Embedding (simplified)
async function embed(text) {
  // In production: Use OpenAI embeddings or Mistral embeddings
  // This is a placeholder for demo
  return new Array(768).fill(0.0).map(() => Math.random() * 2 - 1);
}

// Export for Lambda/Cloud Functions
export async function handler(event) {
  try {
    const { url, formData } = JSON.parse(event.body);
    const result = await analyzeCompliance(url, formData);
    return {
      statusCode: 200,
      body: JSON.stringify({ success: true, data: result }),
    };
  } catch (e) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Analysis failed', details: e.message }),
    };
  }
}

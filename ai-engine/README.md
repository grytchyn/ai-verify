# AI-Verify AI Engine — LLM Inference Service

## Tech Stack

- **LLM**: OpenAI-compatible (Mistral, Llama, etc.)
- **VectorDB**: Pinecone
- **Framework**: Express.js
- **Languages**: TypeScript + Node.js

## Development

```bash
npm install
npm run dev
```

## Environment Variables

```bash
PORT=3002
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
LLM_MODEL=mistral-large-latest
```

## API Endpoints

- `GET /health` — Health check
- `POST /analyze` — Analyze compliance

## AI Prompts

See `src/prompts/` for prompt templates.

## Deployment

```bash
npm run build
npm start
```

Docker:

```bash
docker build -t ai-verify-ai-engine:latest . && docker run -p 3002:3002 ai-verify-ai-engine
```

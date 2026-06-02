# AI-Verify Backend — Node.js + Express API

## Tech Stack

- **Framework**: Express.js
- **Database**: PostgreSQL (Sharded)
- **Validation**: Zod
- **Auth**: JWT (HS256)

## Development

```bash
npm install
npm run dev
```

## Environment Variables

Create `.env` from `.env.example`:

```bash
PORT=3001
NODE_ENV=development

DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_verify
DB_USER=postgres
DB_PASSWORD=your-password

AI_ENGINE_URL=http://localhost:3002
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_test_...
PINECONE_API_KEY=your-key
JWT_SECRET=super-secret-key
```

## API Endpoints

### Public
- `GET /api/v1/compliance/health` — Health check
- `POST /api/v1/compliance/analyze` — Start compliance check
- `GET /api/v1/compliance/checks/:id` — Get report

### Protected (JWT required)
- `GET /api/v1/organizations/:id` — Org details
- `PUT /api/v1/organizations/:id` — Update org
- `POST /api/v1/auth/login` — Login
- `POST /api/v1/auth/register` — Register

### Webhooks
- `POST /api/v1/webhooks/stripe` — Stripe events
- `POST /api/v1/webhooks/regulation` — AI Act updates

## Database Schema

See `infrastructure/data/schema.sql` for complete schema.

## Deployment

```bash
npm run build
npm start
```

Or use Docker:

```bash
docker build -t ai-verify-backend:latest . && docker run -p 3001:3001 ai-verify-backend
```

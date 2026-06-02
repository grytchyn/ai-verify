# AI-Verify Frontend — Next.js 14

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + `styled-components`
- **State**: Zustand + React Query
- **Animations**: Framer Motion

## Development

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run start
```

## File Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (public)/           # Public pages (SEO)
│   ├── (auth)/             # Auth flows
│   └── (app)/              # Protected user app
├── components/             # Reusable components
│   └── forms/              # AI compliance forms
├── hooks/                  # Custom React hooks
├── lib/                    # Utilities
├── public/                 # Static assets
└── styles/                 # Global CSS
```

## Environment Variables

Create `.env.local` from `.env.local.example`:

```
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_APP_NAME="AI Verify"
```

## Deployment

- **Vercel**: `VERCEL_TOKEN` + GitHub repo link
- **Self-hosted**: Docker build + Nginx reverse proxy

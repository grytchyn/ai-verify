# AI-Verify AI Engine — Dockerfile for Production
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source
COPY . .

# Expose port
EXPOSE 3002

# Start server
CMD ["node", "dist/index.js"]

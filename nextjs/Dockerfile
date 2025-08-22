# ---- Build stage ----
FROM node:20-alpine AS builder

WORKDIR /nextjs

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

# Build Next.js
RUN npm run build

# ---- Run stage ----
FROM node:20-alpine

WORKDIR /nextjs

# Copy build artifacts + dependencies
COPY --from=builder /nextjs/.next ./.next
COPY --from=builder /nextjs/node_modules ./node_modules
COPY --from=builder /nextjs/package*.json ./
# COPY --from=builder /nextjs/public ./public

# Cloud Run requires listening on $PORT
EXPOSE 8080

CMD ["sh", "-c", "npm run start -- -p $PORT -H 0.0.0.0"]


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

# Copy only build artifacts + dependencies
COPY --from=builder /nextjs/.next ./.next
COPY --from=builder /nextjs/node_modules ./node_modules
COPY --from=builder /nextjs/package*.json ./

# Expose port 3000
EXPOSE 3000

# Start Next.js server
CMD ["npm", "start"]

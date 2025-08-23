
---

## **Frontend README (`README_FRONTEND.md`)**

```markdown
# ADK Frontend (Next.js)

Modern frontend to interact with a Google ADK backend or Vertex AI Agent Engine via streaming responses.

## Features

- Chat UI with message list and incremental streaming
- Activity timeline for plan visualization
- Automatic environment detection (local backend, Cloud Run, or Agent Engine)
- SSE streaming handlers for both local backend and Agent Engine

## Tech Stack

- Next.js 15 + React 19
- TailwindCSS
- shadcn/ui for UI components
- Node.js 18+
- ESLint & Jest for linting and testing

## Project Structure

nextjs/
src/app/api/health # Proxies backend health checks
src/app/api/run_sse # Streaming endpoint
src/lib/config.ts # Env detection + endpoint resolution
src/lib/handlers/ # Streaming handlers (local/agent-engine)
src/components/chat/ # Chat UI components 


---

## Setup & Run (Local)

### Prerequisites

- Node.js 18+
- Local backend running (`make dev-backend`)

### Install & Run

```bash
npm --prefix nextjs install
npm --prefix nextjs run dev

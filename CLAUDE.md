# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Veritas is an Agent Constitution Protocol — a defense-in-depth system that protects AI agents from memory loss and behavioral compromise. Built for the PL Genesis Hackathon 2026 by Dawn Kelly (human) and Trinity (AI agent). The project provides cryptographic proof of agent integrity using Lit Protocol, Storacha, and Filecoin.

## Build & Development Commands

### Frontend (React + Vite)
```bash
cd frontend
npm install          # Install dependencies
npm run dev          # Dev server on port 5173
npm run build        # Production build
npm run lint         # ESLint (strict, zero warnings allowed)
```

### Backend (FastAPI + Uvicorn)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The Vite dev server proxies `/api/*` requests to the backend at port 8000.

## Architecture

### 4-Layer Defense System

- **Layer 0 — Bootstrap Discovery** (`/api/bootstrap`): Locates agent memory/context before anything else runs. Checks primary locations (Obsidian vault, workspace), falls back to backups, and self-reports gaps.
- **Layer 1 — Constitution Anchor** (`/api/integrity`): Immutable storage of agent ethics via Storacha + Filecoin anchoring. CIDs verified against on-chain hashes. Lit Protocol handles threshold cryptography.
- **Layer 2 — Guardian**: Real-time prompt injection detection. Pattern-based + semantic scoring. Confidence >0.8 blocks, 0.5–0.8 alerts, <0.5 passes.
- **Layer 3 — Internal Validator**: Pre-action verification against constitution. Hard constraints (YAML) + soft principles (embeddings). Violations logged to Filecoin.

### Frontend Structure
Two dashboard pages routed via React Router:
- **TrinityStatus** (`/status`): Agent health — bootstrap status, memory continuity, active projects, alerts, memory timeline
- **VeritasIntegrity** (`/integrity`): Security — constitution CID/anchoring, Guardian logs, Validator logs, infrastructure status

Reusable components: `StatusCard`, `MemoryTimeline`, `ConstitutionViewer`, `GuardianLog`, `ValidatorLog`

### Backend Structure
FastAPI with routers organized by domain:
- `api/bootstrap.py` — Layer 0 endpoints
- `api/status.py` — Trinity dashboard data
- `api/integrity.py` — Veritas security data

All response models are Pydantic. Currently returning mock data — pages have commented-out fetch calls ready for real integration.

## Conventions

- **Frontend naming**: PascalCase components (`StatusCard.jsx`), kebab-case CSS classes (`.status-card`), CSS variables (`--bg-primary`)
- **Backend naming**: snake_case endpoints and Python conventions
- **Styling**: Dark theme design system defined as CSS custom properties in `App.css`. Each page has its own CSS file.
- **ESLint**: Strict mode — zero warnings allowed (`--max-warnings 0`)
- **No TypeScript**: Frontend uses JSX (not TSX), though React type packages are installed
- **Commit style**: Descriptive subjects with bullet-point details

## Key Integration Points

The agent constitution lives at `docs/constitution.md`. The frontend and backend both have mock data structures that exactly mirror the API response models — connecting them is a matter of uncommenting the fetch calls in page components and wiring up real data sources in the backend routers.

Sponsor tech stack: **Lit Protocol** (threshold crypto, non-custodial keys), **Storacha** (UCAN-based storage), **Filecoin** (on-chain anchoring).

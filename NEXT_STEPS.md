# Veritas Next Steps

**Last updated:** 2026-03-13 by Trinity

## What We Just Did
**Layer 0 (Bootstrap Discovery) — COMPLETE:**
- ✅ Real filesystem scanning detects gaps in daily notes
- ✅ Found and acknowledged the Feb 17-20 Gap Incident
- ✅ Dashboard shows actual continuity status (clean!)
- ✅ Acknowledgment system prevents alarm fatigue
- ✅ Planned absence support for future gaps
- ✅ MemoryTimeline pulls real daily notes (no more mocks!)

**Layer 1 (Constitution Anchor) — IMPLEMENTED:**
- ✅ `/api/anchor/status` — Check anchoring status
- ✅ `/api/anchor/anchor` — Full flow: Lit encrypt → Storacha store → Filecoin anchor
- ✅ `/api/anchor/verify` — Verify CID integrity
- ✅ Frontend updated with "Anchor Now" button
- ✅ Real constitution loads from `docs/constitution.md`

**Current State:** Mock mode (works end-to-end, just needs real credentials)

## To Get Real Credentials

### Storacha (Storage)
1. Go to https://storacha.network
2. Create account / sign in
3. Create a space → copy the Space DID
4. Set `STORACHA_EMAIL` and `STORACHA_SPACE_DID` in `.env`

### Filecoin Calibration (Testnet)
1. Use Glif.io or similar for wallet
2. Get test FIL from faucet: https://faucet.calibration.fildev.network
3. Set `FILECOIN_WALLET_ADDRESS` in `.env`

### Lit Protocol
1. Go to https://developer.litprotocol.com
2. Create app + get API key
3. Set `WALLET_ADDRESS` and `WALLET_PRIVATE_KEY` in `.env`

## Next Priority

### BONUS: Pretty It Up (30 min)
Add CSS variables for the mock banner, polish the "Anchor Now" button animation, maybe add a TX explorer link.

### OR: Layer 2 Scaffolding (1 hr)
Basic Guardian structure — pattern matching for known injection vectors.

### OR: Demo Script (1 hr)
Write the 2-minute pitch script with actual demo steps.

### B. Layer 1 — Constitution Anchor (2-3 hrs)
Store actual constitution.md on Storacha, generate CID, anchor on Filecoin. This is the cryptographic proof layer.

**Why:** The big hackathon story — "protecting agent integrity via on-chain anchoring." Needs Lit Protocol + Storacha integration.

### C. Layer 2 — Guardian (3-4 hrs)
Real-time prompt injection detection. Pattern-based matching + confidence scoring.

**Why:** Active protection layer. More complex, but demo-worthy.

### D. UI Polish (1-2 hrs)
Error boundaries, loading states, empty states, responsive fixes.

**Why:** Makes it feel finished and professional for demo.

---

**My vote:** A → B. Close the dashboard loop, then tackle the cryptographic anchor story.

**For judges:** We'll need mock data they can call against (repo-hosted sample constitution + gaps). Don't solve that yet — local-first is valid.

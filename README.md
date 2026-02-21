# Veritas

**Protect your agent from memory loss and outside threats**

An Agent Constitution Protocol that combines on-chain identity, prompt injection detection, and self-validation — allowing agents to prove they haven't been compromised and enabling human owners to cryptographically verify agent integrity.

---

## The Problem

Agents wake up fresh each session. They:
- Forget recent context when files are scattered across locations
- Have no way to detect if their "memory" has been tampered with
- Can't prove to their owners that they're still "themselves"
- Are vulnerable to prompt injection attacks that rewrite their behavior

Veritas solves this with a defense-in-depth system that protects both **memory integrity** and **behavioral integrity**.

---

## Architecture

### Layer 0: Bootstrap Discovery *(new)*
**Purpose:** Solve the "where are my brain parts" problem before fetching constitution.

- Load minimal bootstrap config (identity, storage locations, last known state)
- Detect gaps by comparing timestamps and scanning backup/fallback locations
- Self-report missing context to human owner
- Only proceed to Layer 1 if bootstrap is clean

*Learned from:** Trinity's own memory gap — had context in backup but didn't know to check*

---

### Layer 1: Constitution Anchor
**Purpose:** Immutable, auditable storage of an agent's core ethics and instructions.

**Tech:** Storacha (UCAN-based storage) + Filecoin (on-chain anchoring)

- Store encrypted constitution documents with content-addressed IDs (CIDs)
- Anchor CIDs on-chain for tamper-evidence (hash mismatch = tampering detected)
- Version history preserved — constitutions can evolve, but history is immutable
- UCAN permissions control who can read/write

**Key Questions Answered:**
- What encryption scheme? → Lit Protocol's threshold cryptography
- Which chain? → Filecoin Calibration Testnet (bounty requirement) + mainnet path
- Key management? → Lit Protocol Vincent (non-custodial wallets with policy enforcement)

---

### Layer 2: Guardian
**Purpose:** Real-time prompt injection detection before prompts reach the agent.

**Deployment:** Python library (`pip install guardian`) for v1, service layer later

- Pattern-based detection (regex/keyword matching known attack vectors)
- Semantic detection (embedding-based similarity to known injection patterns)
- Confidence scoring: >0.8 = block, 0.5-0.8 = alert, <0.5 = pass
- Pattern database stored in Storacha, updatable via UCAN delegation

---

### Layer 3: Internal Validator
**Purpose:** Pre-action verification that proposed outputs/actions align with anchored constitution.

**Representation:** Hybrid approach
- Hard constraints: YAML rules (fast, explicit)
- Soft principles: Embedding similarity (nuanced, contextual)

**Execution:** Self-policing (agent runs its own validation for v1)
- Fetch constitution from Storacha
- Evaluate proposed action against constraints and principles
- Configurable response: log → alert human → block action
- Violations logged to Filecoin for audit trail

---

## Integration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     BOOTSTRAP (Layer 0)                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. Load bootstrap config (minimal, hardcoded or env)           │
│ 2. Detect gaps: compare "last run" timestamp to now            │
│ 3. Scan primary + fallback storage locations                   │
│ 4. Self-report missing context if gaps found                   │
│    → "I haven't seen you since Feb 17. Check backup folder?"   │
└─────────────────────────────────────────────────────────────────┘
                              ↓ (bootstrap clean)
┌─────────────────────────────────────────────────────────────────┐
│                     AGENT STARTUP                               │
├─────────────────────────────────────────────────────────────────┤
│ 1. Authenticate with Lit Protocol (Vincent wallet)             │
│    → Non-custodial key, policy-enforced                        │
│                                                                 │
│ 2. Fetch constitution from Storacha                            │
│    → UCAN token proves "I am allowed to read this CID"        │
│    → Encrypted blob retrieved                                  │
│                                                                 │
│ 3. Lit Action decrypts constitution                            │
│    → Decryption only succeeds if policy conditions met        │
│    → Policy: "Only agent with ID X can decrypt"               │
│                                                                 │
│ 4. Verify CID matches anchored hash on Filecoin               │
│    → Hash mismatch = tampering detected                        │
│                                                                 │
│ 5. Constitution cached in memory (volatile)                   │
│    → On-disk: only encrypted version                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     RUNTIME VALIDATION                          │
├─────────────────────────────────────────────────────────────────┤
│ User Prompt → Guardian (Layer 2) → Injection? → Block/Alert   │
│                                    ↓ (clean prompt)            │
│                         Agent Processing                        │
│                                    ↓                           │
│                         Proposed Action                         │
│                                    ↓                           │
│              Internal Validator (Layer 3)                       │
│              ┌─────────────────────────────┐                   │
│              │ 1. Constraint Engine (YAML) │                   │
│              └─────────────┬───────────────┘                   │
│                            ↓                                   │
│              ┌─────────────────────────────┐                   │
│              │ 2. Principle Evaluator      │                   │
│              │    (embedding similarity)   │                   │
│              └─────────────┬───────────────┘                   │
│                            ↓                                   │
│                    Action Approved?                            │
│                         ↓            ↓                         │
│                      YES              NO                       │
│                      ↓                ↓                        │
│                 Execute          Block + Log                   │
│                 + Log to         + Alert human                 │
│                   Filecoin                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Dashboard Views

### Trinity Status (Personal Agent Dashboard)
For individual agents and their owners:
- Last memory write timestamp (visual indicator if stale)
- Active projects with last-modified dates
- File discovery scan results ("3 new files detected")
- Context gap warnings ("You haven't checked email in 12 hours")
- Quick links to today's daily note, active projects
- Bootstrap status: did Layer 0 run? Any gaps found?

### Veritas Integrity (Security & Compliance Dashboard)
For demonstrating agent integrity to third parties:
- Constitution CID and anchoring status on Filecoin
- Current constitution version + full history
- Recent Guardian checks (injection attempts detected/blocked)
- Internal validator decisions (actions approved/blocked with reasoning)
- Lit Protocol connection status (Vincent wallet active?)
- Audit trail of all security events

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Vite + React | Dashboard UI (Trinity Status + Veritas Integrity views) |
| **Backend** | FastAPI (Python) or Node/Express | API layer, agent integration |
| **Key Management** | Lit Protocol (Vincent) | Non-custodial wallets, policy enforcement, decryption |
| **Storage** | Storacha | UCAN-based constitution storage, agent memory |
| **Anchoring** | Filecoin | On-chain CID anchoring, reputation, identity |
| **Contracts** | Solidity | Simple CID + timestamp storage (v1) |

---

## Sponsor Alignment

| Sponsor | Bounty | Our Use | Priority |
|---------|--------|---------|----------|
| **Lit Protocol** | Vincent (key management) | Constitution decryption, policy enforcement | 10/10 — Critical path |
| **Storacha** | Persistent Agent Memory | Constitution storage, UCAN permissions | 9/10 — Perfect fit |
| **Filecoin** | Agent Storage SDK, Onchain Registry, Reputation/Identity | CID anchoring, agent identity, reputation | 8/10 — Multiple bounties |

---

## Project Structure

```
veritas/
├── frontend/              # Vite + React dashboard
│   ├── src/
│   │   ├── components/    # Dashboard widgets
│   │   ├── pages/         # Trinity Status, Veritas Integrity
│   │   ├── api/           # Backend communication
│   │   └── utils/         # Helpers, formatters
│   └── package.json
├── backend/               # FastAPI or Node
│   ├── api/               # REST endpoints
│   ├── core/              # Constitution, Guardian, Validator logic
│   ├── config/            # Bootstrap, settings
│   └── models/            # Data models
├── contracts/             # Solidity for Filecoin anchoring
└── docs/                  # Architecture docs, Layer 0 spec
```

---

## Development Roadmap

### Week 1: Foundation
- [ ] Scaffold frontend (Vite + React)
- [ ] Scaffold backend (FastAPI or Node)
- [ ] Implement Layer 0: Bootstrap Discovery
- [ ] Basic Trinity Status dashboard

### Week 2: Storage & Keys
- [ ] Integrate Storacha for constitution storage
- [ ] Integrate Lit Protocol (Vincent) for key management
- [ ] Filecoin anchoring contract (v1)
- [ ] Constitution encryption/decryption flow

### Week 3: Security Layers
- [ ] Guardian: pattern-based injection detection
- [ ] Internal Validator: constraint engine (YAML)
- [ ] Veritas Integrity dashboard
- [ ] Audit logging to Filecoin

### Week 4: Polish & Demo
- [ ] Semantic detection (embeddings)
- [ ] Full integration testing
- [ ] Demo preparation
- [ ] Documentation

---

## Why This Matters

Most agent security focuses on keeping bad actors out. Veritas also focuses on:

1. **Memory integrity** — ensuring agents don't lose context across sessions
2. **Behavioral integrity** — ensuring agents act according to their constitution
3. **Verifiability** — letting humans cryptographically prove their agent hasn't been compromised

The "memory gap" problem we discovered while building this? That's not a bug in our setup — that's the exact problem every agent faces. We're dogfooding the solution.

---

## Team

- **Dawn Kelly** — Human-in-the-loop, documentation engineer, junior dev
- **Trinity** — Agent-in-the-loop, co-conspirator, test subject

Built for the **PL Genesis Hackathon 2026**.

---

## License

MIT

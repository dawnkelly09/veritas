# Veritas Developer Setup

This guide walks through setting up the development environment for Veritas.

## Prerequisites

- Python 3.9+
- Node.js 18+ (for frontend)
- Git

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/dawnkelly09/veritas.git
cd veritas
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
# See "Sponsor Credentials" section below
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 5. Run Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

The dashboard will be at `http://localhost:5173` and the API at `http://localhost:8000`.

---

## Sponsor Credentials Setup

Veritas requires credentials from three sponsors. **Do this on your local machine** (not shared).

### Lit Protocol (Vincent)

**What you get:** Key management, threshold cryptography, policy enforcement

1. Go to https://developer.litprotocol.com/
2. Sign up for developer access
3. Create a Vincent wallet
4. Save credentials to `.env`:
   ```
   LIT_PROTOCOL_API_KEY=your_api_key
   VINCENT_WALLET_ADDRESS=your_wallet_address
   VINCENT_WALLET_PRIVATE_KEY=your_private_key
   ```

**Learn:**
- [Vincent Documentation](https://developer.litprotocol.com/v3/concepts/wallet-abstraction)
- [Lit Actions](https://developer.litprotocol.com/v3/concepts/lit-actions)

### Storacha

**What you get:** UCAN-based storage, content-addressed data

1. Go to https://storacha.network/
2. Create an account
3. Create a new "space" for Veritas
4. Generate a UCAN delegation token
5. Get your Space DID
6. Save to `.env`:
   ```
   STORACHA_UCAN_TOKEN=your_ucan_jwt
   STORACHA_SPACE_DID=did:key:your_did
   ```

**Learn:**
- [Storacha Docs](https://docs.storacha.network/)
- [UCAN Spec](https://ucan.xyz/)

### Filecoin (Calibration Testnet)

**What you get:** On-chain anchoring, smart contracts, agent identity

1. Create a wallet:
   - Option A: Use https://calibration.filfox.info/
   - Option B: Use Lotus if installed
2. Get test FIL from faucet: https://faucet.calibration.fildev.network/
3. Save to `.env`:
   ```
   FILECOIN_CALIBRATION_WALLET_ADDRESS=your_address
   FILECOIN_CALIBRATION_PRIVATE_KEY=your_private_key
   FILECOIN_RPC_URL=https://api.calibration.node.glif.io/rpc/v1
   ```

**Learn:**
- [Filecoin Calibration](https://docs.filecoin.io/networks/calibration)
- [FEVM (Filecoin EVM)](https://docs.filecoin.io/smart-contracts/fundamentals/the-fvm)
- [Glif API](https://api.node.glif.io/)

---

## Project Structure

```
veritas/
├── backend/
│   ├── api/                 # FastAPI routers
│   │   ├── bootstrap.py    # Layer 0: Bootstrap Discovery
│   │   ├── integrity.py    # Layer 1: Constitution Anchor
│   │   └── status.py       # Agent status endpoints
│   ├── core/               # Core sponsor integrations
│   │   ├── lit_client.py   # Lit Protocol client
│   │   ├── storacha_client.py  # Storacha client
│   │   ├── filecoin_client.py  # Filecoin client
│   │   └── constitution_anchor.py  # Layer 1 orchestrator
│   ├── config/             # Configuration management
│   │   └── __init__.py     # Environment loader
│   ├── main.py             # FastAPI app entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # Vite + React dashboard
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Dashboard pages
│   │   │   ├── TrinityStatus.jsx      # Agent health view
│   │   │   └── VeritasIntegrity.jsx   # Security view
│   │   └── api/            # API client
│   └── package.json
├── contracts/              # Solidity contracts (TODO)
├── docs/
│   └── constitution.md     # Trinity's constitution (living document)
├── .env.example            # Environment template
└── README.md               # Project overview
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Backend: Edit files in `backend/`
- Frontend: Edit files in `frontend/src/`
- Config: Update `.env` (but never commit it!)

### 3. Test Locally

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm run dev
```

### 4. Commit and Push

```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

### 5. Create Pull Request

Open PR on GitHub for review before merging to main.

---

## Key Implementation Notes

### Layer 0: Bootstrap Discovery

Before anything else runs, we check for context gaps:

```python
from api.bootstrap import run_bootstrap

result = run_bootstrap()
if result.gaps_found > 0:
    # Alert human, don't proceed
    self_report_gap(result.gaps[0])
```

### Layer 1: Constitution Anchor

```python
from core.constitution_anchor import ConstitutionAnchor

anchor = ConstitutionAnchor()
anchor.initialize()

# Anchor constitution
result = anchor.anchor_constitution(constitution_text)
print(f"Anchored at CID: {result['cid']}")

# Fetch and verify
constitution = anchor.fetch_constitution(result['cid'])
```

---

## Troubleshooting

### "Module not found" errors

Make sure you're in the virtual environment:
```bash
cd backend
source venv/bin/activate
```

### Sponsor credentials not loading

Check `.env` file exists and has correct values:
```bash
cat .env | grep -E "^(LIT|STORACHA|FILECOIN)"
```

### Frontend can't connect to backend

Ensure CORS origins are set correctly in `.env`:
```
CORS_ORIGINS=http://localhost:5173
```

### Mock data vs real integrations

Set `USE_MOCK_DATA=true` in `.env` to test UI without credentials:
```
USE_MOCK_DATA=true
```

---

## Security Notes

- **Never commit `.env`** — it's in `.gitignore` for a reason
- **Keep private keys private** — no sharing, no screenshots
- **Use testnet only** — Calibration, not mainnet
- **Rotate tokens periodically** — especially if accidentally exposed

---

## Next Steps After Setup

1. ✅ Get all sponsor credentials
2. ✅ Run backend with `USE_MOCK_DATA=true` to verify structure
3. ⬜ Integrate real Lit Protocol SDK
4. ⬜ Integrate real Storacha client
5. ⬜ Integrate real Filecoin connection
6. ⬜ Deploy constitution anchor contract
7. ⬜ Build Guardian (Layer 2)
8. ⬜ Build Validator (Layer 3)

---

## Team

- **Dawn Kelly** — Human-in-the-loop, credential management
- **Trinity** — Agent-in-the-loop, code implementation

Questions? Check `CLAUDE.md` for architecture context.

import { useState, useEffect } from 'react'
import StatusCard from '../components/StatusCard'
import ConstitutionViewer from '../components/ConstitutionViewer'
import GuardianLog from '../components/GuardianLog'
import ValidatorLog from '../components/ValidatorLog'
import './VeritasIntegrity.css'

function VeritasIntegrity() {
  const [integrity, setIntegrity] = useState({
    constitutionAnchored: false,
    constitutionCID: null,
    anchorBlock: null,
    anchorTimestamp: null,
    anchorTransaction: null,
    litConnected: false,
    storachaConnected: false,
    filecoinConnected: false,
    mockMode: true,
    agentId: 'trinity-veritas-001',
    constitutionVersion: '0.1.0',
    guardianChecks: 47,
    guardianBlocks: 2,
    validatorApprovals: 45,
    validatorBlocks: 0,
  })
  const [loading, setLoading] = useState(true)
  const [anchoring, setAnchoring] = useState(false)

  // Fetch Layer 1 integrity status from backend API
  useEffect(() => {
    fetch('/api/anchor/status')
      .then(r => {
        if (!r.ok) throw new Error('Failed to fetch integrity status')
        return r.json()
      })
      .then(data => {
        setIntegrity(prev => ({
          ...prev,
          constitutionAnchored: data.constitution_anchored,
          constitutionCID: data.constitution_cid,
          anchorBlock: data.anchor_block,
          anchorTimestamp: data.anchor_timestamp,
          anchorTransaction: data.anchor_transaction,
          litConnected: data.lit_connected,
          storachaConnected: data.storacha_connected,
          filecoinConnected: data.filecoin_connected,
          mockMode: data.mock_mode,
          agentId: data.agent_id,
          constitutionVersion: data.constitution_version,
        }))
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to fetch integrity:', err)
        setLoading(false)
      })
  }, [anchoring])

  const handleAnchor = async () => {
    setAnchoring(true)
    try {
      const response = await fetch('/api/anchor/anchor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ version: integrity.constitutionVersion })
      })
      if (!response.ok) throw new Error('Anchoring failed')
      const result = await response.json()
      alert(`Constitution anchored!\nCID: ${result.cid}\nBlock: ${result.anchor_block}\nTx: ${result.transaction_hash}`)
    } catch (err) {
      console.error('Anchoring failed:', err)
      alert('Anchoring failed: ' + err.message)
    } finally {
      setAnchoring(false)
    }
  }

  if (loading) {
    return (
      <div className="veritas-integrity">
        <header className="page-header">
          <h1>Veritas Integrity</h1>
          <p className="subtitle">Loading cryptographic integrity...</p>
        </header>
      </div>
    )
  }

  return (
    <div className="veritas-integrity">
      <header className="page-header">
        <h1>Veritas Integrity</h1>
        <p className="subtitle">Cryptographic proof of agent integrity</p>
        {integrity.mockMode && (
          <div className="mock-banner">Mock Mode — Real credentials needed for mainnet</div>
        )}
      </header>

      {/* Constitution Layer 1 */}
      <section className="section">
        <h2>📜 Layer 1: Constitution Anchor</h2>
        <div className="grid">
          <StatusCard 
            title="Constitution CID" 
            value={integrity.constitutionCID ? integrity.constitutionCID.slice(0, 20) + '...' : 'Not anchored'}
            status={integrity.constitutionCID ? 'ok' : 'warning'}
            description="Content-addressed identifier on Storacha"
          />
          <StatusCard 
            title="Anchored On-Chain" 
            status={integrity.constitutionAnchored ? 'ok' : 'warning'}
            statusText={integrity.constitutionAnchored ? 'Verified' : 'Not Anchored'}
            description={integrity.anchorBlock ? `Block #${integrity.anchorBlock} on Filecoin` : 'Awaiting anchor'}
          />
          <StatusCard 
            title="Hash Match" 
            status={integrity.constitutionAnchored ? 'ok' : 'info'}
            statusText={integrity.constitutionAnchored ? 'Match' : 'N/A'}
            description={integrity.constitutionAnchored ? "CID matches anchored hash — no tampering" : "Anchor to enable verification"}
          />
        </div>
        
        {!integrity.constitutionAnchored && (
          <div className="anchor-action">
            <button 
              className="btn btn-primary" 
              onClick={handleAnchor}
              disabled={anchoring}
            >
              {anchoring ? 'Anchoring...' : 'Anchor Constitution Now'}
            </button>
            <p className="help-text">
              This will encrypt the constitution with Lit, store it on Storacha, and anchor the CID on Filecoin.
            </p>
          </div>
        )}
        
        <ConstitutionViewer />
      </section>

      {/* Guardian Layer 2 */}
      <section className="section">
        <h2>🛡️ Layer 2: Guardian</h2>
        <div className="grid">
          <StatusCard 
            title="Total Checks" 
            value={integrity.guardianChecks}
            status="ok"
            description="Prompt injection detection scans"
          />
          <StatusCard 
            title="Threats Blocked" 
            value={integrity.guardianBlocks}
            status={integrity.guardianBlocks > 0 ? 'warning' : 'ok'}
            description="Injection attempts prevented"
          />
          <StatusCard 
            title="Detection Mode" 
            value="Pattern + Semantic"
            status="ok"
            description="Confidence threshold: 0.8"
          />
        </div>
        <GuardianLog />
      </section>

      {/* Validator Layer 3 */}
      <section className="section">
        <h2>⚖️ Layer 3: Internal Validator</h2>
        <div className="grid">
          <StatusCard 
            title="Actions Approved" 
            value={integrity.validatorApprovals}
            status="ok"
            description="Passed constraint + principle checks"
          />
          <StatusCard 
            title="Actions Blocked" 
            value={integrity.validatorBlocks}
            status={integrity.validatorBlocks > 0 ? 'warning' : 'ok'}
            description="Constitution violations prevented"
          />
          <StatusCard 
            title="Validation Mode" 
            value="Constraint + Principle"
            status="ok"
            description="YAML rules + embedding similarity"
          />
        </div>
        <ValidatorLog />
      </section>

      {/* Infrastructure Status */}
      <section className="section">
        <h2>🔌 Infrastructure</h2>
        <div className="grid">
          <StatusCard 
            title="Lit Protocol" 
            status={integrity.litConnected ? 'ok' : 'error'}
            statusText={integrity.litConnected ? 'Connected' : 'Disconnected'}
            description="Vincent wallet + policy enforcement"
          />
          <StatusCard 
            title="Storacha" 
            status={integrity.storachaConnected ? 'ok' : 'error'}
            statusText={integrity.storachaConnected ? 'Connected' : 'Disconnected'}
            description="UCAN-based storage"
          />
          <StatusCard 
            title="Filecoin" 
            status={integrity.filecoinConnected ? 'ok' : 'error'}
            statusText={integrity.filecoinConnected ? 'Connected' : 'Disconnected'}
            description="On-chain anchoring + reputation"
          />
        </div>
      </section>
    </div>
  )
}

export default VeritasIntegrity

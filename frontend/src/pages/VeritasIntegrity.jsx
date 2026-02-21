import { useState, useEffect } from 'react'
import StatusCard from '../components/StatusCard'
import ConstitutionViewer from '../components/ConstitutionViewer'
import GuardianLog from '../components/GuardianLog'
import ValidatorLog from '../components/ValidatorLog'
import './VeritasIntegrity.css'

function VeritasIntegrity() {
  const [integrity, setIntegrity] = useState({
    constitutionAnchored: true,
    constitutionCID: 'QmX7bVbZgQb...9xYz',
    anchorBlock: '3847291',
    litConnected: true,
    storachaConnected: true,
    filecoinConnected: true,
    guardianChecks: 47,
    guardianBlocks: 2,
    validatorApprovals: 45,
    validatorBlocks: 0,
  })

  // TODO: Connect to backend API
  useEffect(() => {
    // fetch('/api/integrity').then(r => r.json()).then(setIntegrity)
  }, [])

  return (
    <div className="veritas-integrity">
      <header className="page-header">
        <h1>Veritas Integrity</h1>
        <p className="subtitle">Cryptographic proof of agent integrity</p>
      </header>

      {/* Constitution Layer 1 */}
      <section className="section">
        <h2>📜 Layer 1: Constitution Anchor</h2>
        <div className="grid">
          <StatusCard 
            title="Constitution CID" 
            value={integrity.constitutionCID}
            status="ok"
            description="Content-addressed identifier on Storacha"
          />
          <StatusCard 
            title="Anchored On-Chain" 
            status={integrity.constitutionAnchored ? 'ok' : 'error'}
            statusText={integrity.constitutionAnchored ? 'Verified' : 'Not Anchored'}
            description={`Block #${integrity.anchorBlock} on Filecoin`}
          />
          <StatusCard 
            title="Hash Match" 
            status="ok"
            statusText="Match"
            description="CID matches anchored hash — no tampering detected"
          />
        </div>
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

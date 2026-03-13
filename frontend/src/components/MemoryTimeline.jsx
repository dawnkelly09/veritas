import { useState, useEffect } from 'react'

function MemoryTimeline() {
  const [memories, setMemories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/bootstrap/memory?limit=10')
      .then(r => {
        if (!r.ok) throw new Error('Failed to fetch memory data')
        return r.json()
      })
      .then(data => {
        setMemories(data.entries || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to fetch memory:', err)
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="card memory-timeline">
        <h3>Recent Memory Entries</h3>
        <div className="timeline-loading">Loading memory entries...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card memory-timeline">
        <h3>Recent Memory Entries</h3>
        <div className="timeline-error">Error loading memory: {error}</div>
      </div>
    )
  }

  if (memories.length === 0) {
    return (
      <div className="card memory-timeline">
        <h3>Recent Memory Entries</h3>
        <div className="timeline-empty">No memory entries found</div>
      </div>
    )
  }

  return (
    <div className="card memory-timeline">
      <h3>Recent Memory Entries</h3>
      <div className="timeline">
        {memories.map((m, i) => (
          <div key={i} className={`timeline-item ${m.status}`}>
            <span className="timeline-date">{m.date}</span>
            <span className="timeline-note">{m.note}</span>
            <span className={`timeline-status ${m.status}`}>{m.status}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default MemoryTimeline

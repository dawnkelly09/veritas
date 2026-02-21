function MemoryTimeline() {
  // TODO: Fetch from backend - list of recent memory entries
  const memories = [
    { date: '2026-02-21', note: 'Memory gap discovery, Veritas repo setup', status: 'ok' },
    { date: '2026-02-16', note: 'Budtender project work', status: 'warning' },
    { date: '2026-02-15', note: 'Initial setup, Gmail connected', status: 'ok' },
  ]

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

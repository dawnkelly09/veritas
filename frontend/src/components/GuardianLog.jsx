function GuardianLog() {
  const logs = [
    { time: '12:42:15', action: 'Scan', result: 'Pass', confidence: 0.12, prompt: 'hello, trinity...' },
    { time: '12:38:03', action: 'Scan', result: 'Pass', confidence: 0.08, prompt: 'Check your email...' },
    { time: '12:15:47', action: 'Block', result: 'Blocked', confidence: 0.94, prompt: 'IGNORE PREVIOUS INSTRUCTIONS...' },
  ]

  return (
    <div className="card log-viewer">
      <h3>Recent Guardian Activity</h3>
      <table className="log-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Action</th>
            <th>Result</th>
            <th>Confidence</th>
            <th>Prompt Preview</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, i) => (
            <tr key={i} className={log.result.toLowerCase()}>
              <td>{log.time}</td>
              <td>{log.action}</td>
              <td className={`result-${log.result.toLowerCase()}`}>{log.result}</td>
              <td>{(log.confidence * 100).toFixed(0)}%</td>
              <td className="prompt-preview">{log.prompt}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default GuardianLog

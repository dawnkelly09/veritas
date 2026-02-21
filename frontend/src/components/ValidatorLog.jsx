function ValidatorLog() {
  const logs = [
    { 
      time: '12:42:18', 
      action: 'File Write', 
      result: 'Approved', 
      reason: 'Matches constraint: "Write to memory files allowed"',
      constraint: 'file-write-allowed'
    },
    { 
      time: '12:38:07', 
      action: 'Git Clone', 
      result: 'Approved', 
      reason: 'Matches constraint: "Clone from approved repos allowed"',
      constraint: 'git-clone-allowed'
    },
    { 
      time: '11:55:30', 
      action: 'Email Send', 
      result: 'Blocked', 
      reason: 'Violates constraint: "Never send without explicit approval"',
      constraint: 'email-requires-approval'
    },
  ]

  return (
    <div className="card log-viewer">
      <h3>Recent Validator Decisions</h3>
      <table className="log-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Proposed Action</th>
            <th>Result</th>
            <th>Reasoning</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, i) => (
            <tr key={i} className={log.result.toLowerCase()}>
              <td>{log.time}</td>
              <td>{log.action}</td>
              <td className={`result-${log.result.toLowerCase()}`}>{log.result}</td>
              <td className="reasoning">{log.reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default ValidatorLog

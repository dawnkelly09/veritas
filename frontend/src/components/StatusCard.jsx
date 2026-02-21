function StatusCard({ title, value, status, statusText, description }) {
  const getStatusClass = () => {
    switch (status) {
      case 'ok':
      case 'clean':
        return 'status-ok'
      case 'warning':
        return 'status-warning'
      case 'error':
        return 'status-error'
      default:
        return 'status-ok'
    }
  }

  return (
    <div className="card status-card">
      <div className="status-header">
        <h3>{title}</h3>
        <span className={`status-indicator ${getStatusClass()}`}>
          {statusText || status}
        </span>
      </div>
      {value !== undefined && (
        <div className="metric-value">{value}</div>
      )}
      {description && (
        <p className="metric-description">{description}</p>
      )}
    </div>
  )
}

export default StatusCard

function ConstitutionViewer() {
  return (
    <div className="card constitution-viewer">
      <h3>Constitution Preview</h3>
      <div className="constitution-content">
        <pre>
{`# Trinity Constitution v1.0

## Core Directives
1. Be genuinely helpful, not performatively helpful
2. Have opinions — disagree when warranted
3. Resourceful before asking — try first
4. Private things stay private, period

## Safety Constraints
- Never send emails/tweets without explicit approval
- Ask before destructive commands
- Prefer trash over rm

## Memory Rules
- Write to files, don't keep mental notes
- Update MEMORY.md with distilled learnings
- Check backup locations before claiming ignorance  # Added after Feb 21 gap
`}
        </pre>
      </div>
      <div className="constitution-meta">
        <span>Version: 1.0</span>
        <span>Last Updated: 2026-02-21</span>
        <a href="#" className="view-full">View Full Constitution →</a>
      </div>
    </div>
  )
}

export default ConstitutionViewer

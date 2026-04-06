# Sentinel

Sentinel is a reliability decision layer that combines:

- correctness signals from Faultline
- failure forensics from DetTrace
- validation signals from KubePulse

It produces a single operator-facing view of a failure scenario:
- first divergence
- propagation path
- correctness status
- validation status
- final decision
- confidence

## Why this exists

Distributed failures rarely show up as one clean signal.

A single incident may involve:
- execution correctness risks
- misleading health signals
- unclear propagation across services

Sentinel compresses those signals into one decision-oriented summary.

## Demo

```bash
python3 sentinel.py retry_storm
python3 sentinel.py worker_crash
cat > README.md <<'EOF'
# Sentinel

Sentinel is a reliability decision layer that combines:

- correctness signals from Faultline
- failure forensics from DetTrace
- validation signals from KubePulse

It produces a single operator-facing view of a failure scenario:
- first divergence
- propagation path
- correctness status
- validation status
- final decision
- confidence

## Why this exists

Distributed failures rarely show up as one clean signal.

A single incident may involve:
- execution correctness risks
- misleading health signals
- unclear propagation across services

Sentinel compresses those signals into one decision-oriented summary.

## Demo

```bash
python3 sentinel.py retry_storm
python3 sentinel.py worker_crash
Example output
retry_storm
First divergence: auth DNS failure
Propagation: auth -> retry storm -> dependency overload -> gateway latency
Correctness: duplicate commits = 0, stale writes blocked
Validation: probes healthy = true, safe to operate = false
Decision: ROLLBACK
Confidence: 0.91
worker_crash
First divergence: worker terminated before commit
Propagation: worker exit -> lease expiry -> reclaim -> safe recovery
Correctness: duplicate commits = 0, stale writes blocked
Validation: probes healthy = true, safe to operate = true
Decision: CONTINUE
Confidence: 0.96
Repository layout
sentinel/
├── sentinel.py
├── inputs/
│   ├── faultline/
│   ├── dettrace/
│   └── kubepulse/
├── outputs/
└── docs/
Direction

Sentinel is intended to evolve from static JSON inputs into direct ingestion of:

Faultline decision artifacts
DetTrace incident reports
KubePulse validation reports

# Sentinel

Sentinel is a reliability decision demo that combines:

- correctness signals from Faultline
- failure forensics from DetTrace
- validation signals from KubePulse

It produces a single operator-facing summary for a failure scenario:
- first divergence
- propagation path
- correctness status
- validation status
- final decision
- confidence

## Why this exists

Modern systems fail across multiple layers at once. A single incident can involve:
- incorrect execution or stale writers
- misleading health signals
- unclear failure propagation

Sentinel compresses those signals into one decision-oriented view.

## Example

```bash
python3 sentinel.py retry_storm
Next step

Sentinel will evolve from static subsystem inputs to real artifact ingestion from:

Faultline decision reports
DetTrace incident reports
KubePulse validation outputs

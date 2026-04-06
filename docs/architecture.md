# Sentinel Architecture

Sentinel is a thin decision layer over three subsystem outputs.

## Inputs

- Faultline: correctness and execution-integrity signals
- DetTrace: first divergence and causal propagation
- KubePulse: validation and safe-to-operate signals

## Flow

1. Load structured subsystem artifacts
2. Normalize key signals
3. Merge them into one scenario view
4. Produce a decision report for an operator

## Current scope

The current implementation reads structured JSON inputs and produces:
- terminal output
- a merged decision artifact

## Intended direction

Later versions should ingest real reports directly from the subsystem repositories rather than copied sample inputs.

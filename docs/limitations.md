# Limitations

Read this document before interpreting the simulation.

## What this lab does not do

- It does not exploit vulnerabilities or implement a real worm.
- It does not self-replicate or copy itself to other hosts.
- It does not perform lateral movement.
- It does not establish persistence.
- It does not implement stealth, anti-forensics, or rootkit behaviour.
- It does not perform privilege escalation.
- The simulator does not send network traffic or execute remote commands.

## What the simulation does

- Represents hosts as graph nodes.
- Represents possible relationships as graph edges.
- Models state transitions using a configurable probability.
- Uses a recorded, sanitized lab event to select an initial simulated node.
- Produces a timeline and aggregate summary.
- Supports repeatable experiments using a fixed random seed.

## Model assumptions

- The graph may assume full connectivity between selected targets.
- A uniform probability may be applied to every target.
- Infected nodes may remain infected for the duration of a run.
- Defender actions may be absent from the basic model.
- The initial state may be seeded from one recorded event.

These assumptions simplify reality. Actual networks have segmentation, different security configurations, patch levels, monitoring, and incident-response controls.

## Possible future experiments

- Split the graph into subgraphs to represent network segmentation.
- Assign different model probabilities to different nodes.
- Add a recovered state to represent remediation.
- Add defender actions such as simulated quarantine.
- Compare outcomes across multiple graph topologies.

These are proposed simulation extensions, not implemented capabilities unless verified in the code.

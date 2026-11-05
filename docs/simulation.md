# Propagation Simulation

The simulator reads graph and event files and writes a simulated timeline. It must not send network traffic or execute actions on other machines.

## Model

- **Nodes:** Lab hosts represented in `nodes.json`.
- **Infrastructure:** Gateways and infrastructure nodes are excluded from the simulated target set.
- **Edges:** The graph builder creates relationships between eligible target nodes according to the documented lab assumption.
- **State:** A target can be `vulnerable` or `infected` in the model.
- **Probability:** Each simulation attempt uses a configured probability value.
- **Seed:** A fixed random seed makes runs reproducible.
- **Termination:** The loop stops when no new simulated infections occur or the configured tick limit is reached.

Example configuration:

```python
P_INFECT = 0.75
SEED = 1337
MAX_TICKS = 20
```

These are illustrative model parameters, not measured probabilities of compromise.

## Initial simulated node

The simulator reads `logs/c2-events.jsonl`. A sanitized event with `"event": "session_open"` can identify the initial node by matching its `remote` field to a node in the graph.

This is a data relationship only. The simulator must not connect to the C2 service or issue instructions to any host.

## Run

```bash
source .venv/bin/activate

python3 propagation-simulator/node-mapping/graph_builder.py \
  network-discovery/asset-inventory/nodes.json \
  propagation-simulator/node-mapping/graph.json

python3 propagation-simulator/propagation-events/simulate.py \
  propagation-simulator/node-mapping/graph.json \
  logs/c2-events.jsonl \
  logs/propagation-timeline.jsonl
```

Adjust arguments to match the actual command-line interface implemented in your scripts.

## Reproducibility

Run the simulator twice with the same inputs and seed, then compare outputs after removing generated timestamps:

```bash
for i in 1 2; do
  python3 propagation-simulator/propagation-events/simulate.py \
    propagation-simulator/node-mapping/graph.json \
    logs/c2-events.jsonl "/tmp/timeline-$i.jsonl" > /dev/null
done

diff \
  <(jq -s 'map(del(.ts))' /tmp/timeline-1.jsonl) \
  <(jq -s 'map(del(.ts))' /tmp/timeline-2.jsonl) \
  && echo "REPRODUCIBLE"
```

A mutation test should alter a copied output and verify that the comparison detects the difference.

## File formats

`logs/c2-events.jsonl`: one sanitized JSON object per line.

`logs/propagation-timeline.jsonl`: one simulated event per line, for example:

```json
{"ts":"2026-11-05T10:15:00Z","tick":1,"event":"simulated_infection","src":"192.0.2.11","dst":"192.0.2.12"}
```

`logs/propagation-timeline.summary.json`: aggregate counts and final simulated node states.

# Architecture

## Overview

The project separates network observation, graph construction, propagation simulation, and visualization. Each stage exchanges files rather than calling the next stage through an API.

```text
Authorized isolated lab
        |
        v
network-discovery/host-discovery/scan.xml
        |
        v
network-discovery/asset-inventory/nodes.json
        |
        v
propagation-simulator/node-mapping/graph_builder.py
        |
        v
propagation-simulator/node-mapping/graph.json
        |
        v
logs/c2-events.jsonl ---> propagation-simulator/propagation-events/simulate.py
                                      |
                                      v
                         logs/propagation-timeline.jsonl
                         logs/propagation-timeline.summary.json
                                      |
                                      v
                         monitoring/dashboard/plot_timeline.py
                         monitoring/dashboard/plot_graph.py
                                      |
                                      v
                         monitoring/dashboard/output/
                         docs/assets/
```

## Why a file-based pipeline?

- Each stage can be replaced without changing its neighbours.
- Intermediate artifacts can be inspected with standard tools such as `cat`, `jq`, and `less`.
- The simulator consumes recorded data and does not perform network actions.
- A stage can be rerun from saved inputs.

## Layer boundaries

| Layer | Reads | Writes | Network activity |
|---|---|---|---|
| Lab event collector | Lab observations | `logs/c2-events.jsonl` | Lab-only |
| Discovery | Authorized lab subnet | `scan.xml`, `nodes.json` | Yes |
| Graph builder | `nodes.json` | `graph.json` | No |
| Simulator | `graph.json`, event JSONL | Timeline and summary | No |
| Visualization | Timeline and graph | PNG figures | No |

The graph builder, simulator, and visualization stages should remain offline and file-only.

## Failure isolation

A simulator failure should not affect discovery artifacts. Previously captured events remain available if the lab is stopped. Graphs and timelines can be regenerated without running the lab again.

## Safety boundary

Use only an isolated environment that you own or are explicitly authorized to test. This documentation describes recorded lab events and simulation; it does not provide instructions for deploying implants, establishing persistence, or propagating software between hosts.

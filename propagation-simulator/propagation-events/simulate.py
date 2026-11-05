#!/usr/bin/env python3
"""Replay C2 session events and simulate worm propagation on the graph.

Model: at each tick, every infected node attempts to infect every
still-vulnerable neighbour with probability P_INFECT. Deterministic with
a fixed seed so runs are reproducible.
"""
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx

P_INFECT = 0.75      # single-attempt infection probability (low security)
SEED = 1337          # fixed for reproducibility
MAX_TICKS = 20       # cap so the sim always terminates


def load_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main(graph_path: Path, events_path: Path, out_path: Path) -> None:
    data = json.loads(graph_path.read_text())
    g = nx.node_link_graph(data)

    rng = random.Random(SEED)

    # Seed the graph from C2 session events.
    for event in load_events(events_path):
        if event.get("event") == "session_open":
            ip = event.get("remote")
            if ip in g.nodes:
                g.nodes[ip]["state"] = "infected"
                g.nodes[ip]["infected_tick"] = 0

    events_out = []
    tick = 0
    while tick < MAX_TICKS:
        tick += 1
        infected_now = [n for n, d in g.nodes(data=True) if d["state"] == "infected"]
        newly_infected = []
        for src in infected_now:
            for dst in g.neighbors(src):
                if g.nodes[dst]["state"] != "vulnerable":
                    continue
                if rng.random() < P_INFECT:
                    g.nodes[dst]["state"] = "infected"
                    g.nodes[dst]["infected_tick"] = tick
                    g.nodes[dst]["infected_by"] = src
                    newly_infected.append(dst)
                    events_out.append(
                        {
                            "ts": datetime.now(timezone.utc).isoformat(),
                            "tick": tick,
                            "event": "infection",
                            "src": src,
                            "dst": dst,
                        }
                    )
        if not newly_infected:
            break

    # Snapshot final state — infrastructure nodes are excluded from the report
    targets = [n for n, d in g.nodes(data=True) if d.get("kind") == "target"]
    summary = {
        "ticks": tick,
        "infected": sorted(n for n in targets if g.nodes[n]["state"] == "infected"),
        "vulnerable": sorted(n for n in targets if g.nodes[n]["state"] == "vulnerable"),
        "events": events_out,
    }
    out_path.write_text("\n".join(json.dumps(e) for e in events_out) + "\n")
    summary_path = out_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"[+] events  → {out_path}")
    print(f"[+] summary → {summary_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(f"usage: {sys.argv[0]} <graph.json> <c2-events.jsonl> <timeline.jsonl>")
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))

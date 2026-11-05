#!/usr/bin/env python3
"""Render the lab graph with node colours reflecting final state."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


def main(graph_path: Path, timeline_path: Path, out_png: Path) -> None:
    graph = json.loads(graph_path.read_text())
    g = nx.node_link_graph(graph)

    infected = set()
    for line in timeline_path.read_text().splitlines():
        if not line.strip():
            continue
        ev = json.loads(line)
        if ev.get("event") == "infection":
            infected.add(ev["dst"])

    c2_events = Path("logs/c2-events.jsonl")
    if c2_events.exists():
        for line in c2_events.read_text().splitlines():
            if not line.strip():
                continue
            ev = json.loads(line)
            if ev.get("event") == "session_open":
                infected.add(ev["remote"])

    colours, labels = [], {}
    for n, d in g.nodes(data=True):
        if d.get("kind") != "target":
            colours.append("#7f8c8d")
            labels[n] = f"{n}\n(infra)"
        elif n in infected:
            colours.append("#c0392b")
            labels[n] = f"{n}\ninfected"
        else:
            colours.append("#27ae60")
            labels[n] = f"{n}\nvulnerable"

    plt.figure(figsize=(7, 5))
    pos = nx.spring_layout(g, seed=42)
    nx.draw_networkx_edges(g, pos, alpha=0.4)
    nx.draw_networkx_nodes(g, pos, node_color=colours, node_size=1800)
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=8)
    plt.title("worm-lab — final propagation state")
    plt.axis("off")
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, dpi=150)
    print(f"[+] wrote {out_png}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(f"usage: {sys.argv[0]} <graph.json> <timeline.jsonl> <out.png>")
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))

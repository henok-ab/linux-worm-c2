#!/usr/bin/env python3
"""Build a NetworkX graph from the asset inventory.

Gateway / infrastructure nodes are excluded so the simulator never
attempts to 'infect' non-target IPs like the Docker bridge gateway.
"""
import json
import sys
from pathlib import Path

import networkx as nx

INFRA_IPS = {"172.28.0.1"}  # Docker bridge gateway — not a worm target


def build_graph(nodes_path: Path) -> nx.Graph:
    nodes = json.loads(nodes_path.read_text())
    g = nx.Graph()
    for node in nodes:
        ip = node["ip"]
        kind = "infrastructure" if ip in INFRA_IPS else "target"
        g.add_node(ip, hostname=node["hostname"], state="vulnerable", kind=kind)
    # Fully-connected assumption for the lab subnet: every target can reach
    # every other target. Real deployments would use /proc/net/arp or a
    # traceroute-based reachability matrix here.
    targets = [n for n, d in g.nodes(data=True) if d["kind"] == "target"]
    for i, src in enumerate(targets):
        for dst in targets[i + 1 :]:
            g.add_edge(src, dst)
    return g


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} <nodes.json> <graph.json>")
    g = build_graph(Path(sys.argv[1]))
    out = Path(sys.argv[2])
    data = nx.node_link_data(g)
    out.write_text(json.dumps(data, indent=2) + "\n")
    targets = [n for n, d in g.nodes(data=True) if d["kind"] == "target"]
    print(f"[+] graph: {len(targets)} targets, {g.number_of_edges()} edges, written to {out}")
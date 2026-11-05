#!/usr/bin/env python3
"""Plot infection counts per tick from propagation-timeline.jsonl."""
import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main(timeline_path: Path, graph_path: Path, out_png: Path) -> None:
    events = [json.loads(l) for l in timeline_path.read_text().splitlines() if l.strip()]
    graph = json.loads(graph_path.read_text())
    total_targets = sum(1 for n in graph["nodes"] if n.get("kind") == "target")

    per_tick = Counter(e["tick"] for e in events)
    ticks = sorted(per_tick)
    counts = [per_tick[t] for t in ticks]

    cumulative = [1]
    for c in counts:
        cumulative.append(cumulative[-1] + c)

    plt.figure(figsize=(8, 4.5))
    plt.step([0] + ticks, cumulative, where="post", marker="o", color="#c0392b", label="infected")
    plt.axhline(total_targets, color="gray", linestyle="--", linewidth=1,
                label=f"total targets ({total_targets})")
    plt.xlabel("tick")
    plt.ylabel("infected nodes")
    plt.title("Worm propagation — infection timeline")
    plt.ylim(0, total_targets + 1)
    plt.xticks([0] + ticks)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, dpi=150)
    print(f"[+] wrote {out_png}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(f"usage: {sys.argv[0]} <timeline.jsonl> <graph.json> <out.png>")
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))

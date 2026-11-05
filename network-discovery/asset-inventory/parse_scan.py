#!/usr/bin/env python3
"""Parse Nmap XML output into a JSON node list for the simulator."""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_scan(xml_path: Path) -> list[dict]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    nodes = []
    for host in root.findall("host"):
        if host.find("status").get("state") != "up":
            continue
        ip = host.find("address[@addrtype='ipv4']").get("addr")
        hostname_el = host.find("hostnames/hostname")
        hostname = hostname_el.get("name") if hostname_el is not None else ip
        nodes.append({"ip": ip, "hostname": hostname, "state": "vulnerable"})
    return sorted(nodes, key=lambda n: [int(x) for x in n["ip"].split(".")])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} <scan.xml> <nodes.json>")
    nodes = parse_scan(Path(sys.argv[1]))
    out = Path(sys.argv[2])
    out.write_text(json.dumps(nodes, indent=2) + "\n")
    print(f"[+] wrote {len(nodes)} nodes to {out}")
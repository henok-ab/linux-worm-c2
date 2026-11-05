# Network Discovery

## Goal

Create an inventory of hosts in an explicitly authorized, isolated lab subnet. The inventory is an input to the graph builder.

## Scope

Before scanning, confirm the exact lab subnet from the virtual network configuration. Do not scan a campus, company, public, or shared network without written authorization.

## Host discovery

For an isolated lab subnet, a host-discovery-only scan can be saved as XML:

```bash
sudo nmap -sn <AUTHORIZED_LAB_SUBNET> -oX host-discovery/scan.xml
```

Replace the placeholder with the subnet assigned to your lab. Do not broaden the target range beyond the approved environment.

## Parse

`network-discovery/asset-inventory/parse_scan.py` should read the XML and write a JSON list of discovered lab nodes. Example schema:

```json
[
  {
    "ip": "192.0.2.11",
    "hostname": "lab-target-1",
    "state": "vulnerable",
    "role": "target"
  },
  {
    "ip": "192.0.2.1",
    "hostname": "lab-gateway",
    "state": "infrastructure",
    "role": "gateway"
  }
]
```

The addresses above are documentation examples. Use the actual addresses from your isolated lab.

## Configuration

`network-discovery/host-discovery/config.yaml` can record the approved subnet and scan settings:

```yaml
network: "<AUTHORIZED_LAB_SUBNET>"
scan_mode: "host-discovery-only"
output_xml: "host-discovery/scan.xml"
```

## Validation

- Confirm every discovered address belongs to the approved lab range.
- Mark gateways and infrastructure separately from simulated targets.
- Do not treat an undiscovered host as proof that it is absent.
- Keep raw scan output out of public commits if it contains sensitive environment details.

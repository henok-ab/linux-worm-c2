# C2 Lab Event Recording

## Purpose

This project uses a recorded command-and-control (C2) lab event as an input to an offline propagation model. The C2 component is not the propagation engine, and the simulator must not issue commands to remote hosts.

## Lab boundary

- Use a private, isolated virtual network.
- Use only disposable virtual machines or containers that you own.
- Do not expose the lab listener or management interface to the public internet or an organization network.
- Do not add persistence, privilege escalation, evasion, credential collection, or lateral-movement functionality.
- Do not commit operator credentials, private keys, implant binaries, or raw sensitive session logs.

## Event record

Record only the minimum metadata needed by the simulator. Example:

```json
{
  "ts": "2026-11-05T10:14:00Z",
  "event": "session_open",
  "session_id": "REDACTED",
  "host": "lab-target-1",
  "remote": "192.0.2.11",
  "transport": "https",
  "operator": "lab-operator",
  "os": "linux/amd64"
}
```

Replace example addresses and identifiers with sanitized lab values. Do not include passwords, tokens, private keys, or command output containing secrets.

## Simulator interface

The simulator should consume the event file as inert JSON data. It should not connect to the C2 service, execute commands, download files, or control an implant.

## What is out of scope

- Implant generation, deployment, or execution instructions.
- Persistence or stealth mechanisms.
- Privilege escalation.
- Lateral movement or self-replication.
- Publicly reachable C2 infrastructure.

# Threat Model

## Purpose

This document distinguishes the safe lab simulation from capabilities that may appear in a real intrusion.

## What the lab demonstrates

- Authorized host discovery in an isolated environment.
- Creation of a host inventory and graph representation.
- Recording of sanitized lab session metadata.
- Offline simulation seeded from a recorded event.
- Reproducible results and visualizations.

## Capability comparison

| Capability | This project | Real intrusion risk |
|---|---|---|
| Initial access | Controlled lab setup | Unauthorized access or exploitation |
| Discovery | Authorized lab host discovery | Broad internal reconnaissance |
| Lateral movement | Simulated graph transitions only | Movement between real systems |
| Persistence | Not implemented | Maintaining access after restart |
| Command and control | Sanitized event metadata for analysis | Remote control of compromised hosts |
| Evasion | Not implemented | Avoiding security monitoring |
| Payload execution | Not part of the simulator | Executing code on target systems |

## Defensive implications

- Segment networks and restrict communication between hosts.
- Monitor unusual outbound connections.
- Keep operating systems and services patched.
- Use endpoint monitoring and centralized logging.
- Restrict administrative privileges.
- Maintain tested backups and an incident-response process.

## Scope statement

This project is intended for defensive education and controlled experimentation in an isolated environment owned by the operator or explicitly authorized for testing. Its propagation component is a file-based simulation, not a deployable worm.

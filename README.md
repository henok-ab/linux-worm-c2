# worm — sliver-based network spreader

Lab-only red team tooling. Isolated network required.
Do not run outside scope.

## Layout
- `sliver/` — C2 profile, setup scripts
- `lab/` — docker-compose for C2 + test VMs
- `src/` — implant, spreader, stager source
- `payloads/` — generated bins (gitignored)
- `runbook/` — operator guides

## Quickstart
1. Fill `.env` with `C2_HOST`
2. `make c2-up`
3. `make beacon`
4. Deploy `payloads/beacon.exe` to seed host

## Phases
0. infra (this)
1. discovery
2. spreaders
3. c2 registration
4. persistence
5. evasion
6. lab test
7. handoff
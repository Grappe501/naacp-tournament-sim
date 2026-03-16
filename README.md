# NAACP Tournament Simulation Platform

This repository contains the architecture and foundation for a modular NCAA-style
tournament simulation system using:

- Python for ingestion, simulation, and orchestration
- PostgreSQL as the source-of-truth database
- TypeScript/Next.js for dashboard and admin surfaces
- Governance-first architecture to prevent drift

## Core Areas

- `apps/` user-facing applications
- `services/` runtime systems
- `packages/` shared contracts, config, db, prompts
- `governance/` protocols, rules, drift controls
- `docs/` architecture and operating documents
- `scripts/` bootstrap and operational scripts

## First Commands

```bash
python scripts/super_bootstrap.py
docker compose up -d
```

## Status

Bootstrapped foundation.

# ARCHITECTURE GRAPH

```text
DATA SOURCES
    ↓
services/ingestion_worker
    ↓
packages/db
    ↓
services/simulation_worker/features
    ↓
services/simulation_worker
    ↓
services/publishing
    ↓
services/api
    ↓
apps/dashboard
```

## Active Subsystems

- Builders: 30
- Ingestion modules: 45
- Simulation modules: 48
- Database modules: 10
- Publishing modules: 0
- API modules: 1


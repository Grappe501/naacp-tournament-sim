# SYSTEM MAP

This document summarizes the current NAACP Tournament platform structure.

## Builders

- `scripts/builders/__init__.py`
- `scripts/builders/ai_builder.py`
- `scripts/builders/api_builder.py`
- `scripts/builders/boxscore_builder.py`
- `scripts/builders/bracket_simulation_builder.py`
- `scripts/builders/dashboard_builder.py`
- `scripts/builders/data_loader_builder.py`
- `scripts/builders/database_builder.py`
- `scripts/builders/db_runtime_builder.py`
- `scripts/builders/env_builder.py`
- `scripts/builders/feature_engineering_builder.py`
- `scripts/builders/governance_builder.py`
- `scripts/builders/harvester_builder.py`
- `scripts/builders/ingestion_builder.py`
- `scripts/builders/metrics_builder.py`
- `scripts/builders/migration_builder.py`
- `scripts/builders/monte_carlo_builder.py`
- `scripts/builders/ncaa_data_builder.py`
- `scripts/builders/pipeline_runner_builder.py`
- `scripts/builders/player_gamelog_harvester_builder.py`
- `scripts/builders/publishing_builder.py`
- `scripts/builders/repo_builder.py`
- `scripts/builders/roster_builder.py`
- `scripts/builders/schedule_builder.py`
- `scripts/builders/schema_builder.py`
- `scripts/builders/simulation_builder.py`
- `scripts/builders/simulation_data_builder.py`
- `scripts/builders/simulation_narrative_builder.py`
- `scripts/builders/tournament_data_harvester_builder.py`
- `scripts/builders/tournament_path_builder.py`

## Database Layer

- `packages/db/connection.py`
- `packages/db/engine.py`
- `packages/db/migration_registry.json`
- `packages/db/migrations/001_teams.sql`
- `packages/db/migrations/002_players.sql`
- `packages/db/migrations/003_games.sql`
- `packages/db/queries.py`
- `packages/db/run_migrations.py`
- `packages/db/schema.sql`
- `packages/db/transactions.py`

## Ingestion Layer

- `services/ingestion_worker/__init__.py`
- `services/ingestion_worker/fetch_teams.py`
- `services/ingestion_worker/ingest.py`
- `services/ingestion_worker/load_data.py`
- `services/ingestion_worker/loaders/__init__.py`
- `services/ingestion_worker/loaders/game_loader.py`
- `services/ingestion_worker/loaders/player_gamelog_loader.py`
- `services/ingestion_worker/loaders/player_loader.py`
- `services/ingestion_worker/loaders/team_loader.py`
- `services/ingestion_worker/models/__init__.py`
- `services/ingestion_worker/models/records.py`
- `services/ingestion_worker/normalizers/__init__.py`
- `services/ingestion_worker/normalizers/player_logs.py`
- `services/ingestion_worker/normalizers/roster_normalizer.py`
- `services/ingestion_worker/normalizers/rosters.py`
- `services/ingestion_worker/normalizers/schedule_normalizer.py`
- `services/ingestion_worker/normalizers/schedules.py`
- `services/ingestion_worker/normalizers/teams.py`
- `services/ingestion_worker/normalizers/teams_normalizer.py`
- `services/ingestion_worker/pipelines/__init__.py`
- `services/ingestion_worker/pipelines/boxscores_pipeline.py`
- `services/ingestion_worker/pipelines/full_harvest.py`
- `services/ingestion_worker/pipelines/metrics_pipeline.py`
- `services/ingestion_worker/pipelines/player_log_harvest.py`
- `services/ingestion_worker/pipelines/player_logs_pipeline.py`
- `services/ingestion_worker/pipelines/rosters_pipeline.py`
- `services/ingestion_worker/pipelines/schedules_pipeline.py`
- `services/ingestion_worker/pipelines/teams_pipeline.py`
- `services/ingestion_worker/registry/__init__.py`
- `services/ingestion_worker/registry/pipelines.py`
- `services/ingestion_worker/registry/source_registry.py`
- `services/ingestion_worker/run_pipelines.py`
- `services/ingestion_worker/sources/__init__.py`
- `services/ingestion_worker/sources/base.py`
- `services/ingestion_worker/sources/espn/__init__.py`
- `services/ingestion_worker/sources/espn/boxscores.py`
- `services/ingestion_worker/sources/espn/player_logs.py`
- `services/ingestion_worker/sources/espn/roster_adapter.py`
- `services/ingestion_worker/sources/espn/rosters.py`
- `services/ingestion_worker/sources/espn/schedule_adapter.py`
- `services/ingestion_worker/sources/espn/schedules.py`
- `services/ingestion_worker/sources/espn/teams.py`
- `services/ingestion_worker/sources/espn/teams_adapter.py`
- `services/ingestion_worker/sources/manual/__init__.py`
- `services/ingestion_worker/utils/http.py`

## Simulation Layer

- `services/simulation_worker/__init__.py`
- `services/simulation_worker/bracket/__init__.py`
- `services/simulation_worker/bracket/bracket_engine.py`
- `services/simulation_worker/bracket/bracket_model.py`
- `services/simulation_worker/config/__init__.py`
- `services/simulation_worker/config/simulation_config.py`
- `services/simulation_worker/data/__init__.py`
- `services/simulation_worker/data/data_loader.py`
- `services/simulation_worker/data/matchup_builder.py`
- `services/simulation_worker/data/team_feature_builder.py`
- `services/simulation_worker/engines/__init__.py`
- `services/simulation_worker/engines/bracket_engine.py`
- `services/simulation_worker/engines/game_engine.py`
- `services/simulation_worker/exports/__init__.py`
- `services/simulation_worker/exports/export_results.py`
- `services/simulation_worker/features/__init__.py`
- `services/simulation_worker/features/feature_pipeline.py`
- `services/simulation_worker/features/game_features.py`
- `services/simulation_worker/features/injury_model.py`
- `services/simulation_worker/features/matchup_features.py`
- `services/simulation_worker/features/player_features.py`
- `services/simulation_worker/features/team_features.py`
- `services/simulation_worker/models/__init__.py`
- `services/simulation_worker/models/player_model.py`
- `services/simulation_worker/monte_carlo/__init__.py`
- `services/simulation_worker/monte_carlo/parallel_engine.py`
- `services/simulation_worker/monte_carlo/tournament_engine.py`
- `services/simulation_worker/monte_carlo/vector_engine.py`
- `services/simulation_worker/narratives/__init__.py`
- `services/simulation_worker/narratives/export_narrative.py`
- `services/simulation_worker/narratives/matchup_reasoning.py`
- `services/simulation_worker/narratives/narrative_writer.py`
- `services/simulation_worker/narratives/reasoning_engine.py`
- `services/simulation_worker/run_bracket_simulation.py`
- `services/simulation_worker/run_database_simulation.py`
- `services/simulation_worker/run_full_tournament_simulation.py`
- `services/simulation_worker/run_massive_monte_carlo.py`
- `services/simulation_worker/run_simulations.py`
- `services/simulation_worker/scenarios/__init__.py`
- `services/simulation_worker/scenarios/injury_model.py`
- `services/simulation_worker/scenarios/scenario_engine.py`
- `services/simulation_worker/simulate.py`
- `services/simulation_worker/tournament/__init__.py`
- `services/simulation_worker/tournament/bracket_structure.py`
- `services/simulation_worker/tournament/game_simulator.py`
- `services/simulation_worker/tournament/probability_engine.py`
- `services/simulation_worker/tournament/round_engine.py`
- `services/simulation_worker/tournament/tournament_engine.py`

## Publishing Layer

None

## API Layer

- `services/api/app.py`

## Apps / Dashboard

- `apps/.gitkeep`
- `apps/dashboard/README.md`

## Scripts

- `scripts/.gitkeep`
- `scripts/bootstrap_docs.py`
- `scripts/bootstrap_system.py`
- `scripts/build.py`
- `scripts/db_bootstrap.py`
- `scripts/project_auditor.py`
- `scripts/project_knowledge_map.py`
- `scripts/project_mapper.py`
- `scripts/run_api.py`
- `scripts/super_bootstrap.py`
- `scripts/utils/__init__.py`
- `scripts/utils/file_utils.py`

## Documentation

- `docs/01-product/.gitkeep`
- `docs/02-architecture/.gitkeep`
- `docs/03-database/.gitkeep`
- `docs/04-ingestion/.gitkeep`
- `docs/05-simulation/.gitkeep`
- `docs/06-ai/.gitkeep`
- `docs/07-api/.gitkeep`
- `docs/08-ui/.gitkeep`
- `docs/09-testing/.gitkeep`
- `docs/10-deployment/.gitkeep`
- `docs/11-operations/.gitkeep`
- `docs/12-roadmap/.gitkeep`
- `docs/file-index.md`
- `docs/master-blueprint.md`

## Tests

- `tests/.gitkeep`
- `tests/test_bootstrap.py`


# DEPENDENCY TREE

This document lists Python files and their direct imports.

## `packages/db/connection.py`

- from contextlib
- from engine

## `packages/db/engine.py`

- from dotenv
- from sqlalchemy
- import os

## `packages/db/queries.py`

- from connection

## `packages/db/run_migrations.py`

- import json
- import os
- import psycopg2

## `packages/db/transactions.py`

- from contextlib
- from engine

## `scripts/bootstrap_docs.py`

- from pathlib

## `scripts/bootstrap_system.py`

- from __future__
- from pathlib
- import subprocess
- import sys

## `scripts/build.py`

- from __future__
- from builders.ai_builder
- from builders.api_builder
- from builders.boxscore_builder
- from builders.bracket_simulation_builder
- from builders.dashboard_builder
- from builders.data_loader_builder
- from builders.database_builder
- from builders.db_runtime_builder
- from builders.env_builder
- from builders.feature_engineering_builder
- from builders.governance_builder
- from builders.harvester_builder
- from builders.ingestion_builder
- from builders.metrics_builder
- from builders.migration_builder
- from builders.monte_carlo_builder
- from builders.ncaa_data_builder
- from builders.pipeline_runner_builder
- from builders.player_gamelog_harvester_builder
- from builders.publishing_builder
- from builders.repo_builder
- from builders.roster_builder
- from builders.schedule_builder
- from builders.schema_builder
- from builders.simulation_builder
- from builders.simulation_data_builder
- from builders.simulation_narrative_builder
- from builders.tournament_data_harvester_builder
- from builders.tournament_path_builder
- from typing
- import sys
- import traceback

## `scripts/builders/__init__.py`

No detected imports.

## `scripts/builders/ai_builder.py`

- from utils.file_utils

## `scripts/builders/api_builder.py`

- from utils.file_utils

## `scripts/builders/boxscore_builder.py`

- from utils.file_utils

## `scripts/builders/bracket_simulation_builder.py`

- from utils.file_utils

## `scripts/builders/dashboard_builder.py`

- from utils.file_utils

## `scripts/builders/data_loader_builder.py`

- from utils.file_utils

## `scripts/builders/database_builder.py`

- from utils.file_utils

## `scripts/builders/db_runtime_builder.py`

- from utils.file_utils

## `scripts/builders/env_builder.py`

- from utils.file_utils

## `scripts/builders/feature_engineering_builder.py`

- from utils.file_utils

## `scripts/builders/governance_builder.py`

- from utils.file_utils

## `scripts/builders/harvester_builder.py`

- from utils.file_utils

## `scripts/builders/ingestion_builder.py`

- from utils.file_utils

## `scripts/builders/metrics_builder.py`

- from utils.file_utils

## `scripts/builders/migration_builder.py`

- from utils.file_utils

## `scripts/builders/monte_carlo_builder.py`

- from utils.file_utils

## `scripts/builders/ncaa_data_builder.py`

- from utils.file_utils

## `scripts/builders/pipeline_runner_builder.py`

- from utils.file_utils

## `scripts/builders/player_gamelog_harvester_builder.py`

- from utils.file_utils

## `scripts/builders/publishing_builder.py`

- from utils.file_utils

## `scripts/builders/repo_builder.py`

- from utils.file_utils

## `scripts/builders/roster_builder.py`

- from utils.file_utils

## `scripts/builders/schedule_builder.py`

- from utils.file_utils

## `scripts/builders/schema_builder.py`

- from utils.file_utils

## `scripts/builders/simulation_builder.py`

- from utils.file_utils

## `scripts/builders/simulation_data_builder.py`

- from utils.file_utils

## `scripts/builders/simulation_narrative_builder.py`

- from utils.file_utils

## `scripts/builders/tournament_data_harvester_builder.py`

- from utils.file_utils

## `scripts/builders/tournament_path_builder.py`

- from utils.file_utils

## `scripts/db_bootstrap.py`

- import psycopg2

## `scripts/project_auditor.py`

- from __future__
- from collections
- from pathlib
- from typing
- import ast
- import os

## `scripts/project_knowledge_map.py`

- from __future__
- from collections
- from pathlib
- import ast
- import os

## `scripts/project_mapper.py`

- from pathlib
- import ast
- import os

## `scripts/run_api.py`

- from pathlib
- import subprocess
- import sys

## `scripts/super_bootstrap.py`

- from pathlib
- import textwrap

## `scripts/utils/__init__.py`

No detected imports.

## `scripts/utils/file_utils.py`

- from pathlib

## `services/api/app.py`

- from flask

## `services/ingestion_worker/__init__.py`

No detected imports.

## `services/ingestion_worker/fetch_teams.py`

- import requests

## `services/ingestion_worker/ingest.py`

No detected imports.

## `services/ingestion_worker/load_data.py`

- from packages.db.connection

## `services/ingestion_worker/loaders/__init__.py`

No detected imports.

## `services/ingestion_worker/loaders/game_loader.py`

- from packages.db.engine
- from sqlalchemy

## `services/ingestion_worker/loaders/player_gamelog_loader.py`

- from packages.db.engine
- from sqlalchemy

## `services/ingestion_worker/loaders/player_loader.py`

- from packages.db.engine
- from sqlalchemy

## `services/ingestion_worker/loaders/team_loader.py`

- from packages.db.engine
- from sqlalchemy

## `services/ingestion_worker/models/__init__.py`

No detected imports.

## `services/ingestion_worker/models/records.py`

- from dataclasses
- from typing

## `services/ingestion_worker/normalizers/__init__.py`

No detected imports.

## `services/ingestion_worker/normalizers/player_logs.py`

- from __future__

## `services/ingestion_worker/normalizers/roster_normalizer.py`

No detected imports.

## `services/ingestion_worker/normalizers/rosters.py`

- from __future__

## `services/ingestion_worker/normalizers/schedule_normalizer.py`

No detected imports.

## `services/ingestion_worker/normalizers/schedules.py`

- from __future__

## `services/ingestion_worker/normalizers/teams.py`

- from __future__

## `services/ingestion_worker/normalizers/teams_normalizer.py`

No detected imports.

## `services/ingestion_worker/pipelines/__init__.py`

No detected imports.

## `services/ingestion_worker/pipelines/boxscores_pipeline.py`

No detected imports.

## `services/ingestion_worker/pipelines/full_harvest.py`

- from services.ingestion_worker.pipelines.rosters_pipeline
- from services.ingestion_worker.pipelines.schedules_pipeline
- from services.ingestion_worker.pipelines.teams_pipeline

## `services/ingestion_worker/pipelines/metrics_pipeline.py`

No detected imports.

## `services/ingestion_worker/pipelines/player_log_harvest.py`

- from packages.db.engine
- from services.ingestion_worker.pipelines.player_logs_pipeline
- from sqlalchemy

## `services/ingestion_worker/pipelines/player_logs_pipeline.py`

- from services.ingestion_worker.loaders.player_gamelog_loader
- from services.ingestion_worker.normalizers.player_logs
- from services.ingestion_worker.sources.espn.player_logs

## `services/ingestion_worker/pipelines/rosters_pipeline.py`

- from services.ingestion_worker.loaders.player_loader
- from services.ingestion_worker.normalizers.rosters
- from services.ingestion_worker.sources.espn.rosters

## `services/ingestion_worker/pipelines/schedules_pipeline.py`

- from services.ingestion_worker.loaders.game_loader
- from services.ingestion_worker.normalizers.schedules
- from services.ingestion_worker.sources.espn.schedules

## `services/ingestion_worker/pipelines/teams_pipeline.py`

- from services.ingestion_worker.loaders.team_loader
- from services.ingestion_worker.normalizers.teams
- from services.ingestion_worker.sources.espn.teams

## `services/ingestion_worker/registry/__init__.py`

No detected imports.

## `services/ingestion_worker/registry/pipelines.py`

No detected imports.

## `services/ingestion_worker/registry/source_registry.py`

No detected imports.

## `services/ingestion_worker/run_pipelines.py`

- from services.ingestion_worker.pipelines.full_harvest
- from services.ingestion_worker.pipelines.rosters_pipeline
- from services.ingestion_worker.pipelines.schedules_pipeline
- from services.ingestion_worker.pipelines.teams_pipeline
- import sys

## `services/ingestion_worker/sources/__init__.py`

No detected imports.

## `services/ingestion_worker/sources/base.py`

- from abc
- from typing

## `services/ingestion_worker/sources/espn/__init__.py`

No detected imports.

## `services/ingestion_worker/sources/espn/boxscores.py`

- from services.ingestion_worker.utils.http

## `services/ingestion_worker/sources/espn/player_logs.py`

- from services.ingestion_worker.utils.http

## `services/ingestion_worker/sources/espn/roster_adapter.py`

No detected imports.

## `services/ingestion_worker/sources/espn/rosters.py`

- from services.ingestion_worker.utils.http

## `services/ingestion_worker/sources/espn/schedule_adapter.py`

No detected imports.

## `services/ingestion_worker/sources/espn/schedules.py`

- from services.ingestion_worker.utils.http

## `services/ingestion_worker/sources/espn/teams.py`

- from services.ingestion_worker.utils.http

## `services/ingestion_worker/sources/espn/teams_adapter.py`

No detected imports.

## `services/ingestion_worker/sources/manual/__init__.py`

No detected imports.

## `services/ingestion_worker/utils/http.py`

- from __future__
- import requests

## `services/simulation_worker/__init__.py`

No detected imports.

## `services/simulation_worker/bracket/__init__.py`

No detected imports.

## `services/simulation_worker/bracket/bracket_engine.py`

- from collections
- from services.simulation_worker.data.matchup_builder
- from services.simulation_worker.engines.bracket_engine

## `services/simulation_worker/bracket/bracket_model.py`

- from dataclasses

## `services/simulation_worker/config/__init__.py`

No detected imports.

## `services/simulation_worker/config/simulation_config.py`

- from dataclasses

## `services/simulation_worker/data/__init__.py`

No detected imports.

## `services/simulation_worker/data/data_loader.py`

- from packages.db.connection

## `services/simulation_worker/data/matchup_builder.py`

- from services.simulation_worker.data.data_loader
- from services.simulation_worker.data.team_feature_builder
- from services.simulation_worker.engines.game_engine

## `services/simulation_worker/data/team_feature_builder.py`

- import random

## `services/simulation_worker/engines/__init__.py`

No detected imports.

## `services/simulation_worker/engines/bracket_engine.py`

- from collections
- from services.simulation_worker.engines.game_engine

## `services/simulation_worker/engines/game_engine.py`

- from dataclasses
- import random

## `services/simulation_worker/exports/__init__.py`

No detected imports.

## `services/simulation_worker/exports/export_results.py`

- from pathlib
- import json

## `services/simulation_worker/features/__init__.py`

No detected imports.

## `services/simulation_worker/features/feature_pipeline.py`

- from services.simulation_worker.features.player_features
- from services.simulation_worker.features.team_features

## `services/simulation_worker/features/game_features.py`

No detected imports.

## `services/simulation_worker/features/injury_model.py`

- import random

## `services/simulation_worker/features/matchup_features.py`

No detected imports.

## `services/simulation_worker/features/player_features.py`

- from packages.db.connection

## `services/simulation_worker/features/team_features.py`

- from packages.db.connection

## `services/simulation_worker/models/__init__.py`

No detected imports.

## `services/simulation_worker/models/player_model.py`

- from dataclasses
- import random

## `services/simulation_worker/monte_carlo/__init__.py`

No detected imports.

## `services/simulation_worker/monte_carlo/parallel_engine.py`

- from __future__
- from concurrent.futures
- from math
- from services.simulation_worker.monte_carlo.vector_engine

## `services/simulation_worker/monte_carlo/tournament_engine.py`

- from __future__
- from collections

## `services/simulation_worker/monte_carlo/vector_engine.py`

- from __future__
- import numpy

## `services/simulation_worker/narratives/__init__.py`

No detected imports.

## `services/simulation_worker/narratives/export_narrative.py`

- from pathlib
- import json

## `services/simulation_worker/narratives/matchup_reasoning.py`

No detected imports.

## `services/simulation_worker/narratives/narrative_writer.py`

- from services.simulation_worker.narratives.matchup_reasoning
- from services.simulation_worker.narratives.reasoning_engine

## `services/simulation_worker/narratives/reasoning_engine.py`

No detected imports.

## `services/simulation_worker/run_bracket_simulation.py`

- from services.simulation_worker.bracket.bracket_engine
- from services.simulation_worker.bracket.bracket_model

## `services/simulation_worker/run_database_simulation.py`

- from services.simulation_worker.data.matchup_builder
- from services.simulation_worker.engines.bracket_engine
- from services.simulation_worker.exports.export_results

## `services/simulation_worker/run_full_tournament_simulation.py`

- from services.simulation_worker.tournament.tournament_engine

## `services/simulation_worker/run_massive_monte_carlo.py`

- from services.simulation_worker.exports.export_results
- from services.simulation_worker.monte_carlo.parallel_engine
- from services.simulation_worker.narratives.export_narrative
- from services.simulation_worker.narratives.narrative_writer

## `services/simulation_worker/run_simulations.py`

- from services.simulation_worker.config.simulation_config
- from services.simulation_worker.engines.bracket_engine
- from services.simulation_worker.engines.game_engine
- from services.simulation_worker.exports.export_results

## `services/simulation_worker/scenarios/__init__.py`

No detected imports.

## `services/simulation_worker/scenarios/injury_model.py`

- import random

## `services/simulation_worker/scenarios/scenario_engine.py`

No detected imports.

## `services/simulation_worker/simulate.py`

No detected imports.

## `services/simulation_worker/tournament/__init__.py`

No detected imports.

## `services/simulation_worker/tournament/bracket_structure.py`

No detected imports.

## `services/simulation_worker/tournament/game_simulator.py`

- from services.simulation_worker.monte_carlo.vector_engine

## `services/simulation_worker/tournament/probability_engine.py`

- from collections

## `services/simulation_worker/tournament/round_engine.py`

- from services.simulation_worker.tournament.game_simulator

## `services/simulation_worker/tournament/tournament_engine.py`

- from services.simulation_worker.tournament.bracket_structure
- from services.simulation_worker.tournament.round_engine

## `tests/test_bootstrap.py`

No detected imports.


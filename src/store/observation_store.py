"""Observation store interfaces and concrete append-only implementations."""

from __future__ import annotations

import json
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path

from src.core.models import Observation


class ObservationStore(ABC):
    """Minimal persistence boundary for append and lookup by id."""

    @abstractmethod
    def append(self, observation: Observation) -> None:
        """Append an observation to the store."""

    @abstractmethod
    def get_by_id(self, observation_id: str) -> Observation | None:
        """Return an observation by id if present."""


class InMemoryObservationStore(ObservationStore):
    """Test-oriented in-memory append-only observation store."""

    def __init__(self) -> None:
        self._items: dict[str, Observation] = {}

    def append(self, observation: Observation) -> None:
        if observation.observation_id in self._items:
            msg = f"Observation already exists: {observation.observation_id}"
            raise ValueError(msg)
        self._items[observation.observation_id] = observation

    def get_by_id(self, observation_id: str) -> Observation | None:
        return self._items.get(observation_id)


class SQLiteObservationStore(ObservationStore):
    """Minimal SQLite-backed append-only observation store."""

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)
        self._ensure_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _ensure_table(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS observations (
                    observation_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_independence_group TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    raw_payload TEXT NOT NULL,
                    parsed_payload TEXT NOT NULL,
                    ingest_status TEXT NOT NULL
                )
                """
            )

    def append(self, observation: Observation) -> None:
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO observations (
                        observation_id,
                        timestamp,
                        source_id,
                        source_type,
                        source_independence_group,
                        session_id,
                        task_id,
                        raw_payload,
                        parsed_payload,
                        ingest_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        observation.observation_id,
                        _serialize_timestamp(observation.timestamp),
                        observation.source_id,
                        observation.source_type,
                        observation.source_independence_group,
                        observation.session_id,
                        observation.task_id,
                        observation.raw_payload,
                        json.dumps(observation.parsed_payload, sort_keys=True),
                        observation.ingest_status,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            msg = f"Observation already exists: {observation.observation_id}"
            raise ValueError(msg) from exc

    def get_by_id(self, observation_id: str) -> Observation | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT
                    observation_id,
                    timestamp,
                    source_id,
                    source_type,
                    source_independence_group,
                    session_id,
                    task_id,
                    raw_payload,
                    parsed_payload,
                    ingest_status
                FROM observations
                WHERE observation_id = ?
                """,
                (observation_id,),
            ).fetchone()

        if row is None:
            return None

        return Observation(
            observation_id=row[0],
            timestamp=_deserialize_timestamp(row[1]),
            source_id=row[2],
            source_type=row[3],
            source_independence_group=row[4],
            session_id=row[5],
            task_id=row[6],
            raw_payload=row[7],
            parsed_payload=json.loads(row[8]),
            ingest_status=row[9],
        )


def _serialize_timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc).isoformat()
    return value.astimezone(timezone.utc).isoformat()


def _deserialize_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value)

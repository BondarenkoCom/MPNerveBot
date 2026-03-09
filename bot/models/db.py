from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from bot.models.entities import AlertSettings, MarketplaceAccount, OnboardingSession


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Database:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS telegram_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_user_id INTEGER NOT NULL UNIQUE,
                    chat_id INTEGER NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS marketplace_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    marketplace TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    connection_mode TEXT NOT NULL,
                    status TEXT NOT NULL,
                    credentials_json TEXT,
                    use_mock INTEGER NOT NULL DEFAULT 1,
                    last_validated_at TEXT,
                    last_sync_at TEXT,
                    last_error_text TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(chat_id, marketplace)
                );

                CREATE TABLE IF NOT EXISTS alert_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL UNIQUE,
                    stock_days_threshold INTEGER NOT NULL DEFAULT 5,
                    sales_drop_percent_threshold INTEGER NOT NULL DEFAULT 30,
                    review_age_hours_threshold INTEGER NOT NULL DEFAULT 24,
                    digest_enabled INTEGER NOT NULL DEFAULT 1,
                    alerts_enabled INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS onboarding_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL UNIQUE,
                    state TEXT NOT NULL,
                    selected_marketplace TEXT,
                    payload_json TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS digest_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    marketplace TEXT NOT NULL,
                    digest_date TEXT NOT NULL,
                    message_id INTEGER,
                    status TEXT NOT NULL,
                    payload_json TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS alert_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    marketplace TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    dedupe_key TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    sent_at TEXT NOT NULL,
                    UNIQUE(chat_id, dedupe_key)
                );

                CREATE TABLE IF NOT EXISTS review_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    marketplace TEXT NOT NULL,
                    external_review_id TEXT NOT NULL,
                    review_text TEXT NOT NULL,
                    draft_reply_text TEXT,
                    action TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

    def upsert_telegram_user(
        self,
        telegram_user_id: int,
        chat_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
    ) -> None:
        now = _utc_now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO telegram_users (
                    telegram_user_id, chat_id, username, first_name, last_name, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(telegram_user_id) DO UPDATE SET
                    chat_id = excluded.chat_id,
                    username = excluded.username,
                    first_name = excluded.first_name,
                    last_name = excluded.last_name,
                    updated_at = excluded.updated_at
                """,
                (telegram_user_id, chat_id, username, first_name, last_name, now, now),
            )

    def get_or_create_alert_settings(self, chat_id: int) -> AlertSettings:
        now = _utc_now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO alert_settings (
                    chat_id, created_at, updated_at
                )
                VALUES (?, ?, ?)
                ON CONFLICT(chat_id) DO NOTHING
                """,
                (chat_id, now, now),
            )
            row = connection.execute(
                """
                SELECT chat_id,
                       stock_days_threshold,
                       sales_drop_percent_threshold,
                       review_age_hours_threshold,
                       digest_enabled,
                       alerts_enabled
                FROM alert_settings
                WHERE chat_id = ?
                """,
                (chat_id,),
            ).fetchone()

        if row is None:
            raise RuntimeError("Alert settings row was not created")

        return AlertSettings(
            chat_id=row["chat_id"],
            stock_days_threshold=row["stock_days_threshold"],
            sales_drop_percent_threshold=row["sales_drop_percent_threshold"],
            review_age_hours_threshold=row["review_age_hours_threshold"],
            digest_enabled=bool(row["digest_enabled"]),
            alerts_enabled=bool(row["alerts_enabled"]),
        )

    def upsert_onboarding_session(
        self,
        chat_id: int,
        state: str,
        selected_marketplace: str | None = None,
        payload: dict | None = None,
    ) -> None:
        now = _utc_now()
        payload_json = json.dumps(payload, ensure_ascii=False) if payload is not None else None
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO onboarding_sessions (
                    chat_id, state, selected_marketplace, payload_json, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET
                    state = excluded.state,
                    selected_marketplace = excluded.selected_marketplace,
                    payload_json = excluded.payload_json,
                    updated_at = excluded.updated_at
                """,
                (chat_id, state, selected_marketplace, payload_json, now, now),
            )

    def get_onboarding_session(self, chat_id: int) -> OnboardingSession | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT chat_id, state, selected_marketplace, payload_json
                FROM onboarding_sessions
                WHERE chat_id = ?
                """,
                (chat_id,),
            ).fetchone()

        if row is None:
            return None

        return OnboardingSession(
            chat_id=row["chat_id"],
            state=row["state"],
            selected_marketplace=row["selected_marketplace"],
            payload_json=row["payload_json"],
        )

    def clear_onboarding_session(self, chat_id: int) -> None:
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM onboarding_sessions WHERE chat_id = ?",
                (chat_id,),
            )

    def upsert_marketplace_account(
        self,
        chat_id: int,
        marketplace: str,
        display_name: str,
        connection_mode: str,
        status: str,
        credentials: dict | None,
        use_mock: bool,
    ) -> None:
        now = _utc_now()
        credentials_json = json.dumps(credentials, ensure_ascii=False) if credentials is not None else None
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO marketplace_accounts (
                    chat_id, marketplace, display_name, connection_mode, status, credentials_json,
                    use_mock, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(chat_id, marketplace) DO UPDATE SET
                    display_name = excluded.display_name,
                    connection_mode = excluded.connection_mode,
                    status = excluded.status,
                    credentials_json = excluded.credentials_json,
                    use_mock = excluded.use_mock,
                    updated_at = excluded.updated_at
                """,
                (
                    chat_id,
                    marketplace,
                    display_name,
                    connection_mode,
                    status,
                    credentials_json,
                    int(use_mock),
                    now,
                    now,
                ),
            )

    def list_marketplace_accounts(self, chat_id: int) -> list[MarketplaceAccount]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT chat_id, marketplace, display_name, connection_mode, status, credentials_json,
                       use_mock, last_validated_at, last_error_text
                FROM marketplace_accounts
                WHERE chat_id = ?
                ORDER BY marketplace
                """,
                (chat_id,),
            ).fetchall()

        return [
            MarketplaceAccount(
                chat_id=row["chat_id"],
                marketplace=row["marketplace"],
                display_name=row["display_name"],
                connection_mode=row["connection_mode"],
                status=row["status"],
                credentials_json=row["credentials_json"],
                use_mock=bool(row["use_mock"]),
                last_validated_at=row["last_validated_at"],
                last_error_text=row["last_error_text"],
            )
            for row in rows
        ]

    def get_marketplace_account(self, chat_id: int, marketplace: str) -> MarketplaceAccount | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT chat_id, marketplace, display_name, connection_mode, status, credentials_json,
                       use_mock, last_validated_at, last_error_text
                FROM marketplace_accounts
                WHERE chat_id = ? AND marketplace = ?
                """,
                (chat_id, marketplace),
            ).fetchone()

        if row is None:
            return None

        return MarketplaceAccount(
            chat_id=row["chat_id"],
            marketplace=row["marketplace"],
            display_name=row["display_name"],
            connection_mode=row["connection_mode"],
            status=row["status"],
            credentials_json=row["credentials_json"],
            use_mock=bool(row["use_mock"]),
            last_validated_at=row["last_validated_at"],
            last_error_text=row["last_error_text"],
        )

    def mark_marketplace_account_validation(
        self,
        chat_id: int,
        marketplace: str,
        status: str,
        display_name: str | None = None,
        error_text: str | None = None,
    ) -> None:
        now = _utc_now()
        with self._connect() as connection:
            if display_name is None:
                connection.execute(
                    """
                    UPDATE marketplace_accounts
                    SET status = ?,
                        last_validated_at = ?,
                        last_error_text = ?,
                        updated_at = ?
                    WHERE chat_id = ? AND marketplace = ?
                    """,
                    (status, now, error_text, now, chat_id, marketplace),
                )
            else:
                connection.execute(
                    """
                    UPDATE marketplace_accounts
                    SET display_name = ?,
                        status = ?,
                        last_validated_at = ?,
                        last_error_text = ?,
                        updated_at = ?
                    WHERE chat_id = ? AND marketplace = ?
                    """,
                    (display_name, status, now, error_text, now, chat_id, marketplace),
                )

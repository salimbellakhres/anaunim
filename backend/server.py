import argparse
import json
import mimetypes
import os
import secrets
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, unquote, urlparse
from urllib.request import Request, urlopen

try:
    from backend.adapters import adapter_for
    from backend.capabilities import CAPABILITY_MATRIX
except ModuleNotFoundError:
    from adapters import adapter_for
    from capabilities import CAPABILITY_MATRIX


ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = Path(__file__).resolve().with_name("seed.json")
ENV_PATH = ROOT / ".env"
META_SCOPES = [
    "pages_show_list",
    "pages_read_engagement",
    "pages_manage_engagement",
    "instagram_basic",
    "instagram_manage_comments",
]

STATIC_CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}


def load_env():
    if not ENV_PATH.exists():
        return

    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()


def configured_data_dir():
    value = os.environ.get("DATA_DIR", "").strip()
    return Path(value).expanduser() if value else ROOT / "data"


DATA_DIR = configured_data_dir()
DB_PATH = Path(os.environ.get("DATABASE_PATH", DATA_DIR / "anaunim.sqlite")).expanduser()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def open_db():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with open_db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS networks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                short_name TEXT NOT NULL,
                accent TEXT NOT NULL,
                status TEXT NOT NULL,
                handle TEXT NOT NULL,
                scopes_json TEXT NOT NULL,
                capability TEXT NOT NULL,
                capability_level TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS interactions (
                id TEXT PRIMARY KEY,
                network TEXT NOT NULL REFERENCES networks(id),
                type TEXT NOT NULL,
                status TEXT NOT NULL,
                actor TEXT NOT NULL,
                handle TEXT NOT NULL,
                avatar TEXT NOT NULL,
                media TEXT NOT NULL,
                target TEXT NOT NULL,
                text TEXT NOT NULL,
                date TEXT NOT NULL,
                provider_ref TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS removal_jobs (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                mode TEXT NOT NULL,
                requested_count INTEGER NOT NULL,
                processed_count INTEGER NOT NULL DEFAULT 0,
                failed_count INTEGER NOT NULL DEFAULT 0,
                error TEXT,
                created_at TEXT NOT NULL,
                completed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS removal_job_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL REFERENCES removal_jobs(id),
                interaction_id TEXT NOT NULL REFERENCES interactions(id),
                network TEXT NOT NULL,
                type TEXT NOT NULL,
                previous_status TEXT NOT NULL,
                result_status TEXT NOT NULL,
                error TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                actor TEXT NOT NULL,
                network TEXT,
                interaction_id TEXT,
                job_id TEXT,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS oauth_states (
                state TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                redirect_uri TEXT NOT NULL,
                scopes_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                used_at TEXT
            );

            CREATE TABLE IF NOT EXISTS provider_tokens (
                provider TEXT PRIMARY KEY,
                token_type TEXT NOT NULL,
                access_token TEXT NOT NULL,
                expires_at TEXT,
                raw_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS meta_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id TEXT NOT NULL UNIQUE,
                page_name TEXT NOT NULL,
                page_access_token TEXT,
                instagram_business_account_id TEXT,
                instagram_username TEXT,
                tasks_json TEXT NOT NULL,
                raw_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )

        count = conn.execute("SELECT COUNT(*) FROM networks").fetchone()[0]
        if count == 0:
            seed_database(conn)
        conn.commit()


def seed_database(conn):
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    timestamp = utc_now()

    for network in seed["networks"]:
        conn.execute(
            """
            INSERT INTO networks (
                id, name, short_name, accent, status, handle, scopes_json,
                capability, capability_level, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                network["id"],
                network["name"],
                network["shortName"],
                network["accent"],
                network["status"],
                network["handle"],
                json.dumps(network["scopes"]),
                network["capability"],
                network["capabilityLevel"],
                timestamp,
                timestamp,
            ),
        )

    for interaction in seed["interactions"]:
        conn.execute(
            """
            INSERT INTO interactions (
                id, network, type, status, actor, handle, avatar, media,
                target, text, date, provider_ref, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                interaction["id"],
                interaction["network"],
                interaction["type"],
                interaction["status"],
                interaction["actor"],
                interaction["handle"],
                interaction["avatar"],
                interaction["media"],
                interaction["target"],
                interaction["text"],
                interaction["date"],
                interaction["id"],
                timestamp,
                timestamp,
            ),
        )

    conn.execute(
        """
        INSERT INTO audit_log (action, actor, payload_json, created_at)
        VALUES (?, ?, ?, ?)
        """,
        ("seed_database", "system", json.dumps({"networks": 5, "interactions": 15}), timestamp),
    )


def network_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "shortName": row["short_name"],
        "accent": row["accent"],
        "status": row["status"],
        "handle": row["handle"],
        "scopes": json.loads(row["scopes_json"]),
        "capability": row["capability"],
        "capabilityLevel": row["capability_level"],
    }


def interaction_dict(row):
    return {
        "id": row["id"],
        "network": row["network"],
        "type": row["type"],
        "status": row["status"],
        "actor": row["actor"],
        "handle": row["handle"],
        "avatar": row["avatar"],
        "media": row["media"],
        "target": row["target"],
        "text": row["text"],
        "date": row["date"],
        "providerRef": row["provider_ref"],
        "updatedAt": row["updated_at"],
    }


def job_dict(row):
    return {
        "id": row["id"],
        "status": row["status"],
        "mode": row["mode"],
        "requestedCount": row["requested_count"],
        "processedCount": row["processed_count"],
        "failedCount": row["failed_count"],
        "error": row["error"],
        "createdAt": row["created_at"],
        "completedAt": row["completed_at"],
    }


def audit_dict(row):
    return {
        "id": row["id"],
        "action": row["action"],
        "actor": row["actor"],
        "network": row["network"],
        "interactionId": row["interaction_id"],
        "jobId": row["job_id"],
        "payload": json.loads(row["payload_json"]),
        "createdAt": row["created_at"],
    }


def meta_account_dict(row):
    return {
        "pageId": row["page_id"],
        "pageName": row["page_name"],
        "hasPageAccessToken": bool(row["page_access_token"]),
        "instagramBusinessAccountId": row["instagram_business_account_id"],
        "instagramUsername": row["instagram_username"],
        "tasks": json.loads(row["tasks_json"]),
        "updatedAt": row["updated_at"],
    }


def meta_status(conn):
    token = conn.execute("SELECT * FROM provider_tokens WHERE provider = 'meta'").fetchone()
    accounts = conn.execute("SELECT * FROM meta_accounts ORDER BY page_name").fetchall()
    app_id = os.environ.get("META_APP_ID", "")
    redirect_uri = os.environ.get("META_REDIRECT_URI", "")

    return {
        "configured": bool(app_id and os.environ.get("META_APP_SECRET") and redirect_uri),
        "appId": app_id,
        "redirectUri": redirect_uri,
        "graphVersion": os.environ.get("META_GRAPH_VERSION", "v23.0"),
        "hasLoginConfigId": bool(os.environ.get("META_LOGIN_CONFIG_ID", "").strip()),
        "hasUserToken": bool(token),
        "userTokenExpiresAt": token["expires_at"] if token else None,
        "accounts": [meta_account_dict(row) for row in accounts],
    }


def bootstrap_payload(conn, extra=None):
    networks = [
        network_dict(row)
        for row in conn.execute("SELECT * FROM networks ORDER BY rowid")
    ]
    interactions = [
        interaction_dict(row)
        for row in conn.execute("SELECT * FROM interactions ORDER BY rowid")
    ]
    jobs = [
        job_dict(row)
        for row in conn.execute("SELECT * FROM removal_jobs ORDER BY created_at DESC LIMIT 10")
    ]
    audit = [
        audit_dict(row)
        for row in conn.execute("SELECT * FROM audit_log ORDER BY created_at DESC, id DESC LIMIT 12")
    ]

    payload = {
        "serverMode": "mock-backend",
        "databasePath": str(DB_PATH),
        "networks": networks,
        "interactions": interactions,
        "jobs": jobs,
        "auditLog": audit,
        "capabilities": CAPABILITY_MATRIX,
        "meta": meta_status(conn),
    }
    if extra:
        payload.update(extra)
    return payload


def read_json(handler):
    length = int(handler.headers.get("Content-Length", "0") or "0")
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    return json.loads(raw.decode("utf-8"))


def write_json(handler, status, payload):
    body = json.dumps(payload, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def write_error(handler, status, message):
    write_json(handler, status, {"error": message})


def log_audit(conn, action, actor="local-user", network=None, interaction_id=None, job_id=None, payload=None):
    conn.execute(
        """
        INSERT INTO audit_log (
            action, actor, network, interaction_id, job_id, payload_json, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            action,
            actor,
            network,
            interaction_id,
            job_id,
            json.dumps(payload or {}),
            utc_now(),
        ),
    )


def sync_mock_providers(conn):
    results = []
    accounts = [network_dict(row) for row in conn.execute("SELECT * FROM networks ORDER BY rowid")]

    for account in accounts:
        if account["status"] == "disconnected":
            continue
        adapter = adapter_for(account["id"])
        result = adapter.sync_interactions(account)
        results.append(result)
        log_audit(
            conn,
            "sync_provider",
            "system",
            network=account["id"],
            payload=result,
        )

    return results


def create_removal_job(conn, payload):
    ids = [str(item) for item in payload.get("ids", []) if str(item).strip()]
    if not ids:
        raise ValueError("No interaction IDs were provided.")

    placeholders = ",".join("?" for _ in ids)
    rows = conn.execute(
        f"SELECT * FROM interactions WHERE id IN ({placeholders}) AND status != 'removed'",
        ids,
    ).fetchall()
    if not rows:
        raise ValueError("No active interactions matched the request.")

    job_id = uuid.uuid4().hex[:12]
    timestamp = utc_now()
    conn.execute(
        """
        INSERT INTO removal_jobs (
            id, status, mode, requested_count, processed_count, failed_count,
            created_at
        )
        VALUES (?, ?, ?, ?, 0, 0, ?)
        """,
        (job_id, "processing", payload.get("mode", "manual"), len(rows), timestamp),
    )

    processed = 0
    failed = 0

    by_network = {}
    for row in rows:
        by_network.setdefault(row["network"], []).append(row)

    for network_id, network_rows in by_network.items():
        adapter = adapter_for(network_id)
        results = adapter.remove_many([dict(row) for row in network_rows])
        results_by_id = {result["interaction_id"]: result for result in results}

        for row in network_rows:
            result = results_by_id.get(row["id"])
            if result and result["status"] == "removed":
                conn.execute(
                    """
                    UPDATE interactions
                    SET status = 'removed', updated_at = ?
                    WHERE id = ?
                    """,
                    (utc_now(), row["id"]),
                )
                conn.execute(
                    """
                    INSERT INTO removal_job_items (
                        job_id, interaction_id, network, type, previous_status,
                        result_status, error, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        job_id,
                        row["id"],
                        row["network"],
                        row["type"],
                        row["status"],
                        "removed",
                        None,
                        utc_now(),
                    ),
                )
                processed += 1
                log_audit(
                    conn,
                    "remove_interaction",
                    payload.get("actor", "local-user"),
                    network=row["network"],
                    interaction_id=row["id"],
                    job_id=job_id,
                    payload=result,
                )
            else:
                failed += 1
                conn.execute(
                    """
                    INSERT INTO removal_job_items (
                        job_id, interaction_id, network, type, previous_status,
                        result_status, error, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        job_id,
                        row["id"],
                        row["network"],
                        row["type"],
                        row["status"],
                        "failed",
                        "Mock adapter did not return a removal result.",
                        utc_now(),
                    ),
                )

    status = "completed" if failed == 0 else "completed_with_errors"
    conn.execute(
        """
        UPDATE removal_jobs
        SET status = ?, processed_count = ?, failed_count = ?, completed_at = ?
        WHERE id = ?
        """,
        (status, processed, failed, utc_now(), job_id),
    )
    log_audit(
        conn,
        "remove_job_completed",
        payload.get("actor", "local-user"),
        job_id=job_id,
        payload={"processed": processed, "failed": failed},
    )

    return job_id


def undo_removal_job(conn, payload):
    job_id = payload.get("jobId") or payload.get("job_id")
    if not job_id:
        row = conn.execute(
            """
            SELECT *
            FROM removal_jobs
            WHERE status IN ('completed', 'completed_with_errors')
            ORDER BY completed_at DESC
            LIMIT 1
            """
        ).fetchone()
        if not row:
            raise ValueError("No completed removal job is available to undo.")
        job_id = row["id"]

    job = conn.execute("SELECT * FROM removal_jobs WHERE id = ?", (job_id,)).fetchone()
    if not job:
        raise ValueError("Removal job was not found.")
    if job["status"] == "undone":
        raise ValueError("Removal job has already been undone.")

    items = conn.execute(
        "SELECT * FROM removal_job_items WHERE job_id = ? AND result_status = 'removed'",
        (job_id,),
    ).fetchall()
    if not items:
        raise ValueError("Removal job has no removable items to restore.")

    for item in items:
        conn.execute(
            """
            UPDATE interactions
            SET status = ?, updated_at = ?
            WHERE id = ?
            """,
            (item["previous_status"], utc_now(), item["interaction_id"]),
        )
        log_audit(
            conn,
            "undo_remove_interaction",
            payload.get("actor", "local-user"),
            network=item["network"],
            interaction_id=item["interaction_id"],
            job_id=job_id,
            payload={"restoredStatus": item["previous_status"]},
        )

    conn.execute(
        "UPDATE removal_jobs SET status = ?, completed_at = ? WHERE id = ?",
        ("undone", utc_now(), job_id),
    )
    log_audit(
        conn,
        "remove_job_undone",
        payload.get("actor", "local-user"),
        job_id=job_id,
        payload={"restored": len(items)},
    )
    return job_id


def toggle_account(conn, payload):
    network_id = payload.get("networkId") or payload.get("network_id")
    if not network_id:
        raise ValueError("No network ID was provided.")

    row = conn.execute("SELECT * FROM networks WHERE id = ?", (network_id,)).fetchone()
    if not row:
        raise ValueError("Network was not found.")

    next_status = "disconnected" if row["status"] == "connected" else "connected"
    conn.execute(
        "UPDATE networks SET status = ?, updated_at = ? WHERE id = ?",
        (next_status, utc_now(), network_id),
    )
    log_audit(
        conn,
        "toggle_account",
        payload.get("actor", "local-user"),
        network=network_id,
        payload={"from": row["status"], "to": next_status},
    )
    return next_status


def meta_graph_version():
    return os.environ.get("META_GRAPH_VERSION", "v23.0").strip() or "v23.0"


def meta_graph_url(path):
    normalized = path if path.startswith("/") else f"/{path}"
    return f"https://graph.facebook.com/{meta_graph_version()}{normalized}"


def meta_config():
    return {
        "app_id": os.environ.get("META_APP_ID", "").strip(),
        "app_secret": os.environ.get("META_APP_SECRET", "").strip(),
        "login_config_id": os.environ.get("META_LOGIN_CONFIG_ID", "").strip(),
        "redirect_uri": os.environ.get(
            "META_REDIRECT_URI",
            "http://localhost:5173/api/oauth/callback?provider=instagram",
        ).strip(),
    }


def require_meta_config():
    config = meta_config()
    missing = [
        key
        for key, value in config.items()
        if key != "login_config_id" and not value
    ]
    if missing:
        raise ValueError(f"Meta OAuth is missing: {', '.join(missing)}.")
    return config


def http_json(url, method="GET", data=None):
    body = None
    headers = {"Accept": "application/json"}
    if data is not None:
        body = urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    request = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise ValueError(f"Meta API returned HTTP {exc.code}: {details}") from exc
    except URLError as exc:
        raise ValueError(f"Could not reach Meta API: {exc.reason}") from exc


def start_meta_oauth(conn, provider_id):
    if provider_id not in {"instagram", "facebook", "meta"}:
        raise ValueError("Meta OAuth can only start for instagram, facebook, or meta.")

    config = require_meta_config()
    state = secrets.token_urlsafe(32)
    timestamp = utc_now()
    conn.execute(
        """
        INSERT INTO oauth_states (state, provider, redirect_uri, scopes_json, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (state, provider_id, config["redirect_uri"], json.dumps(META_SCOPES), timestamp),
    )
    log_audit(
        conn,
        "meta_oauth_started",
        "local-user",
        network=provider_id,
        payload={"scopes": META_SCOPES, "redirectUri": config["redirect_uri"]},
    )

    params = {
        "client_id": config["app_id"],
        "redirect_uri": config["redirect_uri"],
        "state": state,
        "response_type": "code",
    }
    if config["login_config_id"]:
        params["config_id"] = config["login_config_id"]
    else:
        params["scope"] = ",".join(META_SCOPES)
    return f"https://www.facebook.com/{meta_graph_version()}/dialog/oauth?{urlencode(params)}"


def exchange_meta_code_for_token(code, redirect_uri):
    config = require_meta_config()
    token_payload = http_json(
        meta_graph_url("/oauth/access_token"),
        data={
            "client_id": config["app_id"],
            "client_secret": config["app_secret"],
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )

    short_token = token_payload.get("access_token")
    if not short_token:
        raise ValueError("Meta did not return an access token.")

    long_lived = http_json(
        meta_graph_url("/oauth/access_token"),
        data={
            "grant_type": "fb_exchange_token",
            "client_id": config["app_id"],
            "client_secret": config["app_secret"],
            "fb_exchange_token": short_token,
        },
    )
    return long_lived if long_lived.get("access_token") else token_payload


def token_expiry(token_payload):
    expires_in = token_payload.get("expires_in")
    if not expires_in:
        return None
    expires_at = datetime.now(timezone.utc).timestamp() + int(expires_in)
    return datetime.fromtimestamp(expires_at, timezone.utc).isoformat()


def store_meta_token(conn, token_payload):
    timestamp = utc_now()
    conn.execute(
        """
        INSERT INTO provider_tokens (
            provider, token_type, access_token, expires_at, raw_json, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(provider) DO UPDATE SET
            token_type = excluded.token_type,
            access_token = excluded.access_token,
            expires_at = excluded.expires_at,
            raw_json = excluded.raw_json,
            updated_at = excluded.updated_at
        """,
        (
            "meta",
            token_payload.get("token_type", "bearer"),
            token_payload["access_token"],
            token_expiry(token_payload),
            json.dumps({key: value for key, value in token_payload.items() if key != "access_token"}),
            timestamp,
            timestamp,
        ),
    )


def discover_meta_accounts(conn, access_token):
    fields = "id,name,access_token,tasks,instagram_business_account{id,username,name,profile_picture_url}"
    accounts = http_json(
        f"{meta_graph_url('/me/accounts')}?{urlencode({'fields': fields, 'access_token': access_token})}"
    )
    timestamp = utc_now()
    saved = []

    for account in accounts.get("data", []):
        instagram_account = account.get("instagram_business_account") or {}
        tasks = account.get("tasks") or []
        conn.execute(
            """
            INSERT INTO meta_accounts (
                page_id, page_name, page_access_token, instagram_business_account_id,
                instagram_username, tasks_json, raw_json, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(page_id) DO UPDATE SET
                page_name = excluded.page_name,
                page_access_token = excluded.page_access_token,
                instagram_business_account_id = excluded.instagram_business_account_id,
                instagram_username = excluded.instagram_username,
                tasks_json = excluded.tasks_json,
                raw_json = excluded.raw_json,
                updated_at = excluded.updated_at
            """,
            (
                account["id"],
                account.get("name", "Unnamed Page"),
                account.get("access_token"),
                instagram_account.get("id"),
                instagram_account.get("username") or instagram_account.get("name"),
                json.dumps(tasks),
                json.dumps({key: value for key, value in account.items() if key != "access_token"}),
                timestamp,
                timestamp,
            ),
        )
        saved.append(account)

    if saved:
        conn.execute(
            "UPDATE networks SET status = 'connected', updated_at = ? WHERE id IN ('instagram', 'facebook')",
            (timestamp,),
        )
    log_audit(
        conn,
        "meta_accounts_discovered",
        "local-user",
        network="meta",
        payload={
            "pages": len(saved),
            "instagramAccounts": sum(
                1 for account in saved if account.get("instagram_business_account")
            ),
        },
    )
    return saved


def complete_meta_oauth(conn, query):
    error = (query.get("error_description") or query.get("error") or [""])[0]
    if error:
        raise ValueError(f"Meta OAuth failed: {error}")

    code = (query.get("code") or [""])[0]
    state = (query.get("state") or [""])[0]
    if not code or not state:
        raise ValueError("Meta OAuth callback is missing code or state.")

    row = conn.execute(
        "SELECT * FROM oauth_states WHERE state = ? AND used_at IS NULL",
        (state,),
    ).fetchone()
    if not row:
        raise ValueError("OAuth state is invalid or already used.")

    token_payload = exchange_meta_code_for_token(code, row["redirect_uri"])
    store_meta_token(conn, token_payload)
    accounts = discover_meta_accounts(conn, token_payload["access_token"])
    conn.execute("UPDATE oauth_states SET used_at = ? WHERE state = ?", (utc_now(), state))
    log_audit(
        conn,
        "meta_oauth_completed",
        "local-user",
        network=row["provider"],
        payload={"pages": len(accounts)},
    )
    return accounts


def latest_meta_discovery(conn):
    token = conn.execute("SELECT * FROM provider_tokens WHERE provider = 'meta'").fetchone()
    if not token:
        raise ValueError("Meta is not connected yet. Start OAuth first.")
    return discover_meta_accounts(conn, token["access_token"])


def html_response(handler, status, title, body):
    content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <style>
      body {{ font-family: system-ui, sans-serif; margin: 0; background: #f5f6f8; color: #17191f; }}
      main {{ max-width: 720px; margin: 12vh auto; background: white; border: 1px solid #d9dee7; border-radius: 8px; padding: 28px; }}
      a {{ color: #234f9a; font-weight: 700; }}
      code {{ background: #eef1f5; border-radius: 6px; padding: 2px 5px; }}
    </style>
  </head>
  <body><main>{body}</main></body>
</html>""".encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(content)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(content)


def legal_page(title, body):
    return f"""
    <h1>{title}</h1>
    {body}
    <p><a href="/">Return to Anaunim</a></p>
    """


def oauth_status(provider_id):
    if provider_id not in CAPABILITY_MATRIX:
        raise ValueError("Unknown provider.")

    capability = CAPABILITY_MATRIX[provider_id]
    return {
        "provider": provider_id,
        "status": "blocked_pending_provider_credentials",
        "message": "OAuth is scaffolded, but this provider needs a real developer app, client credentials, redirect URI, scopes, and review approval before live login can start.",
        "authModel": capability["auth_model"],
        "productionStatus": capability["production_status"],
        "requiredUserInput": capability["required_user_input"],
        "sources": capability["sources"],
    }


class AnaunimHandler(BaseHTTPRequestHandler):
    server_version = "AnaunimHTTP/0.1"

    def log_message(self, format, *args):
        return

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path == "/healthz":
                write_json(self, 200, {"ok": True, "time": utc_now()})
                return
            if path == "/asset-check":
                write_json(
                    self,
                    200,
                    {
                        "index": (ROOT / "index.html").exists(),
                        "css": (ROOT / "styles.css").exists(),
                        "js": (ROOT / "app.js").exists(),
                        "assets": (ROOT / "assets").exists(),
                        "cssContentType": STATIC_CONTENT_TYPES[".css"],
                        "jsContentType": STATIC_CONTENT_TYPES[".js"],
                    },
                )
                return
            if path == "/privacy":
                html_response(
                    self,
                    200,
                    "Privacy Policy",
                    legal_page(
                        "Privacy Policy",
                        """
                        <p>Anaunim is a private social interaction management tool. It stores connected account metadata, interaction records, removal jobs, and audit logs needed to provide the service.</p>
                        <p>Access tokens are stored server-side and are never exposed to the browser. You can request deletion of locally stored data by using the data deletion instructions.</p>
                        <p>This development policy will be replaced with a full production privacy policy before public release.</p>
                        """,
                    ),
                )
                return
            if path == "/data-deletion":
                html_response(
                    self,
                    200,
                    "Data Deletion",
                    legal_page(
                        "Data Deletion",
                        """
                        <p>To delete data associated with your connected Meta account, contact the application operator and request deletion of your Anaunim account data.</p>
                        <p>For local development, stop the service and delete the SQLite database file configured by <code>DATABASE_PATH</code> or <code>data/anaunim.sqlite</code>.</p>
                        <p>This page exists so Meta can verify that data deletion instructions are available during app setup.</p>
                        """,
                    ),
                )
                return
            if path == "/terms":
                html_response(
                    self,
                    200,
                    "Terms",
                    legal_page(
                        "Terms",
                        """
                        <p>Anaunim is currently a development tool. Do not use it for production social account management until provider review, security hardening, and data handling policies are complete.</p>
                        <p>Destructive actions should remain audited and reversible where possible.</p>
                        """,
                    ),
                )
                return
            if path == "/api/bootstrap":
                with open_db() as conn:
                    write_json(self, 200, bootstrap_payload(conn))
                return
            if path == "/api/oauth/start":
                provider_id = (query.get("provider") or [""])[0]
                if provider_id in {"instagram", "facebook", "meta"}:
                    with open_db() as conn:
                        login_url = start_meta_oauth(conn, provider_id)
                        conn.commit()
                    self.send_response(302)
                    self.send_header("Location", login_url)
                    self.send_header("Cache-Control", "no-store")
                    self.end_headers()
                    return
                write_json(self, 200, oauth_status(provider_id))
                return
            if path == "/api/oauth/callback":
                provider_id = (query.get("provider") or [""])[0]
                if provider_id in {"instagram", "facebook", "meta"}:
                    with open_db() as conn:
                        accounts = complete_meta_oauth(conn, query)
                        conn.commit()
                    html_response(
                        self,
                        200,
                        "Meta connected",
                        f"""
                        <h1>Meta connected</h1>
                        <p>Discovered <strong>{len(accounts)}</strong> Facebook Page account(s).</p>
                        <p>You can return to <a href="/">Anaunim</a>. The dashboard will show the Meta connection status.</p>
                        """,
                    )
                    return
                write_json(self, 200, oauth_status(provider_id))
                return
            if path == "/api/meta/status":
                with open_db() as conn:
                    write_json(self, 200, {"meta": meta_status(conn)})
                return
            if path == "/api/meta/accounts":
                with open_db() as conn:
                    accounts = [
                        meta_account_dict(row)
                        for row in conn.execute("SELECT * FROM meta_accounts ORDER BY page_name")
                    ]
                    write_json(self, 200, {"accounts": accounts})
                return
            if path == "/api/capabilities":
                write_json(self, 200, {"capabilities": CAPABILITY_MATRIX})
                return
            if path == "/api/jobs":
                with open_db() as conn:
                    jobs = [
                        job_dict(row)
                        for row in conn.execute(
                            "SELECT * FROM removal_jobs ORDER BY created_at DESC LIMIT 25"
                        )
                    ]
                    write_json(self, 200, {"jobs": jobs})
                return
            if path == "/api/audit":
                with open_db() as conn:
                    audit = [
                        audit_dict(row)
                        for row in conn.execute(
                            "SELECT * FROM audit_log ORDER BY created_at DESC, id DESC LIMIT 50"
                        )
                    ]
                    write_json(self, 200, {"auditLog": audit})
                return

            self.serve_static(path)
        except Exception as exc:
            write_error(self, 500, str(exc))

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = read_json(self)
            with open_db() as conn:
                if path == "/api/sync":
                    results = sync_mock_providers(conn)
                    conn.commit()
                    write_json(self, 200, bootstrap_payload(conn, {"syncResults": results}))
                    return
                if path == "/api/removals":
                    job_id = create_removal_job(conn, payload)
                    conn.commit()
                    job = conn.execute("SELECT * FROM removal_jobs WHERE id = ?", (job_id,)).fetchone()
                    write_json(self, 200, bootstrap_payload(conn, {"job": job_dict(job)}))
                    return
                if path == "/api/removals/undo":
                    job_id = undo_removal_job(conn, payload)
                    conn.commit()
                    job = conn.execute("SELECT * FROM removal_jobs WHERE id = ?", (job_id,)).fetchone()
                    write_json(self, 200, bootstrap_payload(conn, {"job": job_dict(job)}))
                    return
                if path == "/api/accounts/toggle":
                    status = toggle_account(conn, payload)
                    conn.commit()
                    write_json(self, 200, bootstrap_payload(conn, {"accountStatus": status}))
                    return
                if path == "/api/meta/discover":
                    accounts = latest_meta_discovery(conn)
                    conn.commit()
                    write_json(self, 200, bootstrap_payload(conn, {"metaAccounts": len(accounts)}))
                    return
            write_error(self, 404, "Endpoint not found.")
        except ValueError as exc:
            write_error(self, 400, str(exc))
        except Exception as exc:
            write_error(self, 500, str(exc))

    def serve_static(self, request_path):
        clean_path = unquote(request_path.lstrip("/")) or "index.html"
        target = (ROOT / clean_path).resolve()
        root = ROOT.resolve()

        try:
            target.relative_to(root)
        except ValueError:
            write_error(self, 403, "Path is outside the application root.")
            return

        if target.is_dir():
            target = target / "index.html"

        if not target.exists() or not target.is_file():
            write_error(self, 404, "File not found.")
            return

        content = target.read_bytes()
        content_type = STATIC_CONTENT_TYPES.get(
            target.suffix.lower(),
            mimetypes.guess_type(str(target))[0] or "application/octet-stream",
        )
        if target.suffix in {".html", ".js", ".css"}:
            cache_control = "no-store"
        else:
            cache_control = "public, max-age=3600"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", cache_control)
        self.end_headers()
        self.wfile.write(content)


def main():
    parser = argparse.ArgumentParser(description="Run the Anaunim local backend.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=int(os.environ.get("PORT", "5173")), type=int)
    args = parser.parse_args()

    init_db()
    server = ThreadingHTTPServer((args.host, args.port), AnaunimHandler)
    print(f"Anaunim running at http://{args.host}:{args.port}/")
    print(f"SQLite database: {DB_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    main()

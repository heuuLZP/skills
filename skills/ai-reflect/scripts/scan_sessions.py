#!/usr/bin/env python3
"""Normalize recent Claude Code and Codex conversations for ai-reflect."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


IGNORED_CODEX_USER_PREFIXES = (
    "The following is the Codex agent history whose request action you are assessing.",
    "The following is the Codex agent history whose action you are reviewing.",
)


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def text_blocks(content: Any, allowed_types: set[str] | None = None) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""

    allowed = allowed_types or {"text"}
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict) or item.get("type") not in allowed:
            continue
        value = item.get("text")
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    return "\n".join(parts)


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict):
                    yield value
    except OSError:
        return


def append_message(
    messages: list[dict[str, str]], timestamp: datetime | None, role: str, text: str, since: datetime
) -> None:
    if not text or (timestamp is not None and timestamp < since):
        return
    item = {
        "timestamp": timestamp.isoformat() if timestamp else "",
        "role": role,
        "text": text,
    }
    if messages and messages[-1]["role"] == role and messages[-1]["text"] == text:
        return
    messages.append(item)


def parse_claude(path: Path, since: datetime) -> dict[str, Any] | None:
    messages: list[dict[str, str]] = []
    session_id = path.stem
    cwd = ""
    started_at: datetime | None = None

    for record in read_jsonl(path):
        if record.get("isSidechain") is True or record.get("type") not in {"user", "assistant"}:
            continue
        message = record.get("message")
        if not isinstance(message, dict):
            continue
        role = message.get("role")
        if role not in {"user", "assistant"}:
            continue
        origin = record.get("origin")
        if role == "user" and isinstance(origin, dict) and origin.get("kind") not in {None, "human"}:
            continue

        timestamp = parse_timestamp(record.get("timestamp"))
        text = text_blocks(message.get("content"), {"text"})
        append_message(messages, timestamp, role, text, since)
        session_id = str(record.get("sessionId") or session_id)
        cwd = str(record.get("cwd") or cwd)
        if timestamp and (started_at is None or timestamp < started_at):
            started_at = timestamp

    return build_session("claude-code", path, session_id, cwd, started_at, messages)


def parse_codex(path: Path, since: datetime) -> dict[str, Any] | None:
    messages: list[dict[str, str]] = []
    session_id = path.stem
    cwd = ""
    started_at: datetime | None = None

    for record in read_jsonl(path):
        timestamp = parse_timestamp(record.get("timestamp"))
        record_type = record.get("type")
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue

        if record_type == "session_meta":
            session_id = str(payload.get("session_id") or payload.get("id") or session_id)
            cwd = str(payload.get("cwd") or cwd)
            started_at = parse_timestamp(payload.get("timestamp")) or timestamp or started_at
            continue

        if record_type == "event_msg" and payload.get("type") == "user_message":
            text = payload.get("message")
            if isinstance(text, str) and not text.startswith(IGNORED_CODEX_USER_PREFIXES):
                append_message(messages, timestamp, "user", text.strip(), since)
            continue

        if record_type == "response_item" and payload.get("type") == "message" and payload.get("role") == "assistant":
            text = text_blocks(payload.get("content"), {"output_text", "text"})
            append_message(messages, timestamp, "assistant", text, since)

    return build_session("codex", path, session_id, cwd, started_at, messages)


def build_session(
    source: str,
    path: Path,
    session_id: str,
    cwd: str,
    started_at: datetime | None,
    messages: list[dict[str, str]],
) -> dict[str, Any] | None:
    if not messages:
        return None
    original_count = len(messages)
    return {
        "source": source,
        "id": session_id,
        "path": str(path),
        "cwd": cwd,
        "startedAt": started_at.isoformat() if started_at else "",
        "messageCount": original_count,
        "messages": sample_messages(messages),
    }


def sample_messages(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    if len(messages) <= 200:
        return messages
    middle = messages[10:-10]
    indexes = [round(index * (len(middle) - 1) / 19) for index in range(20)]
    return messages[:10] + [middle[index] for index in indexes] + messages[-10:]


def scan(root: Path, source: str, since: datetime) -> list[dict[str, Any]]:
    parser = parse_claude if source == "claude-code" else parse_codex
    sessions: list[dict[str, Any]] = []
    if not root.exists():
        return sessions
    for path in root.rglob("*.jsonl"):
        session = parser(path, since)
        if session:
            sessions.append(session)
    return sessions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--max-sessions", type=int, default=20)
    parser.add_argument("--claude-root", type=Path, default=Path.home() / ".claude/projects")
    parser.add_argument("--codex-root", type=Path, default=Path.home() / ".codex/sessions")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--now", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.days <= 0 or args.max_sessions <= 0:
        parser.error("--days and --max-sessions must be positive")

    now = parse_timestamp(args.now) if args.now else datetime.now(timezone.utc)
    if now is None:
        parser.error("--now must be an ISO-8601 timestamp")
    since = now - timedelta(days=args.days)

    sessions = scan(args.claude_root.expanduser(), "claude-code", since)
    sessions += scan(args.codex_root.expanduser(), "codex", since)
    sessions.sort(key=lambda item: item["messageCount"], reverse=True)
    sessions = sessions[: args.max_sessions]

    payload = {
        "generatedAt": now.isoformat(),
        "since": since.isoformat(),
        "sources": {
            "claude-code": sum(item["source"] == "claude-code" for item in sessions),
            "codex": sum(item["source"] == "codex" for item in sessions),
        },
        "sessions": sessions,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

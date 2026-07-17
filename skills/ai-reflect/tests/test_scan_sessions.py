import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "scan_sessions.py"
SPEC = importlib.util.spec_from_file_location("scan_sessions", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


class ScanSessionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.since = datetime(2026, 7, 10, tzinfo=timezone.utc)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_parses_human_claude_messages_and_excludes_sidechains(self) -> None:
        path = self.root / "claude" / "session.jsonl"
        write_jsonl(
            path,
            [
                {
                    "timestamp": "2026-07-15T01:00:00Z",
                    "type": "user",
                    "origin": {"kind": "human"},
                    "message": {"role": "user", "content": "帮我分析这个设计"},
                    "sessionId": "claude-1",
                    "cwd": "/tmp/project",
                },
                {
                    "timestamp": "2026-07-15T01:01:00Z",
                    "type": "assistant",
                    "message": {"role": "assistant", "content": [{"type": "text", "text": "先看边界。"}]},
                    "sessionId": "claude-1",
                },
                {
                    "timestamp": "2026-07-15T01:02:00Z",
                    "type": "user",
                    "isSidechain": True,
                    "message": {"role": "user", "content": "子代理任务"},
                },
            ],
        )

        session = MODULE.parse_claude(path, self.since)

        self.assertEqual(session["id"], "claude-1")
        self.assertEqual([item["role"] for item in session["messages"]], ["user", "assistant"])
        self.assertNotIn("子代理", json.dumps(session, ensure_ascii=False))

    def test_parses_codex_messages_and_excludes_internal_approval_transcript(self) -> None:
        path = self.root / "codex" / "session.jsonl"
        write_jsonl(
            path,
            [
                {
                    "timestamp": "2026-07-15T02:00:00Z",
                    "type": "session_meta",
                    "payload": {"session_id": "codex-1", "cwd": "/tmp/project"},
                },
                {
                    "timestamp": "2026-07-15T02:01:00Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "请比较两个方案"},
                },
                {
                    "timestamp": "2026-07-15T02:02:00Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "content": [{"type": "output_text", "text": "先列出约束。"}],
                    },
                },
                {
                    "timestamp": "2026-07-15T02:03:00Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "The following is the Codex agent history whose request action you are assessing. hidden",
                    },
                },
            ],
        )

        session = MODULE.parse_codex(path, self.since)

        self.assertEqual(session["id"], "codex-1")
        self.assertEqual([item["text"] for item in session["messages"]], ["请比较两个方案", "先列出约束。"])

    def test_filters_old_messages_and_samples_large_sessions(self) -> None:
        messages = [
            {"timestamp": "", "role": "user", "text": f"message-{index}"}
            for index in range(220)
        ]
        sampled = MODULE.sample_messages(messages)

        self.assertEqual(len(sampled), 40)
        self.assertEqual(sampled[0]["text"], "message-0")
        self.assertEqual(sampled[-1]["text"], "message-219")


if __name__ == "__main__":
    unittest.main()

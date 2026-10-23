"""Transactional provenance ledger with revision guards."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from server.graph import DependencyGraph
from server.paths import DEFAULT_DB, FIXTURE_CASE


class LedgerError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_proposal(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class CaseStore:
    def __init__(self, db_path: Path = DEFAULT_DB) -> None:
        self.db_path = db_path
        self.manifest_path = FIXTURE_CASE / "manifest.json"
        self._manifest: Dict[str, Any] = (
            json.loads(self.manifest_path.read_text())
            if self.manifest_path.exists()
            else {}
        )
        self._connect()

    def _connect(self) -> None:
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")

    @contextmanager
    def _tx(self):
        try:
            yield
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (
              key TEXT PRIMARY KEY,
              value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS documents (
              id TEXT PRIMARY KEY,
              title TEXT NOT NULL,
              version INTEGER NOT NULL,
              role TEXT,
              content_hash TEXT NOT NULL,
              content TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS assertions (
              id TEXT PRIMARY KEY,
              key TEXT NOT NULL,
              value TEXT NOT NULL,
              document_id TEXT NOT NULL,
              status TEXT NOT NULL,
              coverage TEXT NOT NULL,
              superseded_by TEXT,
              conflict_group TEXT
            );
            CREATE TABLE IF NOT EXISTS assessment_deps (
              assessment_id TEXT NOT NULL,
              dep_id TEXT NOT NULL,
              PRIMARY KEY (assessment_id, dep_id)
            );
            CREATE TABLE IF NOT EXISTS assessments (
              id TEXT PRIMARY KEY,
              title TEXT NOT NULL,
              compute TEXT NOT NULL,
              status TEXT NOT NULL,
              value TEXT,
              explanation TEXT
            );
            CREATE TABLE IF NOT EXISTS checklist (
              id TEXT PRIMARY KEY,
              label TEXT NOT NULL,
              assertion_id TEXT NOT NULL,
              blocks_ready INTEGER NOT NULL DEFAULT 0,
              done INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS proposals (
              id TEXT PRIMARY KEY,
              created_at TEXT NOT NULL,
              actor_role TEXT NOT NULL,
              case_revision INTEGER NOT NULL,
              proposal_hash TEXT NOT NULL,
              from_assertion_id TEXT NOT NULL,
              to_assertion_id TEXT NOT NULL,
              status TEXT NOT NULL,
              payload_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS events (
              seq INTEGER PRIMARY KEY AUTOINCREMENT,
              created_at TEXT NOT NULL,
              event_type TEXT NOT NULL,
              case_revision INTEGER NOT NULL,
              actor_role TEXT,
              payload_json TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    def reset_from_fixture(self) -> None:
        self._manifest = json.loads(self.manifest_path.read_text())
        case_dir = self.manifest_path.parent
        with self._tx():
            for table in (
                "events",
                "proposals",
                "checklist",
                "assessment_deps",
                "assessments",
                "assertions",
                "documents",
                "meta",
            ):
                self.conn.execute(f"DELETE FROM {table}")

            self.conn.execute(
                "INSERT INTO meta(key, value) VALUES ('case_revision', '0')"
            )
            self.conn.execute(
                "INSERT INTO meta(key, value) VALUES ('case_id', ?)",
                (self._manifest["case_id"],),
            )
            self.conn.execute(
                "INSERT INTO meta(key, value) VALUES ('program_threshold', ?)",
                (str(self._manifest["program_threshold"]),),
            )
            active_income = self._manifest["initial_active_income_assertion"]

            for doc in self._manifest["documents"]:
                content = (case_dir / doc["file"]).read_text()
                content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
                self.conn.execute(
                    """
                    INSERT INTO documents(id, title, version, role, content_hash, content)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        doc["id"],
                        doc["title"],
                        doc["version"],
                        doc.get("role"),
                        content_hash,
                        content,
                    ),
                )

            for a in self._manifest["assertions"]:
                status = "current"
                self.conn.execute(
                    """
                    INSERT INTO assertions(id, key, value, document_id, status, coverage, conflict_group)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        a["id"],
                        a["key"],
                        a["value"],
                        a["document_id"],
                        status,
                        a.get("coverage", "known"),
                        a.get("conflict_group"),
                    ),
                )

            for asm in self._manifest["assessments"]:
                deps = list(asm["depends_on"])
                if asm["id"] == "A1":
                    deps = [active_income]
                self.conn.execute(
                    """
                    INSERT INTO assessments(id, title, compute, status, value, explanation)
                    VALUES (?, ?, ?, 'current', NULL, NULL)
                    """,
                    (asm["id"], asm["title"], asm["compute"]),
                )
                for d in deps:
                    self.conn.execute(
                        "INSERT INTO assessment_deps(assessment_id, dep_id) VALUES (?, ?)",
                        (asm["id"], d),
                    )

            for chk in self._manifest["checklist"]:
                self.conn.execute(
                    """
                    INSERT INTO checklist(id, label, assertion_id, blocks_ready, done)
                    VALUES (?, ?, ?, ?, 0)
                    """,
                    (
                        chk["id"],
                        chk["label"],
                        chk["assertion_id"],
                        1 if chk.get("blocks_ready") else 0,
                    ),
                )

            self._recompute_all_assessments()
            self._append_event(
                "case_reset",
                0,
                None,
                {"case_id": self._manifest["case_id"]},
            )

    def _meta_int(self, key: str) -> int:
        row = self.conn.execute(
            "SELECT value FROM meta WHERE key = ?", (key,)
        ).fetchone()
        if not row:
            return 0
        return int(row["value"])

    def _set_revision(self, rev: int) -> None:
        self.conn.execute(
            "UPDATE meta SET value = ? WHERE key = 'case_revision'", (str(rev),)
        )

    def _append_event(
        self,
        event_type: str,
        revision: int,
        actor_role: Optional[str],
        payload: Dict[str, Any],
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO events(created_at, event_type, case_revision, actor_role, payload_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (_utc_now(), event_type, revision, actor_role, json.dumps(payload)),
        )

    def _assessment_deps_map(self) -> Dict[str, List[str]]:
        rows = self.conn.execute(
            "SELECT assessment_id, dep_id FROM assessment_deps"
        ).fetchall()
        deps: Dict[str, List[str]] = {}
        for r in rows:
            deps.setdefault(r["assessment_id"], []).append(r["dep_id"])
        return deps

    def _get_assertion(self, aid: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM assertions WHERE id = ?", (aid,)
        ).fetchone()
        if not row:
            raise LedgerError("not_found", f"Assertion {aid} not found")
        return row

    def _recompute_all_assessments(self) -> None:
        order = DependencyGraph(self._assessment_deps_map()).topological_order()
        threshold = self._meta_int("program_threshold") or int(
            self._manifest.get("program_threshold", 2500)
        )
        for aid in order:
            self._recompute_assessment(aid, threshold)

    def _recompute_assessment(self, aid: str, threshold: int) -> None:
        row = self.conn.execute(
            "SELECT * FROM assessments WHERE id = ?", (aid,)
        ).fetchone()
        if not row:
            return
        compute = row["compute"]
        deps = [
            r["dep_id"]
            for r in self.conn.execute(
                "SELECT dep_id FROM assessment_deps WHERE assessment_id = ?",
                (aid,),
            ).fetchall()
        ]

        if compute == "income_from_assertion":
            assert_id = deps[0] if deps else None
            if not assert_id:
                self._set_assessment(aid, "unresolved", None, "No income assertion linked")
                return
            a = self._get_assertion(assert_id)
            if a["status"] != "current" or a["coverage"] == "unknown":
                self._set_assessment(
                    aid, "stale", None, f"Source assertion {assert_id} is not current"
                )
                return
            self._set_assessment(
                aid,
                "current",
                a["value"],
                f"Taken from assertion {assert_id} (document {a['document_id']})",
            )
            return

        if compute == "threshold_check":
            a1 = self.conn.execute(
                "SELECT value, status FROM assessments WHERE id = 'A1'"
            ).fetchone()
            if not a1 or a1["status"] != "current" or not a1["value"]:
                self._set_assessment(
                    aid, "stale", None, "Income answer not current; threshold not recomputed"
                )
                return
            income = float(a1["value"])
            within = "yes" if income <= threshold else "no"
            self._set_assessment(
                aid,
                "current",
                within,
                f"Income {income} compared to fictional threshold {threshold}",
            )
            return

        if compute == "unknown_coverage":
            assert_id = deps[0]
            a = self._get_assertion(assert_id)
            if a["coverage"] == "unknown":
                self._set_assessment(
                    aid,
                    "unresolved",
                    None,
                    "Dependency coverage marked unknown in authored graph",
                )
                return
            self._set_assessment(aid, "current", a["value"], "Coverage known")

    def _set_assessment(
        self, aid: str, status: str, value: Optional[str], explanation: str
    ) -> None:
        self.conn.execute(
            """
            UPDATE assessments SET status = ?, value = ?, explanation = ?
            WHERE id = ?
            """,
            (status, value, explanation, aid),
        )

    def _conflicts(self) -> List[str]:
        groups: Dict[str, List[str]] = {}
        for r in self.conn.execute(
            "SELECT conflict_group, value FROM assertions WHERE conflict_group IS NOT NULL AND status = 'current'"
        ).fetchall():
            groups.setdefault(r["conflict_group"], []).append(r["value"])
        out = []
        for g, vals in groups.items():
            if len(set(vals)) > 1:
                out.append(g)
        return out

    def _ready_to_export(self) -> bool:
        if self._conflicts():
            return False
        unresolved = self.conn.execute(
            "SELECT COUNT(*) AS c FROM assessments WHERE status IN ('stale', 'unresolved')"
        ).fetchone()["c"]
        if unresolved:
            return False
        blocking = self.conn.execute(
            "SELECT COUNT(*) AS c FROM checklist WHERE blocks_ready = 1 AND done = 0"
        ).fetchone()["c"]
        return blocking == 0

    def get_case_view(self) -> Dict[str, Any]:
        rev = self._meta_int("case_revision")
        case_id = self.conn.execute(
            "SELECT value FROM meta WHERE key = 'case_id'"
        ).fetchone()["value"]
        docs = [
            {
                "id": r["id"],
                "title": r["title"],
                "version": r["version"],
                "role": r["role"],
                "content_preview": r["content"][:200],
            }
            for r in self.conn.execute("SELECT * FROM documents").fetchall()
        ]
        assertions = [
            {
                "id": r["id"],
                "key": r["key"],
                "value": r["value"],
                "document_id": r["document_id"],
                "status": r["status"],
                "coverage": r["coverage"],
                "superseded_by": r["superseded_by"],
            }
            for r in self.conn.execute("SELECT * FROM assertions").fetchall()
        ]
        assessments = []
        for r in self.conn.execute("SELECT * FROM assessments").fetchall():
            deps = [
                x["dep_id"]
                for x in self.conn.execute(
                    "SELECT dep_id FROM assessment_deps WHERE assessment_id = ?",
                    (r["id"],),
                ).fetchall()
            ]
            assessments.append(
                {
                    "id": r["id"],
                    "title": r["title"],
                    "status": r["status"],
                    "value": r["value"],
                    "explanation": r["explanation"],
                    "depends_on": deps,
                }
            )
        checklist = [
            dict(r)
            for r in self.conn.execute("SELECT * FROM checklist").fetchall()
        ]
        ledger_tail = [
            {
                "seq": r["seq"],
                "event_type": r["event_type"],
                "case_revision": r["case_revision"],
                "created_at": r["created_at"],
                "payload": json.loads(r["payload_json"]),
            }
            for r in self.conn.execute(
                "SELECT * FROM events ORDER BY seq DESC LIMIT 10"
            ).fetchall()
        ]
        pending = self.conn.execute(
            "SELECT id FROM proposals WHERE status = 'pending' ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        return {
            "case_id": case_id,
            "title": self._manifest.get("title", "Case"),
            "case_revision": rev,
            "documents": docs,
            "assertions": assertions,
            "assessments": assessments,
            "checklist": checklist,
            "conflicts": self._conflicts(),
            "ready_to_export": self._ready_to_export(),
            "active_proposal_id": pending["id"] if pending else None,
            "ledger_tail": list(reversed(ledger_tail)),
        }

    def inspect_source(self, assessment_id: str) -> Dict[str, Any]:
        deps = [
            r["dep_id"]
            for r in self.conn.execute(
                "SELECT dep_id FROM assessment_deps WHERE assessment_id = ?",
                (assessment_id,),
            ).fetchall()
        ]
        sources = []
        for d in deps:
            if d.startswith("assert_"):
                a = self._get_assertion(d)
                doc = self.conn.execute(
                    "SELECT title, content_hash FROM documents WHERE id = ?",
                    (a["document_id"],),
                ).fetchone()
                sources.append(
                    {
                        "assertion_id": d,
                        "key": a["key"],
                        "value": a["value"],
                        "document_id": a["document_id"],
                        "document_title": doc["title"],
                        "content_hash": doc["content_hash"],
                    }
                )
        asm = self.conn.execute(
            "SELECT title, value, status FROM assessments WHERE id = ?",
            (assessment_id,),
        ).fetchone()
        return {
            "assessment_id": assessment_id,
            "assessment_title": asm["title"] if asm else None,
            "current_value": asm["value"] if asm else None,
            "status": asm["status"] if asm else None,
            "sources": sources,
        }

    def propose_income_correction(
        self,
        role: str,
        to_document_id: Optional[str] = None,
        custom_income: Optional[str] = None,
        expected_revision: Optional[int] = None,
    ) -> Dict[str, Any]:
        rev = self._meta_int("case_revision")
        if expected_revision is not None and expected_revision != rev:
            raise LedgerError(
                "stale_revision",
                f"Case revision is {rev}, proposal expected {expected_revision}",
            )
        cm = self._manifest["correction_map"]
        from_id = cm["from_assertion"]
        to_id = cm["to_assertion"]
        if to_document_id == "doc_payslip_aug":
            raise LedgerError("invalid", "Cannot correct toward older payslip in demo")
        to_assert = self._get_assertion(to_id)
        new_value = custom_income if custom_income else to_assert["value"]

        graph = DependencyGraph(self._assessment_deps_map())
        affected = sorted(graph.dependent_closure([from_id]))

        payload = {
            "from_assertion_id": from_id,
            "to_assertion_id": to_id,
            "from_document_id": cm["from_document"],
            "to_document_id": cm["to_document"],
            "new_income_value": new_value,
            "affected_assessment_ids": affected,
            "case_revision": rev,
        }
        proposal_hash = _hash_proposal(payload)
        pid = str(uuid.uuid4())
        with self._tx():
            self.conn.execute(
                "UPDATE proposals SET status = 'cancelled' WHERE status = 'pending'"
            )
            self.conn.execute(
                """
                INSERT INTO proposals(
                  id, created_at, actor_role, case_revision, proposal_hash,
                  from_assertion_id, to_assertion_id, status, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
                """,
                (
                    pid,
                    _utc_now(),
                    role,
                    rev,
                    proposal_hash,
                    from_id,
                    to_id,
                    json.dumps(payload),
                ),
            )
        return {
            "proposal_id": pid,
            "proposal_hash": proposal_hash,
            "case_revision": rev,
            **payload,
        }

    def confirm_proposal(self, proposal_id: str, role: str) -> Dict[str, Any]:
        if role != "applicant":
            raise LedgerError("forbidden", "Only the simulated applicant can confirm")
        row = self.conn.execute(
            "SELECT * FROM proposals WHERE id = ?", (proposal_id,)
        ).fetchone()
        if not row:
            raise LedgerError("not_found", "Proposal not found")
        if row["status"] != "pending":
            raise LedgerError("invalid", f"Proposal is {row['status']}")
        rev = self._meta_int("case_revision")
        if row["case_revision"] != rev:
            raise LedgerError(
                "stale_revision",
                "Proposal was created at an older case revision",
            )
        payload = json.loads(row["payload_json"])
        if _hash_proposal(payload) != row["proposal_hash"]:
            raise LedgerError("hash_mismatch", "Proposal contents changed; reconfirm required")

        from_id = row["from_assertion_id"]
        to_id = row["to_assertion_id"]
        new_value = payload["new_income_value"]
        graph = DependencyGraph(self._assessment_deps_map())
        affected = sorted(graph.dependent_closure([from_id]))

        with self._tx():
            new_rev = rev + 1
            self.conn.execute(
                "UPDATE assertions SET status = 'superseded', superseded_by = ? WHERE id = ?",
                (to_id, from_id),
            )
            self.conn.execute(
                "UPDATE assertions SET status = 'current', value = ? WHERE id = ?",
                (new_value, to_id),
            )
            self.conn.execute(
                "DELETE FROM assessment_deps WHERE assessment_id = 'A1' AND dep_id = ?",
                (from_id,),
            )
            self.conn.execute(
                "INSERT OR IGNORE INTO assessment_deps(assessment_id, dep_id) VALUES ('A1', ?)",
                (to_id,),
            )
            for aid in affected:
                self.conn.execute(
                    "UPDATE assessments SET status = 'stale' WHERE id = ?",
                    (aid,),
                )
            self._recompute_all_assessments()
            self.conn.execute(
                "UPDATE proposals SET status = 'confirmed' WHERE id = ?",
                (proposal_id,),
            )
            self.conn.execute(
                "UPDATE checklist SET done = 1 WHERE id = 'chk_income'"
            )
            self._set_revision(new_rev)
            self._append_event(
                "correction_confirmed",
                new_rev,
                role,
                {
                    "proposal_id": proposal_id,
                    "from_assertion_id": from_id,
                    "to_assertion_id": to_id,
                    "new_income_value": new_value,
                    "affected_assessment_ids": affected,
                },
            )

        return {
            "case_revision": new_rev,
            "affected_assessment_ids": affected,
            "new_income_value": new_value,
        }

    def cancel_proposal(self, proposal_id: str) -> None:
        with self._tx():
            self.conn.execute(
                "UPDATE proposals SET status = 'cancelled' WHERE id = ? AND status = 'pending'",
                (proposal_id,),
            )

    def export_receipt(self) -> Dict[str, Any]:
        view = self.get_case_view()
        events = [
            dict(r)
            for r in self.conn.execute(
                "SELECT seq, event_type, case_revision, created_at, payload_json FROM events ORDER BY seq"
            ).fetchall()
        ]
        for e in events:
            e["payload"] = json.loads(e["payload_json"])
            del e["payload_json"]
        return {
            "exported_at": _utc_now(),
            "case_revision": view["case_revision"],
            "ready_to_export": view["ready_to_export"],
            "assessments": view["assessments"],
            "assertions": view["assertions"],
            "conflicts": view["conflicts"],
            "checklist": view["checklist"],
            "ledger_events": events,
            "revision_receipt": {
                "message": "Handoff packet with provenance and unresolved items",
                "simulated_roles_only": True,
            },
        }

    def try_cycle_edge(self) -> Tuple[bool, str]:
        """Demo-only: attempt to add A2 -> A1 dependency (would cycle)."""
        if DependencyGraph(self._assessment_deps_map()).would_create_cycle("A2", "A1"):
            return False, "Would create assessment dependency cycle"
        return True, "ok"

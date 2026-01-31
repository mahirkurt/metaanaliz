from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ._io import append_jsonl, read_json, write_json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Paths:
    logs_dir: Path

    @property
    def prisma_counts(self) -> Path:
        return self.logs_dir / "prisma_counts.json"

    @property
    def audit_log(self) -> Path:
        return self.logs_dir / "audit_log.jsonl"

    @property
    def screening_log(self) -> Path:
        return self.logs_dir / "screening_log.jsonl"

    @property
    def record_map(self) -> Path:
        return self.logs_dir / "record_map.jsonl"

    @property
    def dedup_report(self) -> Path:
        return self.logs_dir / "dedup_report.json"

    @property
    def protocol_changes(self) -> Path:
        return self.logs_dir / "protocol_changes.csv"


def ensure_prisma_structure(prisma_obj: Dict[str, Any]) -> Dict[str, Any]:
    # Eğer dosya şablonsuz/boşsa minimum iskelet yarat.
    if "prisma" not in prisma_obj:
        prisma_obj["prisma"] = {}
    prisma = prisma_obj["prisma"]
    prisma.setdefault("identification", {}).setdefault("records_identified", 0)
    prisma.setdefault("identification", {}).setdefault(
        "records_removed_before_screening", {"duplicates": 0, "other_reasons": 0}
    )
    prisma.setdefault("screening", {}).setdefault("records_screened", 0)
    prisma.setdefault("screening", {}).setdefault("records_excluded", 0)
    prisma.setdefault("eligibility", {}).setdefault("reports_sought_for_retrieval", 0)
    prisma.setdefault("eligibility", {}).setdefault("reports_not_retrieved", 0)
    prisma.setdefault("eligibility", {}).setdefault("reports_assessed_for_eligibility", 0)
    prisma.setdefault("eligibility", {}).setdefault("reports_excluded", [])
    prisma.setdefault("included", {}).setdefault("studies_included_in_review", 0)
    prisma.setdefault("included", {}).setdefault("reports_included_in_review", 0)
    prisma_obj.setdefault("updated_at", None)
    return prisma_obj


def load_prisma(paths: Paths) -> Dict[str, Any]:
    return ensure_prisma_structure(read_json(paths.prisma_counts))


def save_prisma(paths: Paths, prisma_obj: Dict[str, Any]) -> None:
    prisma_obj["prisma"]["updated_at"] = utc_now_iso() if "prisma" in prisma_obj else utc_now_iso()
    if "prisma" in prisma_obj:
        prisma_obj["prisma"]["updated_at"] = utc_now_iso()
    write_json(paths.prisma_counts, prisma_obj)


def cmd_prisma_set(args: argparse.Namespace) -> None:
    paths = Paths(Path(args.logs_dir))
    obj = load_prisma(paths)
    section, key = args.field.split(".", 1)
    if section not in obj["prisma"]:
        raise SystemExit(f"Bilinmeyen bölüm: {section}")
    # nested key support for a single level deeper
    target = obj["prisma"][section]
    if "." in key:
        k1, k2 = key.split(".", 1)
        if k1 not in target or not isinstance(target[k1], dict):
            target[k1] = {}
        target[k1][k2] = args.value
    else:
        target[key] = args.value
    save_prisma(paths, obj)


def cmd_prisma_add_excluded(args: argparse.Namespace) -> None:
    paths = Paths(Path(args.logs_dir))
    obj = load_prisma(paths)
    excluded: List[Dict[str, Any]] = obj["prisma"]["eligibility"].get("reports_excluded", [])
    excluded.append({"reason": args.reason, "n": args.n})
    obj["prisma"]["eligibility"]["reports_excluded"] = excluded
    save_prisma(paths, obj)


def cmd_audit_append(args: argparse.Namespace) -> None:
    paths = Paths(Path(args.logs_dir))
    payload: Dict[str, Any] = json.loads(args.payload_json) if args.payload_json else {}
    evidence_pointer: Dict[str, Any] = json.loads(args.evidence_json) if args.evidence_json else {}
    event = {
        "timestamp": args.timestamp or utc_now_iso(),
        "actor": args.actor,
        "action": args.action,
        "record_id": args.record_id,
        "payload": payload,
        "evidence_pointer": evidence_pointer,
        "notes": args.notes or "",
    }
    append_jsonl(paths.audit_log, event)


def cmd_screening_append(args: argparse.Namespace) -> None:
    paths = Paths(Path(args.logs_dir))
    reasons = [r.strip() for r in (args.reasons or "").split("|") if r.strip()]
    if args.decision == "exclude" and not reasons:
        raise SystemExit("exclude kararı için en az bir reason gir (örn. --reasons 'population mismatch|review')")
    event = {
        "record_id": args.record_id,
        "source": args.source,
        "stage": args.stage,
        "decision": args.decision,
        "reasons": reasons,
        "reviewer": args.reviewer,
        "timestamp": args.timestamp or utc_now_iso(),
        "notes": args.notes or "",
    }
    append_jsonl(paths.screening_log, event)


def cmd_protocol_change_append(args: argparse.Namespace) -> None:
    paths = Paths(Path(args.logs_dir))
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    # CSV yoksa header yaz.
    if not paths.protocol_changes.exists():
        paths.protocol_changes.write_text(
            "timestamp,changed_by,section,old_value,new_value,reason,impact_assessment,approved_by\n",
            encoding="utf-8",
        )

    row = {
        "timestamp": args.timestamp or utc_now_iso(),
        "changed_by": args.changed_by,
        "section": args.section,
        "old_value": args.old_value or "",
        "new_value": args.new_value or "",
        "reason": args.reason or "",
        "impact_assessment": args.impact_assessment or "",
        "approved_by": args.approved_by or "",
    }

    with paths.protocol_changes.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "changed_by",
                "section",
                "old_value",
                "new_value",
                "reason",
                "impact_assessment",
                "approved_by",
            ],
        )
        writer.writerow(row)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.prisma_log",
        description="logs/ altındaki PRISMA/audit/screening/protocol log dosyalarını doldurmak için küçük CLI.",
    )
    p.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")

    sub = p.add_subparsers(dest="cmd", required=True)

    # PRISMA: set
    ps = sub.add_parser("prisma-set", help="prisma_counts.json içinde bir sayacı set et")
    ps.add_argument(
        "--field",
        required=True,
        help=(
            "Alan yolu. Örn: 'screening.records_screened' veya "
            "'identification.records_removed_before_screening.duplicates'"
        ),
    )
    ps.add_argument("--value", required=True, type=int)
    ps.set_defaults(func=cmd_prisma_set)

    # PRISMA: add excluded reason
    pe = sub.add_parser("prisma-add-excluded", help="eligibility.reports_excluded listesine reason+n ekle")
    pe.add_argument("--reason", required=True)
    pe.add_argument("--n", required=True, type=int)
    pe.set_defaults(func=cmd_prisma_add_excluded)

    # Audit
    a = sub.add_parser("audit-append", help="audit_log.jsonl'e event append et")
    a.add_argument("--timestamp", default=None)
    a.add_argument("--actor", default="agent")
    a.add_argument("--action", required=True)
    a.add_argument("--record-id", required=True)
    a.add_argument("--payload-json", default=None, help="JSON string")
    a.add_argument("--evidence-json", default=None, help="JSON string")
    a.add_argument("--notes", default=None)
    a.set_defaults(func=cmd_audit_append)

    # Screening
    s = sub.add_parser("screening-append", help="screening_log.jsonl'e karar append et")
    s.add_argument("--record-id", required=True)
    s.add_argument("--source", required=True)
    s.add_argument("--stage", required=True, choices=["title_abstract", "full_text"])
    s.add_argument("--decision", required=True, choices=["include", "exclude", "maybe"])
    s.add_argument("--reasons", default=None, help="'reason1|reason2' formatında")
    s.add_argument("--reviewer", default="agent")
    s.add_argument("--timestamp", default=None)
    s.add_argument("--notes", default=None)
    s.set_defaults(func=cmd_screening_append)

    # Protocol changes
    pc = sub.add_parser("protocol-change-append", help="protocol_changes.csv'e satır ekle")
    pc.add_argument("--timestamp", default=None)
    pc.add_argument("--changed-by", default="agent")
    pc.add_argument("--section", required=True)
    pc.add_argument("--old-value", default=None)
    pc.add_argument("--new-value", default=None)
    pc.add_argument("--reason", default=None)
    pc.add_argument("--impact-assessment", default=None)
    pc.add_argument("--approved-by", default=None)
    pc.set_defaults(func=cmd_protocol_change_append)

    return p


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

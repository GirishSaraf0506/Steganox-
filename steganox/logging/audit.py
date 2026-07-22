"""
Audit logging with tamper-evident hash chaining.
Each log entry includes a SHA-256 hash of the previous entry.
"""

import hashlib
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass
class AuditEntry:
    timestamp: str
    action: str  # "embed" | "extract" | "failed"
    image_hash: str
    status: str  # "success" | "failure"
    detail: str
    prev_hash: str
    entry_hash: str = ""


class AuditLogger:
    def __init__(self, log_path: str = "audit.log"):
        self.log_path = log_path
        self._prev_hash = "0" * 64

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
            if lines:
                last = json.loads(lines[-1])
                self._prev_hash = last.get("entry_hash", "0" * 64)

    def log(self, action: str, image_hash: str, status: str, detail: str = ""):
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            action=action,
            image_hash=image_hash,
            status=status,
            detail=detail,
            prev_hash=self._prev_hash,
        )
        raw = json.dumps(
            {k: v for k, v in asdict(entry).items() if k != "entry_hash"},
            sort_keys=True,
        )
        entry.entry_hash = hashlib.sha256(raw.encode()).hexdigest()
        self._prev_hash = entry.entry_hash

        with open(self.log_path, "a") as f:
            f.write(json.dumps(asdict(entry)) + "\n")

    def verify_integrity(self) -> bool:
        """Verify the audit log has not been tampered with."""
        if not os.path.exists(self.log_path):
            return True
        prev = "0" * 64
        with open(self.log_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                if entry.get("prev_hash") != prev:
                    return False
                raw = json.dumps(
                    {k: v for k, v in entry.items() if k != "entry_hash"},
                    sort_keys=True,
                )
                expected = hashlib.sha256(raw.encode()).hexdigest()
                if entry.get("entry_hash") != expected:
                    return False
                prev = entry["entry_hash"]
        return True

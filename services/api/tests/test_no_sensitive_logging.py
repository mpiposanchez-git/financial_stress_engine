from __future__ import annotations

import re
from pathlib import Path


def test_no_sensitive_logging_patterns_in_api_app() -> None:
    app_dir = Path(__file__).resolve().parents[1] / "app"

    checks: list[tuple[str, re.Pattern[str]]] = [
        ("await request.body()", re.compile(r"await\s+request\.body\s*\(", re.IGNORECASE)),
        ("request.json()", re.compile(r"\brequest\.json\s*\(", re.IGNORECASE)),
        (
            "logger call containing Authorization/Bearer",
            re.compile(
                r"logger\.(?:debug|info|warning|error|exception|critical)\s*\([^\n]*(?:Authorization|Bearer)",
                re.IGNORECASE,
            ),
        ),
    ]

    offenders: list[str] = []
    for file_path in sorted(app_dir.rglob("*.py")):
        content = file_path.read_text(encoding="utf-8")
        rel_path = file_path.relative_to(app_dir.parent)

        for label, pattern in checks:
            for match in pattern.finditer(content):
                line_no = content.count("\n", 0, match.start()) + 1
                offenders.append(f"{rel_path}:{line_no} matched '{label}' via /{pattern.pattern}/")

    assert not offenders, (
        "Sensitive logging/body-access patterns detected in API code:\n"
        + "\n".join(f"- {item}" for item in offenders)
    )

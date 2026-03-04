from __future__ import annotations

from pathlib import Path


def test_no_request_body_logging_patterns_in_api_app() -> None:
    app_dir = Path(__file__).resolve().parents[1] / "app"
    py_files = app_dir.rglob("*.py")

    forbidden_patterns = (
        "request.body(",
        "request.json(",
        "await request.body(",
        "await request.json(",
    )

    offenders: list[str] = []
    for file_path in py_files:
        content = file_path.read_text(encoding="utf-8")
        lowered = content.lower()

        for pattern in forbidden_patterns:
            if pattern.lower() in lowered:
                offenders.append(f"{file_path.name}: contains '{pattern}'")

        for line in content.splitlines():
            lowered_line = line.lower()
            is_log_line = "logger." in lowered_line or "logging." in lowered_line or "print(" in lowered_line
            if is_log_line and ("authorization" in lowered_line or "bearer" in lowered_line or "token" in lowered_line):
                offenders.append(f"{file_path.name}: potentially sensitive log line '{line.strip()}'")

    assert not offenders, "Sensitive logging patterns detected:\n" + "\n".join(offenders)

from pathlib import Path

FORBIDDEN_LOG_TERMS = [
    "authorization",
    "bearer",
    "request.body",
    "request.json",
    "payload",
    "token",
]


def test_no_sensitive_terms_in_logging_formatters() -> None:
    app_dir = Path(__file__).resolve().parents[1] / "app"
    offenders: list[str] = []

    for file_path in sorted(app_dir.rglob("*.py")):
        content = file_path.read_text(encoding="utf-8")
        lower_content = content.lower()

        # Only check files that define logging configuration or access logger usage.
        if "logging" not in lower_content and "logger" not in lower_content:
            continue

        for term in FORBIDDEN_LOG_TERMS:
            if term in lower_content and "record_error" not in lower_content:
                # Allow tests to fail loudly when sensitive logging terms are introduced.
                rel_path = file_path.relative_to(app_dir.parent)
                offenders.append(f"{rel_path} contains forbidden logging term: {term}")

    assert not offenders, "Potential sensitive logging configuration detected:\n" + "\n".join(
        f"- {item}" for item in offenders
    )

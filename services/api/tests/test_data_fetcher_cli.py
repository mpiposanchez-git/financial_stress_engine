from __future__ import annotations

from services.api.app import data_fetcher


def test_main_refresh_all_invokes_refresh(monkeypatch, capsys) -> None:
    called: dict[str, bool] = {"value": False}

    def _fake_refresh_all() -> dict[str, list[str]]:
        called["value"] = True
        return {"updated": ["boe_bank_rate"]}

    monkeypatch.setattr(data_fetcher, "refresh_all", _fake_refresh_all)

    exit_code = data_fetcher.main(["refresh-all"])

    assert exit_code == 0
    assert called["value"] is True
    assert capsys.readouterr().out.strip() == '{"updated": ["boe_bank_rate"]}'

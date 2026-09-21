from pathlib import Path

from yaml_doctor.cli import main


def test_check_success(tmp_path, capsys):
    source = tmp_path / "ok.yml"
    source.write_text("name: app\n", encoding="utf-8")
    assert main(["check", str(source)]) == 0
    assert "OK" in capsys.readouterr().out


def test_check_duplicate_fails(tmp_path):
    source = tmp_path / "bad.yml"
    source.write_text("a: 1\na: 2\n", encoding="utf-8")
    assert main(["check", str(source)]) == 1


def test_strict_warning_fails(tmp_path):
    source = tmp_path / "warn.yml"
    source.write_text("a: 1  \n", encoding="utf-8")
    assert main(["check", str(source), "--strict"]) == 1


def test_get_value(tmp_path, capsys):
    source = tmp_path / "app.yml"
    source.write_text("services:\n  - name: api\n", encoding="utf-8")
    assert main(["get", str(source), "services[0].name"]) == 0
    assert capsys.readouterr().out.strip() == "api"


def test_format_refuses_overwrite(tmp_path):
    source = tmp_path / "in.yml"
    output = tmp_path / "out.yml"
    source.write_text("b: 2\na: 1\n", encoding="utf-8")
    output.write_text("keep", encoding="utf-8")
    assert main(["format", str(source), "-o", str(output)]) == 2
    assert output.read_text(encoding="utf-8") == "keep"


def test_format_writes_when_forced(tmp_path):
    source = tmp_path / "in.yml"
    output = tmp_path / "out.yml"
    source.write_text("b: 2\na: 1\n", encoding="utf-8")
    output.write_text("old", encoding="utf-8")
    assert main(["format", str(source), "-o", str(output), "--sort-keys", "--force"]) == 0
    assert output.read_text(encoding="utf-8").startswith("a: 1")

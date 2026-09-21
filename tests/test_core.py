import pytest

from yaml_doctor.core import DuplicateKeyError, diagnose, format_yaml, load_documents, parse_path, query


def test_valid_yaml_and_multiple_documents():
    docs, diags = diagnose("name: app\n---\nitems:\n  - one\n")
    assert len(docs) == 2
    assert not [d for d in diags if d.severity == "error"]


def test_duplicate_key_is_error():
    docs, diags = diagnose("name: one\nname: two\n")
    assert docs is None
    assert diags[-1].code == "duplicate-key"
    assert diags[-1].line == 2


def test_syntax_error_has_location():
    docs, diags = diagnose("items: [one, two\n")
    assert docs is None
    assert diags[-1].code == "syntax"
    assert diags[-1].line is not None


def test_style_diagnostics():
    _, diags = diagnose("name:\tvalue  \n" + "x" * 121)
    codes = {d.code for d in diags}
    assert {"tab", "trailing-space", "line-length"} <= codes


def test_unicode_formatting_round_trip():
    text = "title: مرحبا\nitems: [a, b]\n"
    rendered = format_yaml(text)
    assert "مرحبا" in rendered
    assert load_documents(rendered)[0]["items"] == ["a", "b"]


def test_query_paths():
    data = {"services": [{"name": "api", "ports": [80, 443]}]}
    assert parse_path("services[0].ports[1]") == ["services", 0, "ports", 1]
    assert query(data, "services[0].name") == "api"
    assert query(data, "services[0].ports[1]") == 443


def test_missing_path_fails():
    with pytest.raises(KeyError):
        query({"a": 1}, "b")


def test_empty_document_warning():
    docs, diags = diagnose("")
    assert docs == []
    assert any(d.code == "empty" for d in diags)

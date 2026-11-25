import pytest

from qa_mcp_server import tools


def test_generate_is_reproducible():
    schema = {"n": "name", "e": "email", "id": "uuid"}
    assert tools.generate_test_data(schema, 3, seed=1) == tools.generate_test_data(schema, 3, seed=1)


def test_generate_count_and_fields():
    rows = tools.generate_test_data({"a": "int", "b": "bool"}, 10)
    assert len(rows) == 10 and set(rows[0]) == {"a", "b"}


def test_generate_rejects_bad_input():
    with pytest.raises(ValueError):
        tools.generate_test_data({"a": "nope"})
    with pytest.raises(ValueError):
        tools.generate_test_data({})
    with pytest.raises(ValueError):
        tools.generate_test_data({"a": "int"}, count=0)


def test_boundary_values():
    r = tools.boundary_values(1, 100)
    assert r["valid"] == [1, 2, 50, 99, 100]
    assert r["invalid"] == [0, 101]


def test_boundary_small_range_has_no_out_of_range_values():
    assert tools.boundary_values(5, 5)["valid"] == [5]


def test_boundary_rejects_reversed_range():
    with pytest.raises(ValueError):
        tools.boundary_values(10, 1)


def test_edge_cases_include_prompt_injection():
    assert any("prompt injection" in c["probes"] for c in tools.edge_case_strings())


def test_triage_timeout_and_flaky():
    r = tools.triage_failure("TimeoutError: Timeout 30000ms exceeded. Passed on rerun.")
    assert r["likely_causes"][0]["category"] == "timeout"
    assert r["possibly_flaky"] is True


def test_triage_selector():
    r = tools.triage_failure("Error: strict mode violation: locator('button') resolved to 2 elements")
    assert any(c["category"] == "selector" for c in r["likely_causes"])


def test_triage_unknown_and_empty():
    assert tools.triage_failure("something odd")["likely_causes"][0]["category"] == "unknown"
    with pytest.raises(ValueError):
        tools.triage_failure("  ")

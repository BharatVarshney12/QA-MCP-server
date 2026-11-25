"""MCP server exposing the QA helpers as tools."""
from mcp.server.fastmcp import FastMCP

from . import tools

mcp = FastMCP("qa-mcp-server")


@mcp.tool()
def generate_test_data(schema: dict[str, str], count: int = 5, seed: int = 42) -> list[dict]:
    """Generate reproducible synthetic test records.

    schema maps field name to type. Types: name, email, phone, date, int, bool, uuid, text.
    Example: {"full_name": "name", "contact": "email", "age": "int"}
    """
    return tools.generate_test_data(schema, count, seed)


@mcp.tool()
def boundary_values(minimum: int, maximum: int) -> dict[str, list[int]]:
    """Return valid and invalid boundary values for an integer range."""
    return tools.boundary_values(minimum, maximum)


@mcp.tool()
def edge_case_strings() -> list[dict[str, str]]:
    """Return strings that commonly break input handling, including prompt injection."""
    return tools.edge_case_strings()


@mcp.tool()
def triage_failure(log: str) -> dict:
    """Give a rule-based first triage of a failed test's log or error message."""
    return tools.triage_failure(log)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()

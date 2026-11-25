# qa-mcp-server

A small [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that gives AI assistants practical QA tools: synthetic test data, boundary values, risky input strings and a first look at failed test logs.

It is deliberately simple. Every tool is deterministic, needs no API key and makes no network calls, so the results are reproducible and the code is easy to read if you are learning MCP.

## Tools

| Tool | What it does |
|------|--------------|
| `generate_test_data` | Creates reproducible synthetic records from a schema (name, email, phone, date, int, bool, uuid, text). Same seed gives the same data. |
| `boundary_values` | Returns valid and invalid boundary values for an integer range. |
| `edge_case_strings` | Returns strings that often break input handling: empty, very long, SQL characters, script tags, unicode, control characters and a prompt-injection example for LLM apps. |
| `triage_failure` | Rule-based first triage of a failed test log (timeout, selector, assertion, network, auth, data conflict) with a suggested next step and a possible-flaky hint. |

`triage_failure` is a heuristic starting point. Always confirm by reproducing the failure.

## Install

Requires Python 3.10 or newer.

```bash
git clone https://github.com/BharatVarshney12/qa-mcp-server.git
cd qa-mcp-server
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
```

## Use it with Claude Desktop

Add this to your `claude_desktop_config.json`, using the full path to the Python inside your virtual environment:

```json
{
  "mcpServers": {
    "qa-tools": {
      "command": "/full/path/to/qa-mcp-server/.venv/bin/python",
      "args": ["-m", "qa_mcp_server.server"]
    }
  }
}
```

Restart Claude Desktop, then try prompts like:

- "Generate 5 test users with a name, email and phone number."
- "Give me boundary test values for an age field from 18 to 60."
- "Triage this failure: `Error: strict mode violation: locator('button') resolved to 2 elements`"

## Use it with Claude Code

```bash
claude mcp add qa-tools -- /full/path/to/qa-mcp-server/.venv/bin/python -m qa_mcp_server.server
```

## Try it without a client

Run the MCP Inspector to call the tools from a browser:

```bash
npx @modelcontextprotocol/inspector python -m qa_mcp_server.server
```

## Project layout

```
src/qa_mcp_server/
  tools.py     pure functions, unit tested
  server.py    MCP wiring (FastMCP), one decorated function per tool
tests/         pytest unit tests
.github/       CI workflow (Python 3.10 and 3.12)
```

Keeping the logic in `tools.py` and the protocol wiring in `server.py` means you can test the QA logic without running a server.

## Ideas for extending it

- Add a tool that reads a Playwright or JUnit report and summarizes the failures.
- Add a tool that builds a golden dataset entry (question, expected answer, source) for RAG evaluation.
- Connect `triage_failure` to an LLM for deeper analysis, keeping the rules as a fast first pass.

## Contributing

Issues and pull requests are welcome. Please add a test for any new tool or rule.

## License

MIT

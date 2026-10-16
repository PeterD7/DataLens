# DataLens

DataLens is a planned modular financial research and visualization tool. Each Lens
is visual, quantifiable, and composable. Development starts with one company's
CapEx history, reusable financial metrics, and one interactive visualization.

Status: repository scaffold and architecture specifications only. Application
functionality has not been implemented. The former working name was FlowLens.

## Folder guide

| Location | Purpose |
| --- | --- |
| `src/datalens/` | Reusable Python code |
| `apps/dashboard/` | Future dashboard entry point |
| `tests/` | Automated tests and small test fixtures |
| `docs/` | Planning, definitions, and development notes |
| `data/` | Local datasets; contents excluded from Git except its README |
| `AGENTS.md` | Shared guidance for coding assistants |
| `.cursor/rules/project.mdc` | Always-applied Cursor project guidance |
| `pyproject.toml` | Python package metadata; add dependencies as needed |
| `docs/FlowLens_Sketch_10.13.docx` | Original planning reference, preserved unchanged |

## Working locally

Open this whole folder in your editor. Keep one shared project folder across your tools.
The scaffold uses Python 3.11 or newer as a starting baseline.
When ready to write code, create a local environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Select `.venv/bin/python` as the interpreter in your editor. There is no runnable
dashboard or test suite yet. No application dependencies have been selected or installed.

## Next steps

Start with the [architecture audit](docs/architecture.md),
[shared data contracts](docs/data_contracts.md), [CapEx methodology](docs/metric_definitions.md),
and [V1 roadmap](docs/roadmap.md). The first recommended coding task is pure quarterly
normalization with synthetic tests, before live ingestion or dashboard work.

The future temporal network will distinguish what was publicly known at a date from
what was economically effective then. Documented spending, estimated exposure, and
thematic relationships stay distinct; undisclosed allocations remain unallocated.

## GitHub later

This folder is prepared for Git, but no repository or GitHub remote has been created.
The `.gitignore` excludes local environments, editor settings, secrets, and local data.
Review the files (including the original sketch) before your first commit. Choose a
license before publishing if you want to grant others permission to reuse the code.

## Notes

<!-- Add a short project description, setup instructions, and screenshots as the project grows. -->

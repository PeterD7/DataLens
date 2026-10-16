# DataLens architecture and audit

Audit date: 2026-10-13. Status: design baseline, not implemented functionality.

## Audit result

The original layout suits a small modular Python application. Its documentation
defined responsibilities but left contracts, revisions, fiscal normalization,
allocation accounting, and release criteria unresolved. This audit establishes those
rules in [data contracts](data_contracts.md), [metric definitions](metric_definitions.md),
and the [roadmap](roadmap.md).

All existing Markdown documentation, configuration, Python placeholders, and the
original Word sketch were reviewed. The sketch remains historical reference; the
latest user requirements and these documents establish current scope.

| Area | Finding and decision |
| --- | --- |
| Structure | Retain all layers; rename `src/flowlens` to `src/datalens` to match the requested product name. |
| Shared models | Define stable identities, immutable versions, sources, units, periods, and availability. Implement only the next milestone's subset. |
| Temporal support | Use explicit dates and version rows in ordinary tables; no graph or temporal database. |
| Streamlit independence | Placeholders currently have no Streamlit dependency. Enforce the boundaries below as code is added. |
| Additional Lenses | Common numerical and event contracts support extension; actual interoperability requires tests once implemented. |
| Complexity | No unnecessary infrastructure exists. Do not add frameworks just to populate folders. |
| Housekeeping | `.gitignore` exists; add `.cursor/rules/project.mdc` alongside shared `AGENTS.md`. |

## Product principles and V1

Every Lens is visual, quantifiable, and composable. Numerical observations support
mathematics; qualitative events carry structured dates, entities, and linked measurements.
Choose charts, maps, timelines, or networks according to the underlying data. Lenses
need not all use money-flow diagrams.

V1 delivers one company's cash CapEx history, reusable metrics, and one interactive
historical chart with a detail panel. The panel exposes company, period, documented
allocation categories, and available relationships. Clicking a category or relationship
opens evidence and dates. Missing disclosure is explicit. Microsoft is the recommended
first company, subject to source mapping review. Comparisons and the full network
time slider follow V1.

## Responsibilities and dependency boundaries

| Location | Responsibility | Dependencies |
| --- | --- | --- |
| `src/datalens/core/` | Shared records, validation, temporal selection | Standard library initially |
| `src/datalens/sources/` | Retrieve payloads and map source fields | Core; HTTP client when needed |
| `src/datalens/storage/` | Persist records, versions, provenance | Core; SQLite |
| `src/datalens/lenses/capex/` | Pure normalization, metrics, allocations; service orchestration | Core; service may call source/storage functions |
| `src/datalens/visualization/` | Build figures from prepared records | Core; Plotly when needed |
| `apps/dashboard/` | User inputs, session state, rendering, details | Services, visualization, Streamlit |

Core and calculation functions must never import Streamlit, dashboard, Plotly, database
connections, or HTTP clients. Visualization must not fetch data or calculate financial
metrics. Streamlit caching belongs in app wrappers. Functions accept records and return
records or explicit validation results. Test services using injected callables and
in-memory collections; add formal interfaces only when a second implementation needs them.

The example file layout is effective as a guide for future files:

- `core/models.py`: records and validators needed by the first slice.
- `core/temporal.py`: shared version/date queries when introduced.
- `sources/sec/client.py` and `normalization.py`: retrieval and SEC tag/sign mapping.
- `lenses/capex/metrics.py`: pure financial period normalization and calculations.
- `lenses/capex/relationships.py`: allocation validation and relationship preparation.
- `lenses/capex/service.py`: orchestration, without UI state.
- `storage/database.py` and `repositories.py`: concrete SQLite operations.
- `visualization/charts.py` and later `networks.py`: presentation only.

Do not create all these files in advance. Source-specific conventions belong in the
adapter; financial methodology belongs in CapEx. No application modules are added by this audit.

## Temporal economic networks

Historical queries have two inputs: `effective_on` (economic date) and
`knowledge_cutoff` (latest permitted public information).

The **known-then** perspective sets the economic date to the selected date and the
cutoff to its explicit end of day/timezone. Later announcements are excluded even if
they describe earlier periods. The **retrospective** perspective holds economic date
fixed and uses an explicitly labeled latest-data cutoff, allowing later corrections.

Select the latest eligible version of each logical record at the knowledge cutoff
first, then filter its economic interval. Reversing that order can resurrect a
superseded claim. Preserve cancellations and retractions as versions. Apply the same
cutoff to entity labels/identifiers and show eligible endpoints or selected standalone
entities. First appearance in DataLens is not a company's founding date.

An unknown effective start remains unknown, not the announcement date. A future
contract can appear in announcements but is not an active edge before its start.
An unknown end is open-ended with an explicit uncertainty label.

Synthetic example: a March 10 announcement says a contract started February 1; an
April 5 update says it ended March 1. February 15 known-then has no edge; February 15
retrospective after April 5 can show it. March 20 known-then may show it active, while
retrospective March 20 after April 5 does not.

Use ordinary SQLite version rows, indexes on logical IDs/availability/periods, and
retained raw evidence. Python query functions implement both perspectives. No database
snapshot per slider position, event bus, or separate system-time audit engine is needed.

## Capital allocation and visual semantics

Reported cash CapEx is the parent total. Only documented non-overlapping allocations
matching its entity scope, period, currency, and accounting basis reduce the residual.
Contract commitments, estimates, and thematic links do not reduce reported spending.
Partial disclosure yields an explicit unallocated/undisclosed remainder.

The user's $40B/$5B/$35B example is synthetic arithmetic, not evidence about Alphabet
or a supplier. Overlapping allocations or an overage produce a conflict and suppress
a misleading breakdown. Never clamp a negative residual to zero to conceal a problem.

V1 uses a quarterly/annual historical chart and selected-period details. A reconciled
allocation breakdown can appear in the detail panel; without eligible allocations the
whole total is unallocated. Relationship details are clickable without requiring a
network renderer. Drill-down must not count both categories and their supplier children.

Future networks include a legend: documented monetary flows have currency/period
labels and proportional widths; verified nonmonetary edges use fixed-width solid
lines, estimated exposures dashed lines, thematic edges dotted lines. Use patterns
and labels as well as color. Distinguish announced, active, ended, and unknown-effective
states. Evidence that a relationship exists does not establish a dollar allocation.

## Composable Lenses and research

A new Lens adds its processing under `lenses/`, metric definitions, and source adapters
as needed. It returns shared records instead of importing other Lenses' private logic.
Stable entities, explicit units/frequency, methodology versions, and availability make
joins possible. Similar labels alone do not establish comparability.

CapEx growth, interest rates, electricity prices, and revenue growth can become model
inputs after explicit alignment. GeoLens can link a tariff announcement event to a
rate observation and affected trade value; the event needs no invented numerical score.

QuantLab will consume historical indicators and events, with version selection at
each research cutoff. It must define trading calendars, execution lag, stale-data limits,
frequency alignment, and missing-value policies. Never fill future information backward.
The current scaffold is not a working research or backtesting engine.

## Complexity and open decisions

Keep Python 3.11+, SQLite, and Streamlit/Plotly as the initial direction. Add dependencies
only when required; Pandas is optional until useful. Defer microservices, React/FastAPI,
plugin discovery, generic repositories, universal event schemas, and graph infrastructure.

Confirm the first company/history window, source tag mapping, unusual CapEx definitions,
and availability of allocation evidence during source review. License and GitHub visibility
remain publishing decisions. Roadmap defaults allow the first coding task to be precise.

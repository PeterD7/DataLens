# CapExLens V1 roadmap

Priority: accurate ingestion, standardized metrics, and one compelling interactive
visualization. This is an implementation plan; no functional milestone is complete yet.

- [x] Initial repository skeleton.
- [x] Architecture audit, shared contract design, CapEx methodology, and DataLens naming.
- [x] Git ignore rules and dedicated Cursor project rules.

## V1 capabilities and boundaries

| Capability | V1 acceptance |
| --- | --- |
| Capital visualization | Show reported cash CapEx and eligible documented allocations; explicitly show undisclosed remainder. |
| Historical timeline | One company, quarterly/annual history with actual dates, fiscal labels, revisions, and data cutoff. |
| Interactive exploration | Select a period/company, then available category or relationship details; show evidence, announcement/effective/expiration dates, value basis, and changes where known. |
| Quantitative output | Reusable observations and indicators, with unit, period, methodology, availability, and provenance; machine-readable export. |

Recommend Microsoft first, initially FY2023–FY2025 (12 fiscal quarters) for a bounded
reproducible baseline. This is a proposed scope, not already retrieved data or a claim
to cover the latest financial results. Source review confirms availability and mapping.
Load extra comparator periods only if needed; otherwise show unavailable early growth.

## Precise implementation sequence

Complete each gate before moving to dependent work. Tests use local synthetic fixtures
by default; external service access is isolated.

1. **Pure records and quarter normalization.** Create only required models in
   `core/models.py` and pure functions in `lenses/capex/metrics.py`. Add pytest as a
   development dependency and tests under `tests/unit/` with synthetic fixtures.
   Gate: 10/25/45/70 cumulative inputs produce 10/15/20/25 quarters with full lineage
   and correct availability; missing, mixed-basis, fiscal-calendar, and revised inputs
   are handled explicitly. Import and run without Streamlit, SQLite, or network access.
2. **Source reconnaissance and mapping.** Inspect original filings for the chosen
   company/window. Document concept, scope, units, sign, fiscal boundaries, and filing
   metadata. Keep small attributable sample fixtures. Gate: selected quarterly/YTD/annual
   examples reconcile to original statements; unresolved mappings block affected facts.
3. **One-company SEC ingestion.** Implement `sources/sec/client.py` and source field
   mapping separately. Add an identified User-Agent, caching, bounded retry/backoff,
   timeouts, and compliance with current SEC access guidance. Retain raw payloads and
   checksums under ignored `data/`. Gate: fixture-driven parser tests and a deliberate
   live retrieval demonstrate traceability, deduplication, and explicit errors.
4. **Persistence and version selection.** Add simple SQLite storage of normalized
   records, provenance, and revisions; introduce `core/temporal.py` as needed for pure
   cutoff selection. Gate: repeat imports are idempotent, originals survive corrections,
   known-then excludes later versions, and round-trip decimal/date values are preserved.
5. **Metrics and application service.** Add QoQ, YoY, annual, and TTM results and an
   orchestration service returning shared records. Gate: formulas and missing-input rules
   pass; every output references exact inputs and latest-input availability; service tests
   run with in-memory data and no UI. Export decimal strings with schema and methodology
   versions, units, periods, source references, and the query cutoff.
6. **Minimal allocation and relationship details.** Add documented allocation validation
   and detail records only as needed for V1. Gate: synthetic $40/$5/$35 partitions work;
   overlapping/overallocated cases fail; commitments/estimates do not reduce totals.
   Real missing disclosures remain missing. If no eligible breakdown exists, show the
   full amount as unallocated. Synthetic relationship examples remain clearly labeled
   test/demo data and never masquerade as real company evidence.
7. **One interactive visual workflow.** Build the Plotly history chart and thin Streamlit
   shell. Include quarterly/annual selection, click-to-detail, company/category/relationship
   exploration, sources, units, fiscal dates, and a visible legend for allocation status.
   Gate: verify selections update correct detail records; chart code performs no financial
   calculations or API access; missing data is visibly distinct from zero.
8. **V1 release check.** Reconcile the full chosen history to source statements, test
   calculations and revision handling, validate exports, and document install/run/test
   commands. Gate: a fresh environment can reproduce the local workflow; no private data
   or secrets are staged; the UI explains methodology and disclosure limitations.

## After V1

1. Add Alphabet/Amazon and deliberate cross-company fiscal/basis comparisons.
2. Implement the full temporal network, with known-then versus retrospective modes,
   economic-date slider, date/evidence legend, version history, and allocation drill-down.
   Its entity/relationship contracts are reserved now; its renderer is deferred.
3. Add a second Lens to exercise real contract reuse without a plugin framework.
4. Introduce QuantLab consuming both versioned numerical indicators and economic events,
   after point-in-time coverage, trading-time alignment, costs, and evaluation rules are defined.
5. Expand other Lenses and choose their own best-fit visuals.

## Open decisions

- Confirm recommended Microsoft/FY2023–FY2025 scope before live ingestion.
- Verify each accepted CapEx tag/basis and source precision during source reconnaissance.
- Determine which actual allocation/relationship disclosures are usable; absence is a valid result.
- Set final UI labels and accessibility choices during the chart milestone.
- Choose a license and public/private GitHub visibility before publication.

**Recommended first coding task:** implement milestone 1 only: typed source/observation
records and pure quarter normalization with synthetic tests. It resolves the highest-risk
financial logic before adding external data, a database, or a dashboard.

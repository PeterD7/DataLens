# Shared data contracts

Design version 1, 2026-10-13. These specifications are not implemented classes or tables.
Start with standard-library dataclasses and explicit validation; build only each
milestone's required subset.

## Conventions and version envelope

IDs are stable opaque strings; names/tickers are attributes. Dates use ISO YYYY-MM-DD;
timestamps are timezone-aware UTC. Numeric values use `Decimal`, serialized as decimal
strings in JSON and SQLite TEXT. Round only for display. Null requires a missing reason;
it never means zero. Reporting periods have inclusive endpoints. Economic validity uses
`[valid_from, valid_to)` with an exclusive end.

Every entity, observation, relationship, allocation, and event version uses this envelope.
Indicators use the same identity/version fields plus computational lineage.

| Field | Type and rule |
| --- | --- |
| `logical_id` | Required string; identity across revisions |
| `record_id` | Required unique immutable version ID |
| `schema_version` | Required positive integer, initially 1 |
| `supersedes_record_id` | Nullable prior version of the same logical record; no cycles |
| `source_ids` | Evidence references; nonempty for sourced claims |
| `available_at` | UTC timestamp or null; conservative public availability of this version |
| `availability_basis` | `exact`, `date_only_conservative`, `derived_inputs`, or `unknown` |
| `recorded_at` | Required ingestion/computation timestamp; never substituted for publication |
| `status` | `accepted`, `needs_review`, or `retracted` |
| `quality_flags` | List of explanatory codes |

Unresolved conflicts are excluded from published metrics. A latest eligible retraction
suppresses the record, without falling back to older accepted versions. Conflicting
sources do not automatically supersede each other. Same-time versions need an explicit
supersession chain; ambiguous ties fail validation.

Availability cannot predate the evidence establishing a sourced claim. Changed claims
create new versions. Identical repeated disclosures can be corroboration without changing
original availability; retain provenance. Derived records retain exact input versions.

## SourceReference

| Field | Type and rule |
| --- | --- |
| `source_id` | Unique immutable string |
| `provider`, `document_type`, `url` | Required source identity and original-document URL |
| `accession_number` | Required for SEC filing evidence; otherwise nullable |
| `published_on` | Source-local publication date, nullable if unknown |
| `published_at`, `source_timezone` | Exact UTC timestamp if known; timezone required for date-only conversion |
| `publication_precision` | `timestamp`, `date`, or `unknown` |
| `retrieved_at` | Required UTC timestamp |
| `locator` | Statement/note/table/section supporting the claim |
| `raw_payload_ref`, `content_hash` | Retained payload location and checksum when ingested |

For date-only publication, conservative `available_at` is midnight at the start of
the following day in the source timezone, converted to UTC. Preserve the original date;
this boundary is a policy, not an invented exact publication time. Unknown date/timezone
means unknown availability and exclusion from known-then queries. Trading-session mapping
belongs to future QuantLab, not ingestion.

## Entity

Fields: `entity_id` (also `logical_id`), required `name`, `entity_type` (company,
category, industry, country, region), namespaced `identifiers` (CIK, exchange/ticker),
nullable `valid_from`/`valid_to` for that name/identifier version, and optional
`parent_entity_id` for classification. These dates are not assumed company lifetime.
Names and ticker changes preserve entity identity. Historical labels must not silently
use today's ticker; disclose missing historical metadata.

## MetricDefinition

Fields: `metric_id`, `definition_version`, `label`, `description`, `owner_lens`, `unit`,
`value_kind` (flow, stock, rate, ratio), `allowed_frequencies`, `aggregation_rule`,
`methodology`, and `limitations`. Stable names include `capex.cash_ppe`,
`capex.growth_yoy`, `macro.interest_rate`, `energy.electricity_price`, and
`earnings.revenue_growth`. These are data identifiers, not required Python APIs.

Different accounting bases require different IDs or explicit definition versions.
Do not sum rates as though they were cash flows. Units include denominators, e.g.
`USD/MWh`. Dimensionless ratios store `0.20` for 20%; display formatting is separate.

## FinancialObservation

| Field | Type and rule |
| --- | --- |
| `entity_id`, `metric_id`, `definition_version` | Required references |
| `value`, `missing_reason` | Decimal/null; explanation required for null |
| `unit`, `currency` | Required unit; ISO currency for monetary values |
| `period_start`, `period_end` | Duration endpoints; instant facts have null start |
| `period_kind`, `frequency` | `duration`/`instant`; documented frequency such as quarter, ytd, annual |
| `fiscal_year`, `fiscal_quarter` | Nullable generally; required for accepted V1 quarterly facts |
| `fiscal_year_start`, `fiscal_year_end` | Verified fiscal boundaries for normalization |
| `dimensions` | Structured scope, e.g. consolidated or segment; V1 is consolidated |
| `source_concept`, `source_unit`, `source_value` | Original taxonomy/tag, unit, signed value |
| `source_fy`, `source_fp`, `source_frame` | Raw SEC labels; separate from normalized period labels |
| `origin` | `reported` or `derived` |
| `input_record_ids`, `methodology_version` | Required for derived quarters |

Logical identity includes entity, metric definition, actual period, frequency, unit,
and dimensions. Changed prior-period facts become revisions; identical disclosures
are deduplicated without discarding evidence. Incompatible definitions are separate
series. Validate finite values, date ordering, references, and metric-specific signs.

## Relationship

| Field | Type and rule |
| --- | --- |
| `relationship_id` | Logical identity of one contract/relationship, not only its endpoint pair |
| `from_entity_id`, `to_entity_id` | Required endpoints; direction specified by type |
| `relationship_type` | Documented vocabulary, e.g. supplier, investment_category, thematic_exposure |
| `evidence_class` | `verified`, `estimated`, or `thematic` |
| `announced_on` | Nullable announcement date; independent of availability |
| `valid_from`, `valid_to` | Nullable economic start and exclusive end |
| `end_reason` | Nullable, e.g. expired or terminated |
| `contract_value`, `currency` | Optional disclosed or explicitly estimated amount with currency |
| `value_basis` | Required with value: commitment, ceiling, estimate, or other documented basis |
| `methodology`, `limitations` | Method required for estimates; describe evidence limitations |

Preserve exact expiration wording in source evidence. Expiration at the end of a date
normalizes to the following day as exclusive `valid_to`. Never infer a start from an
announcement. Multiple contracts between the same endpoints have distinct identities.
Changes append versions; future terminations set an end, while withdrawn claims use
`retracted`. Version history supplies the detail panel's historical changes.

Verified evidence supports the stated relationship, not necessarily a payment. Thematic
edges have no attributable monetary value. A disclosed contract amount is not by itself
a CapEx allocation.

## CapitalAllocation

| Field | Type and rule |
| --- | --- |
| `allocation_id` | Logical identity with common version envelope |
| `total_observation_record_id` | Exact CapEx total version partitioned |
| `from_entity_id`, `to_entity_id` | Spending company and disclosed category/supplier |
| `amount`, `currency`, `period_start`, `period_end` | Required for eligible monetary allocations |
| `evidence_class` | `documented` or `estimated`; estimates remain separate overlays |
| `measurement_basis` | Must match parent total, e.g. cash_ppe |
| `allocation_set_id`, `parent_allocation_id` | Consistent partition and optional drill-down parent |
| `relationship_id` | Optional supporting relationship |
| `methodology`, `limitations` | Scope, exclusions, assumptions |

Only accepted documented allocations matching total scope and covering disjoint spending
reduce the residual. Validate units, period, basis, duplicate coverage, and hierarchy.
Never add categories to their supplier children. Reconcile immediate children separately
at each level. A revised total requires allocation revalidation, not automatic rebinding.

Residual = total minus eligible direct allocations. Return exact input version IDs,
cutoff, and reconciliation status. No allocations means the full total is unallocated.
Overages beyond declared source rounding tolerance, overlap, or incompatible scope yield
a conflict rather than a misleading chart. Residual is undisclosed allocation, not unspent cash.

## Indicator

Fields: `entity_id`, `metric_id`, `definition_version`, `value`, `missing_reason`,
`unit`, `period_start`, `period_end`, `frequency`, exact `input_record_ids`,
`methodology_version`, `computed_at`, `knowledge_cutoff`, and `perspective`
(`known_then`/`retrospective`), plus the common envelope.

Availability is at least the maximum availability of required inputs; any unknown
required availability makes the result unknown. Corrected inputs create new indicator
versions. Today's historical reconstruction does not prove that its strategy existed
then; QuantLab must separately control strategy selection and execution timing.

## EconomicEvent

Future contract: `event_id` (logical ID), `event_type`, `entity_ids`, `summary`,
`announced_on`, `valid_from`, `valid_to`, `evidence_class`, `related_record_ids`,
`measurement_record_ids`, and common version fields. A tariff announcement links to
rate/trade-value observations without an invented scalar score. Distinguish occurrence
from reports about it. Add typed event-specific fields when a second Lens needs them.

## Query boundaries and examples

Future pure interfaces accept records without database/API/UI access:

- `select_versions(records, knowledge_cutoff)`: eligible versions first.
- `relationships_at(records, effective_on, knowledge_cutoff)`: economic intervals second.
- `calculate_metrics(observations, definitions)`: indicators and quality results.
- `allocation_breakdown(total, allocations, knowledge_cutoff)`: partition or conflict.

Unknown availability is excluded from known-then selection. Unknown economic starts
are excluded from active edges and shown in an unknown-date view. Unknown ends are
open intervals labeled as uncertain. Retrospective queries also record an explicit cutoff.

Synthetic tests must cover late announcements, retroactive corrections, future starts,
end boundaries, retractions, unknown dates, source conflicts, multiple contracts per
endpoint pair, and $40/$5/$35 allocation arithmetic. No external API is needed.

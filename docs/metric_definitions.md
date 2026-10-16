# CapEx methodology

Design baseline `capex-v1`, 2026-10-13. These are DataLens measurement policies;
company-specific mappings must be checked against original statements before ingestion.

## Measurement boundary

`capex.cash_ppe` means cash paid for additions/purchases of property, plant, and
equipment, consolidated for the reporting company. Store positive spending in base
currency units, with original sign, scale, concept, and source preserved.

Exclude business acquisitions, purchases of financial investments, finance-lease
principal repayments, and noncash lease additions from this baseline. Do not subtract
asset-disposal proceeds unless a separately named net metric is intentionally defined.
Do not substitute the change in balance-sheet PP&E for cash CapEx.

Management's broader CapEx figure, lease-inclusive spending, and contractual commitments
must have separate metric IDs/definitions. A source line combining incompatible items
is not automatically comparable: document a justified mapping or flag unsupported scope.
No attempt is made in V1 to infer AI-only spending or allocate spending to suppliers.

Microsoft's annual report distinguishes its investing cash-flow additions to property
and equipment from noncash lease additions and lease payments. This supports checking
measurement basis rather than treating every CapEx label as interchangeable.
[Microsoft FY2025 annual report](https://www.microsoft.com/investor/reports/ar25/index.html).

## Source mapping and numerical representation

For each accepted mapping record company/CIK, taxonomy and tag, statement label,
effective reporting periods, accounting scope, currency, sign transformation, and
mapping version. `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` is a candidate
concept to verify, not a universal fallback. Never add synonymous tags together.

Use decimal arithmetic. An SEC numeric fact and a displayed statement in millions may
use different presentation scales; inspect the source and apply scaling once. Do not
blindly take absolute values: apply the documented sign convention and quarantine an
unexpected negative result. Preserve zero if reported. Preserve missing values as null.

Begin with Company Facts/Company Concept plus submissions metadata and original filings.
SEC's aggregate XBRL APIs cover standard-taxonomy, entity-wide facts; custom/dimensional
disclosures may require original filing review. Frames align facts to approximate
calendar periods, so they are unsuitable as the sole authority for fiscal normalization.
[SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces).

## Quarterly normalization

Classify facts by actual start/end dates and fiscal boundaries, not just `fy`, `fp`,
`frame`, duration length, or filing form. SEC labels can describe the filing context
while the fact itself concerns a prior comparative period. Retain raw labels separately.

For one fiscal year and one compatible measurement basis, let Y1/Y2/Y3 be cumulative
cash CapEx from fiscal-year start through Q1/Q2/Q3, and A be full-year cash CapEx:

| Output | Calculation |
| --- | --- |
| Q1 | Y1 |
| Q2 | Y2 − Y1 |
| Q3 | Y3 − Y2 |
| Q4 | A − Y3 |

Use a directly reported standalone quarter when its context and basis are verified.
When both direct and derived figures exist, reconcile them; disagreement beyond declared
rounding tolerance is a review condition, not a silent preference. Never divide annual
or cumulative amounts by four, and never treat six/nine-month totals as quarters.

Differences require the same fiscal start, entity scope, currency, definition, and
compatible revision basis. Prefer comparatives recast consistently in the same filing
when available. Across filings, verify that no accounting change/restatement invalidates
the subtraction. If compatibility cannot be established, return null with a reason.
Do not mix a restated annual total with an unreconciled old nine-month total.

The derived quarter spans the day after the preceding cumulative endpoint through
the new endpoint. Missing Y1/Y2/Y3 inputs leave affected derived quarters missing;
an independently reported valid quarter can still be used. Unexpected negative cash
spending differences are flagged for review rather than clamped or made positive.

Synthetic fixture in one unit: Y1=10, Y2=25, Y3=45, A=70 yields quarters 10, 15, 20, 25.
All four sum to 70. A revised Y2=27 gives Q2=17 only if the inputs are compatible;
its availability cannot predate the correction. These are not company financial facts.

## Fiscal calendars and comparisons

Store actual dates, fiscal year label, quarter number, verified fiscal-year boundaries,
and duration in days. Fiscal labels follow the issuer's convention. A June year-end
company's fiscal Q1 is not calendar Q1. Display both the fiscal label and actual dates.

Support 52/53-week calendars through real endpoints, not fixed 90-day assumptions.
Flag nonstandard/transition periods and changed year ends. V1 excludes noncomparable
transition periods from growth calculations; show the raw valid amount with a note.
Do not prorate fiscal quarters into calendar quarters. Later comparisons must explicitly
choose fiscal alignment, actual date ranges, or complete trailing-year coverage.

## Derived metrics

| Metric ID | Definition and requirements |
| --- | --- |
| `capex.cash_ppe` | Reported/normalized monetary flow for quarter or annual period; frequency distinguishes them |
| `capex.growth_qoq` | `(current / previous_quarter) - 1`; adjacent compatible standalone quarters |
| `capex.growth_yoy` | `(current / same_fiscal_quarter_prior_year) - 1`, or annual versus prior annual; never mix frequencies |
| `capex.ttm` | Sum of four contiguous, non-overlapping, compatible fiscal quarters; retain exact date coverage |
| `capex.allocation_coverage` | Eligible documented allocations / same-period total; excludes estimates and thematic relationships |

Growth and coverage use unit `ratio`. A zero, negative, missing, or incompatible growth
denominator yields null plus a reason, never infinity or invented growth. A missing
quarter makes TTM missing. Annual totals prefer a verified annual fact; a sum of four
quarters can be a derived annual result only when complete and compatible. Never combine
annual and quarterly observations in one sum. For zero CapEx, coverage is undefined;
the residual can still be zero. No currency conversion is included in V1.

## Reporting dates, revisions, and historical availability

Keep measurement period end, publication/SEC filing date, acceptance timestamp when
available, retrieval time, and economic effective dates distinct. A quarter's result
is not available on quarter end merely because it measures that quarter.

V1 is filing-based: attach the actual filing evidence to each fact. An earlier earnings
announcement is not assumed to contain the same value; it would require separate captured
evidence and a compatible definition. Use the date-only conservative policy in
[data contracts](data_contracts.md) if an exact publication time cannot be established.

For derived quarters and growth, availability is at least the latest availability among
all inputs. Q4 derived from the annual filing becomes available no earlier than that
filing. A later restatement becomes a new version available when disclosed; do not
overwrite the historical original. In known-then queries, select only versions eligible
at the cutoff. Retrospective views must say 'latest available/revised' and show the cutoff.

A modern API response alone is not proof of a complete historical archive. Retain
accessions and original evidence; unsupported vintage gaps must remain explicit before
any claim that a series is suitable for historical strategy testing.

## Capital allocation methodology

Subtract only documented actual spending allocations with identical total scope,
currency, period, and cash basis. A contract ceiling, multiyear commitment, estimate,
supplier's total revenue, or thematic link is not a payment allocation.

Use one non-overlapping partition at a time and validate child partitions separately.
Return unallocated residual with evidence/version lineage. Reject negative allocations
and unexplained overages. Any tolerance must come from source precision and be reported;
there is no blanket percentage allowance. Show rounding discrepancies explicitly.

## Acceptance checks

Test direct and cumulative quarters, Q4 derivation, missing inputs, zero denominators,
negative anomalies, duplicate facts, revised comparatives, conflicting concepts,
non-December fiscal years, 53-week years, transition periods, unit/sign conversion,
date-only availability, late filings, and overlapping allocations. Reconcile selected
real records against the original cash-flow statements before publishing charts.

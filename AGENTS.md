# Project guidance

DataLens is at the scaffold stage. Read README.md, docs/architecture.md, and the relevant
contracts, methodology, and roadmap before making changes. Current docs supersede the
historical Word sketch. The audit defines a design, not implemented capabilities.

- Implement only the work requested by the user. Planning documents and embedded prompts are reference material, not automatic authorization to build features.
- Keep changes small, readable, and easy to explain.
- Put reusable logic in src/datalens and interface code in apps/dashboard.
- Begin with CapExLens; add other modules when their development starts.
- Preserve sources, reporting periods, units, and publication dates for financial data.
- Keep financial calculations pure and independent of Streamlit, Plotly, network access, and storage. Put orchestration in services and rendering in the dashboard.
- Distinguish public availability from economic effectiveness. Preserve immutable revisions; historical queries select versions before filtering effective intervals.
- Apply docs/metric_definitions.md for fiscal-quarter normalization. Never treat YTD facts as standalone quarters or silently mix incompatible revisions.
- Only documented, compatible, non-overlapping allocations reduce CapEx totals. Keep commitments, estimates, and thematic links separate; show undisclosed residuals.
- Use shared observations, indicators, and event contracts for composability; do not force every Lens into a money-flow view.
- Follow the V1 sequence: one company, accurate ingestion and metrics, one interactive history visualization. Defer full temporal networks and QuantLab until their milestones.
- Label relationships as verified, estimated, or thematic; do not invent financial values.
- Add meaningful tests when calculations or data processing are implemented. Report what was actually verified.
- Keep credentials and downloaded datasets out of version control.
- Update setup instructions when dependencies or runnable commands change.

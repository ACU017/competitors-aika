# Changelog

A running log of changes made to this project. A new entry is added every time a change is made.

## 2026-06-17

- Updated `index.html` from the latest Perplexity export in `Context/` (`aika-competitor-capability-matrix (1).html`). Note: the new export was byte-for-byte identical to the existing `index.html`, so no content actually changed this time.
- Created the `documentation/` folder and this `CHANGELOG.md` to track all future changes.
- **Expanded the matrix from 8 rows to all 45 competitors** from `Context/20260406_Biorce Competitors - Competitor Matrix.csv`. The Perplexity HTML export only contained 8 strategic anchor entries (Status Quo, Veeva, Medidata, Faro Health, QuantHealth, IQVIA, Suvoda, Phesi); those were replaced with the full CSV competitor set.
  - The CSV has no per-feature ratings, so each competitor's Strong/Partial/None rating across the 41 capability features was **inferred** from its "Key Capabilities" / "One-Liner" / "Type" / "Vertical" text. Ratings are conservative working assumptions (consistent with the matrix footer), not vendor-certified audits.
  - 34 of 45 competitors received at least one Strong/Partial rating (34 Strong + 85 Partial cells total). 11 competitors had no taxonomy-relevant evidence (PharmaTrail, Allos, Altrovia, Ancora.ai AG, Kitsa, Puray, Qorra, Sano Genetics, Testmate Health, cogniscreen, QuantHealth) and show as all-gaps rows — several are patient-recruitment/identification tools that don't map to the document-centric feature taxonomy.
  - Row `type` = CSV "Type"; row note = CSV "One-Liner Description". The embedded `rawData` JSON (used by search + Export JSON) was regenerated to match.
  - Updated the header pill from "8 competitor rows" to "45 competitor rows".
  - Regeneration assets saved under `build/` (`build_matrix.py`, `competitors.json`, `coverage_all.json`) so the matrix can be rebuilt or re-rated later.
- **v2 generous re-rate.** The first pass was too sparse (only 6.4% of cells filled, 12 blank rows) because ratings were inferred strictly from the CSV's "Key Capabilities" column alone. Re-ran the assessment with a more generous rubric (`build/rubric_v2.md`) that reads the *full* CSV row (incl. Weaknesses, Target Segment, Vertical) and includes "mapping hints" so adjacent-category tools (patient recruitment, EDC/data capture, trial intelligence, regulatory writing) get honest Partial ratings instead of blank rows.
  - Result: fill density **6.4% → 17.8%** (329 cells: 77 Strong + 252 Partial); blank rows **12 → 4**.
  - The 4 still-blank competitors (Allos, Puray, Qorra, PhaseV) have `Not available`/empty CSV data, so they can't be rated from the CSV — they would need a web-research pass.


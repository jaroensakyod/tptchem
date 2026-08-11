# Lab Safety Scenario Analysis — QA Report v1.0

- **Review date:** 2026-08-11
- **Product ID:** CN-LS-SCENARIO-01
- **Scenario source SHA-256:** `308c4cc922b6537f41669863eb0bffd524069fa996847f2ec978d51b21e5691e`

## Decision

**CONDITIONAL PASS — pilot-ready for internal use; not certified for sale.**

The package passes deterministic content, packaging, and PDF visual checks. It must remain `packaged_pending_qa` in the catalog until a native-English cold read, a certified science-teacher safety review, and a timed classroom pilot are recorded.

## What was checked

- Source contains 10 unique scenarios with complete evidence, risk, safest-first-action, and rationale fields.
- The student framework and key both implement `NOTICE → RISK → ACT → EXPLAIN`.
- Scenario 0 is a separate worked model, so none of the ten scored scenarios is given away.
- The teacher materials include timing, quick-start/sub directions, differentiation, misconceptions, a 3-point rubric, Honors exemplar, CER model, and exit-ticket guidance.
- The student packet excludes keys and is numbered `Student 1 of 6` through `Student 6 of 6`.
- The low-ink packet is a genuine grayscale version and does not rely on color to carry meaning.
- Product, student, low-ink, teacher, and preview PDFs are US Letter, have the expected page counts, and show no clipping, overlap, missing sections, or broken checkbox glyphs in the final render.
- Visible PDF text uses embedded repo-bundled Poppins fonts. Listing images are 1800 × 1800 pixels and show enlarged real pages rather than tiny full-page screenshots.
- The editable DOCX opens structurally, contains all required sections, uses fixed table geometry, and has scrubbed CurioNest metadata. A 12-page native Word render passed visual review before the final copy-only brand/tag correction; the final structural and metadata checks passed after that correction. Word automation then hung twice, so this specific final binary still requires the external cold-read/render gate before certification.

## Safety corrections completed

- Broken glass no longer invents chemical contamination; the key distinguishes cut risk from possible residue only when residue is actually present.
- A skin splash now directs the student to alert the teacher while immediately beginning the room's designated rinse procedure, subject to posted site/SDS exceptions.
- An unattended hot plate now prioritizes staying at the station, a trained and safe normal shutoff, keeping others/combustibles clear, and immediate teacher escalation when it cannot be shut down safely.

Safety language was checked against the ACS Student Laboratory Code of Conduct and ACS secondary-school laboratory safety guidance. District and site policy still takes precedence.

## Automated results

- `qa_lab_safety_scenario_analysis.py`: PASS
- Final PDF page-by-page render review: PASS
- Final listing-image review: PASS
- Repository regression tests: 3 passed, 0 failed
- `qa.py all`: 34 passed, 8 warnings, 0 failed. The warnings concern intentional pending-QA catalog states, one uncataloged pilot directory, pre-existing font/figure provenance work, and a dependency advisory; none is a failure for this package. Any future failure reopens this gate.

## Remaining release gates

1. Native-English cold read for clarity, tone, and age-appropriate US classroom language.
2. Certified chemistry/science teacher review of every safety action against the intended school/site policy.
3. Classroom pilot to verify the stated 45–55 minute core timing and 60–75 minute Honors timing.
4. Record reviewer names, dates, decisions, and any corrections; then rerun all automated and visual QA before changing the catalog status to `certified`.

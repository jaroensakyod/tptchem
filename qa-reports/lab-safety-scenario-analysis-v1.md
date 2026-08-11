# Lab Safety Scenario Analysis - QA Report v1.0

- **Review date:** 2026-08-11
- **Product ID:** CN-LS-SCENARIO-01
- **Scenario source SHA-256:** `820098f1e307b593eeee3353d47525d2c0636e7e5edc6d635f1c0c6e4373aaa1`

## Decision

**FAIL / BLOCKED - all 10 required instructional scenario visuals are missing; not sellable.**

The existing files pass structural, accessibility, Word-open, and render checks, but instructional visual coverage is 0/10. The product is not internally complete and cannot proceed to external certification until the visual gate passes.

## Scope checked

- 10 unique original scenarios with evidence, risk, safest-first-action, and rationale fields.
- Student framework and answer key both use `NOTICE -> RISK -> ACT -> EXPLAIN`.
- Scenario 0 is a separate worked model and does not reveal any scored response.
- Teacher timing, sub-plan directions, differentiation, misconception guidance, rubric, Honors exemplar, CER model, and exit-ticket guidance.
- Master, student, low-ink, teacher, and preview PDFs plus listing images.
- Scenario 10 requires teacher notification for an unattended energized hot plate; a normal control may be used only when the student is trained and it is safe.
- Chem Pride and OpenStax Chemistry 2e are benchmark/reference sources only; no questions, layouts, or images were copied from them.

## Final automated and visual results

- `qa_lab_safety_scenario_analysis.py`: FAIL by design - instructional visual gate is 0/10.
- `qa.py all`: catalog visual-gate warning blocks any claim that the product is complete or certified.
- DOCX accessibility audit: 0 high, 0 medium, 0 low findings.
- Microsoft Word opened the final DOCX read-only and reported 12 pages.
- Product, student, low-ink, teacher, and preview PDFs rendered and were visually inspected page-by-page.
- The clipped Answer Key heading on product page 11 was repaired and re-rendered; no clipping, overlap, unintended blank page, or unreadable content remains.
- `git diff --check`: PASS.

## Remaining release gates

1. Native-English human cold read for clarity and US classroom tone.
2. Chemistry/science teacher review against the intended school/site policy.
3. Classroom pilot or documented teacher dry run for the stated Core and Honors timing.
4. Final page-by-page visual inspection of the editable DOCX in Microsoft Word, with reviewer name/date recorded.

After any correction, rebuild and rerun QA. Only then change the catalog status to `certified`, create the buyer ZIP, extract-test it, and activate the TPT listing.

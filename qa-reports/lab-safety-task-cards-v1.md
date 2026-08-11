# Lab Safety Task Cards - QA Report v1.0

- **Review date:** 2026-08-11
- **Product ID:** CN-LS-TASK-02
- **Card data SHA-256:** `445168f9f08688cd69c5b1f3a906844f4fd959769a07f6ddc8f56c229841ae97`

## Decision

**FAIL / BLOCKED - 12 required instructional visuals are missing; not sellable.**

The existing files pass structural, accessibility, Word-open, and render checks, but instructional visual coverage is only 4/16. The product is not internally complete and cannot proceed to external certification until the visual gate passes.

## Scope checked

- 24 unique original cards, four choices per card, complete key, rationale, and misconception guidance.
- Four instructional portions: Notice and Pause; Choose the Next Move; Communicate and Follow Procedure; Transfer and Repair Misconceptions.
- Master, student, low-ink, teacher, preview, and four standalone portion PDFs.
- Editable DOCX with 4 inline images and 4 non-empty alternative descriptions.
- Four rights-cleared visual placements: CC0 wash bottles, a verified CC0 GHS pictogram, and a CC BY 2.5 hot-plate photograph used twice.
- No code-drawn or ImageGen instructional visual remains in the package.
- T01, T09, and T21 safety corrections are present in source, student cards, and key.
- Chem Pride and OpenStax Chemistry 2e are benchmark/reference sources only; no questions, layouts, or images were copied from them.

## Final automated and visual results

- `qa_lab_safety_task_cards.py`: FAIL by design - instructional visual gate is 4/16.
- `qa.py all`: catalog visual-gate warning blocks any claim that the product is complete or certified.
- DOCX accessibility audit: 0 high, 0 medium, 0 low findings.
- Microsoft Word opened the final DOCX read-only and reported 30 pages.
- All 9 PDFs rendered and were visually inspected page-by-page; no clipping, overlap, unintended blank page, or unreadable content was found.
- `git diff --check`: PASS.

## Remaining release gates

1. Native-English human cold read for clarity and US classroom tone.
2. Chemistry/science teacher review against the intended school/site policy.
3. Classroom pilot or documented teacher dry run for timing and station workflow.
4. Final page-by-page visual inspection of the editable DOCX in Microsoft Word, with reviewer name/date recorded.

After any correction, rebuild and rerun QA. Only then change the catalog status to `certified`, create the buyer ZIP, extract-test it, and activate the TPT listing.

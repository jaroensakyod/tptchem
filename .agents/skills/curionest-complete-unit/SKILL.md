---
name: curionest-complete-unit
description: Build, revise, audit, render, package, or continue CurioNest U.S. chemistry complete-unit products without lowering the established instructional, typography, visual-rights, assessment, and release baseline. Use for chapter units, student packets, lesson slides, tests A/B, teacher keys, previews, TPT listings, PDF rebuilds, visual-asset additions, QA, release evidence, or model handoffs in the tpt-pilot repository.
---

# CurioNest complete unit

Preserve product quality across model changes by treating repository policy and deterministic QA as the source of truth. Never rely on conversation memory alone.

## Load the governing files

At the repository root, read these files completely before taking product action:

- `product-lines/complete-unit-quality-baseline.json` — locked measurable minimums.
- `product-quality-standard.md` — instructional, rights, assessment, print, and human-release gates.
- `product-lines/complete-unit-instruction-standard.md` — package and lesson architecture.
- `product-lines/instructional-visual-policy.md` — when visuals are mandatory and which sources are allowed.
- `docs/TPT-PRODUCT-RELEASE-CHECKLIST.md` — release and upload sequence.

For chapter status and previous decisions, also read `plans/chapter-production-queue.json`, `plans/repeatable-production-plan.json`, `catalog.json`, and the relevant product's `source/source.json`, `assets/manifest.json`, `docs/QA-REPORT.md`, and `docs/RELEASE-EVIDENCE.md`.

Resolve conflicts in this order: explicit current user instruction, locked quality baseline, product quality standard, complete-unit architecture, visual policy, release checklist, older notes.

## Hold the quality lock

- Require `quality_contract_version` in source and catalog metadata.
- Treat every number in `complete-unit-quality-baseline.json` as a floor or exact package contract as labeled.
- Do not reduce type sizes, visual coverage, teaching components, practice, assessments, answer support, source evidence, QA checks, or human gates to make content fit or to finish faster.
- Add or reflow pages when necessary. Do not solve overflow by shrinking below the typography baseline.
- Change the contract only after the user explicitly approves the exact policy change; then update its version, governing documents, source metadata, catalog metadata, generator, QA, and release evidence together.

## Follow the production workflow

1. Inspect the branch, dirty worktree, product status, and existing evidence. Preserve unrelated user changes.
2. Research current U.S. scope and terminology from official or primary sources. Use benchmark worksheets only for broad topic/workflow comparison.
3. Write original American-English instruction, examples, practice, distractors, tests, rationales, teacher guidance, and page composition in `source/source.json`.
4. Verify teach/practice/assessment alignment. Every tested skill must have been taught and practiced; every target must receive formative and summative coverage.
5. Make an item/page-level visual decision. Use a functional visual whenever observation, equipment, scale, particles, hazards, structure, or spatial reasoning matters. Record a defensible reason when a lesson remains text-only.
6. Download only commercially compatible free/open visuals from stable international repositories. Retain the asset, provenance page, creator, license, access date, placement, and evidence snapshot. Do not generate or code-draw instructional substitutes.
7. Build all seven buyer PDFs from the common source with the shared generator. Keep student answers out of student files and keep the teacher key complete.
8. Render every buyer PDF and preview page after the final content change. Compare all component pages with the complete PDF. Inspect full-size pages and contact sheets for clipping, overlap, weak hierarchy, excessive blank space, undersized type, stretched images, low contrast, and insufficient answer space.
9. Build the three 1600 × 1600 listing images only from delivered pages. Make every count and claim match the files exactly.
10. Package exactly the seven declared buyer PDFs. Do not include source, internal QA, research, or seller notes in the buyer ZIP.
11. Scan the exact final ZIP with Microsoft Defender, record scanner/version, result, date, and SHA-256, and rerun the scan after any ZIP-changing rebuild.
12. Run product QA and repository QA. Fix failures at the source, rebuild, rerender, repackage, rescan, and rerun checks.
13. Keep status at `draft_pending_teacher_review` until named reviewers approve the native-English cold read, U.S. chemistry/science review, and classroom dry run on the final files.

## Use the standard commands

Use the configured workspace Python runtime. Substitute the relevant product directory for `<product>`.

```powershell
python <product>\source\build_pdf.py
python tools\render_complete_unit_release.py <product> --pdftoppm <path-to-pdftoppm> --replace
python tools\curionest_complete_unit_listing.py <product>
python <product>\source\package_release.py
python <product>\source\qa_product.py
python qa.py
```

Use `tools/make_pdf_contact_sheets.py` for visual review. Record the final render manifest and component parity. Run the Defender command separately because the exact scanner path is platform-specific.

## Stop instead of degrading

- Stop with `BLOCKED` if a required visual or rights record is missing.
- Stop with `FAIL` if content, calculation, key, rationale, or assessment coverage is uncertain.
- Stop with `FAIL` for clipping, overlap, unreadable type, unsupported blank space, false listing claims, or a mismatched preview.
- Stop before certification if any human gate is pending.
- Never claim guaranteed sales, zero account risk, formal standards alignment without review, or platform approval.

## Deliver evidence

Report what changed, exact page and asset counts, render review status, product QA totals, repository QA totals, Defender result and ZIP hash, and remaining human gates. Link the complete PDFs, previews, ZIPs, upload checklists, and release evidence. Do not describe a draft as ready to sell while human gates remain pending.

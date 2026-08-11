# CurioNest TPT Chemistry Production Pipeline

Repository for original U.S. high-school chemistry teaching resources for Teachers Pay Teachers.

The model-independent entry point is [`AGENTS.md`](AGENTS.md) and the project skill at [`.agents/skills/curionest-complete-unit/SKILL.md`](.agents/skills/curionest-complete-unit/SKILL.md). The locked measurable baseline is [`product-lines/complete-unit-quality-baseline.json`](product-lines/complete-unit-quality-baseline.json). The authoritative inventory is [`catalog.json`](catalog.json).

## Current complete-unit products — 2026-08-11

| Product ID | Unit | Automated state | Publication state |
|---|---|---|---|
| `CN-CH01-MATH` | Math and Measurement | QA `263/263`; 107/107 final PDF pages rendered; Defender pass | Blocked pending three human gates |
| `CN-CH02-MATTER` | Introduction to Matter | QA `271/271`; 107/107 final PDF pages rendered; Defender pass | Blocked pending three human gates |

Both products are PDF only, US Letter, American English, and branded CurioNest with this exact line:

`© 2026 CurioNest · For classroom use only`

## Mandatory complete-unit sequence

`Engage → Teach → Model → Guided Practice → Independent Practice → Exit Ticket → Cumulative Mixed Review → Unit Test A/B`

A worksheet or test cannot be the first student encounter with new content. Each lesson must include explicit teaching, a complete worked example, scaffolded practice, independent practice, and feedback support. Assessment comes after instruction and review.

## Visual and source rules

- Use an instructional visual when the task depends on appearance, equipment, particles, setup, spatial relationships, or observable evidence.
- Instructional visuals must come from documented free/open international sources with commercial-use-compatible rights and product-level credit records.
- Do not use AI-generated or code-drawn instructional images.
- ChemPride is only a broad topic/workflow benchmark. Do not copy or adapt its wording, questions, answers, files, screenshots, art, layout, or sequence.
- The local *Chemistry 2e* PDF is excluded from direct commercial adaptation under the current source gate.
- Buyer-facing products must not use CHEM P'M branding or publisher text.

## Product package structure

```text
products/<product>/
  source/                  original source JSON and thin builder wrappers
  assets/                  visual files, manifest, and license evidence
  docs/                    listing copy, rights record, QA, release evidence
  output/buyer-files/      exactly seven current buyer PDFs
  output/tpt-upload/       ZIP, preview, three listing images, seller documents
  output/qa/               page renders and parity evidence; never upload
```

Each complete unit delivers:

- 51-page complete PDF
- 15 projectable lesson slides
- 12 student lesson, practice, and review pages
- Unit Test A and Unit Test B, 20 multiple-choice items per form
- 13-page teacher guide and answer key with rationales and repair moves
- 2-page rights and sources PDF

## Build and verify a unit

Run the wrappers inside the selected product package:

```powershell
python source/build_pdf.py
python source/build_listing_assets.py
python source/package_release.py
python source/qa_product.py
```

The reusable implementations are in `tools/`. Final release also requires rendering every page, inspecting the complete file and preview, scanning the exact ZIP, recording its SHA-256, and then rerunning QA.

## Human release gates

Automated PASS does not authorize publication. Every unit remains blocked until all three reviews are documented in `docs/RELEASE-EVIDENCE.md`:

1. Native/U.S. English cold read.
2. Independent U.S. chemistry/science teacher review of every prompt, answer, rationale, calculation, grade fit, and standards statement.
3. Classroom dry run covering projection, printing, timing, directions, and answer space.

Only after those gates pass should the seller create a draft TPT listing, download it as a buyer would, compare it with the local package, and activate it.

# CurioNest Product Quality Standard v2.1

> Mandatory release standard for every CurioNest TPT product. Version 2.1 adds a model-independent quality lock on 2026-08-11.

## Core promise

CurioNest sells classroom-ready instruction, not pages of unsupported questions. A product may use the words `lesson`, `unit`, `complete`, or `core pack` only when it contains an explicit teaching sequence, supported practice, assessment, complete keys, teacher guidance, and verified rights.

Automated QA never authorizes publication. A product may be listed only after all automated gates and the three human gates are approved.

## Model-independent quality lock

- Every model or agent must begin with `AGENTS.md` and `.agents/skills/curionest-complete-unit/SKILL.md`.
- `product-lines/complete-unit-quality-baseline.json` is the machine-readable minimum for complete units.
- Source and catalog metadata must name the active `quality_contract_version`; automated QA must reject missing or stale versions.
- Never lower a typography minimum, visual minimum, instructional component, assessment requirement, QA gate, or human gate to make a build pass.
- A lower minimum or removed gate requires explicit user approval, a new contract version, and synchronized changes to policy, generator, QA, source, catalog, and release evidence.

## Required learning sequence (G0)

Every chapter unit must follow this sequence:

`Engage -> Teach -> Model -> Guided Practice -> Independent Practice -> Formative Check -> Mixed Review -> Summative Assessment`

For every lesson:

1. State a measurable learning target and prerequisite.
2. Begin with a phenomenon, data point, image, prediction, or prior-knowledge prompt.
3. Teach the concept in student-friendly American English.
4. Define essential vocabulary in context.
5. Include at least one fully worked example or modeled reasoning path.
6. Include guided practice that names the scaffold or thinking step.
7. Include independent practice that requires transfer, not copied arithmetic.
8. End with an exit ticket or other observable formative check.
9. Provide a teacher-facing answer, likely misconception, and specific repair action.

A chapter unit must also contain:

- a pacing guide and teacher moves;
- a cumulative mixed review after all lessons;
- a multiple-choice summative test after instruction and practice;
- two equivalent test forms (A and B) for retakes/test security;
- four plausible, parallel choices per multiple-choice item;
- a keyed rationale for every answer and a misconception note when useful;
- at least one application, data, model, or evidence-based item in each test form.

Stop release if a tested skill was not explicitly taught and practiced, or if a taught learning target is never assessed.

## U.S. science design (G0-S)

- Use U.S. Grades 9-10 expectations, American English, and US Letter pages.
- Use a coherent learning progression rather than disconnected worksheets.
- Embed formative checks throughout instruction; do not rely only on the final test.
- Use phenomena, models, data, and evidence when they materially support sensemaking.
- Distinguish `supports NGSS practices` from a formal NGSS performance-expectation alignment claim.
- Do not claim NGSS alignment unless a documented three-dimensional alignment review is complete.

## Chemistry accuracy (G1)

- Verify every definition, equation, unit, numerical result, distractor, and rationale.
- Recalculate quantitative answers independently from the keyed result.
- Record accepted conventions and any scientifically reasonable alternate response.
- Freeze source content by hash after review; any content change requires rerunning chemistry QA.
- Do not publish an item the seller cannot solve and explain aloud.

## Language and accessibility (G2)

- Use natural American English, concise teacher language, and grade-appropriate vocabulary.
- Define necessary academic language; avoid decorative jargon and generic AI phrasing.
- Keep prompts unambiguous and choices grammatically parallel.
- Avoid trick questions, cultural assumptions, and unnecessary reading load.
- Provide sufficient writing space and readable print contrast.
- A native-English cold read remains mandatory before publication.

## Product completeness (G3)

Every complete chapter unit must include:

- cover;
- teacher quick-start and pacing;
- projectable lesson slides or equivalent teacher-led teaching pages;
- student teaching notes and practice;
- cumulative review;
- Unit Test A and Unit Test B;
- teacher guide and full answer key;
- terms, rights, and sources;
- preview PDF and at least three truthful listing images;
- listing copy, upload checklist, QA report, release evidence, malware result, and package hash.

PDF-only products are allowed when the listing states PDF-only. Never advertise an editable file that is not delivered and render-verified.

## Instructional visual gate (G3-V)

- Write an item-level visual plan before layout.
- If an item asks students to identify equipment, read a scale, interpret particles, recognize a hazard, inspect a structure, or reason spatially, include a functional visual.
- Use internationally recognizable free/open sources that permit commercial use. Record source URL, creator, license, downloaded file, and local license evidence.
- Do not use AI-generated instructional images or code-drawn substitutes for this product line.
- Layout shapes, rules, numbering, and answer areas are allowed; they are not instructional art.
- A decorative image never satisfies a required instructional visual.
- Block release when a required visual or rights record is missing.

## Assessment gate (G3-A)

For each test form, automated QA must verify:

- the required number of unique items;
- exactly four choices per item;
- exactly one keyed best answer;
- no answer-position pattern longer than three;
- coverage of every stated learning target;
- no assessment item outside taught scope;
- no verbatim reuse between Forms A and B;
- rationales for all items;
- comparable skill coverage and difficulty between forms;
- answer keys separated from student test files.

Multiple choice is one measure, not the entire learning experience. Guided reasoning, independent application, and formative checks remain required before the final test.

## Rights, originality, and platform compliance (G4)

- Brand buyer-facing files exactly as `CurioNest`.
- Use the exact line `© 2026 CurioNest · For classroom use only`.
- Do not place CHEM P'M, CHEM_PM, ChemPride, OpenStax, or another publisher name in buyer-facing content except where a license legally requires attribution and has been approved.
- ChemPride may inform only broad topic architecture and classroom workflow. Never copy or adapt its questions, answers, wording, art, screenshots, distinctive layouts, or packet sequence.
- The local Chemistry 2e PDF is blocked from direct authoring and commercial adaptation.
- Write original questions, examples, explanations, distractors, and page composition.
- Answer TPT's AI disclosure truthfully. Do not promise sales, formal endorsement, or zero account risk.
- Listing claims must match the exact files and page counts in the buyer ZIP.
- Scan the exact final ZIP and record SHA-256 after every rebuild.

## Visual and print QA (G5)

- US Letter, embedded fonts, consistent margins, page numbers, and edition labels.
- Render every final PDF page to PNG after the last content change.
- Reject clipped text, overlap, broken symbols, low-resolution visuals, unreadable choices, ambiguous answer space, blank pages, or accidental extra pages.
- Inspect listing images at full resolution and thumbnail size.
- Preserve a calm print-first hierarchy; avoid repetitive dashboard cards and decorative clutter.

## Duplicate-product gate (G6)

- Document the instructional purpose, audience, format, assessed skills, and prompt inventory.
- A new SKU must differ in learning task or classroom use, not only title, colors, or rearranged questions.
- Never reuse scored prompts across separately listed products without clearly disclosed bundle relationships.

## Human release gates (G7)

All three decisions must be recorded as `APPROVED` after reviewing the final rebuilt files:

1. Native-English cold read.
2. U.S. chemistry/science teacher review of content, level, assessment, and safety.
3. Classroom dry run with observed timing and usability notes.

Any correction reopens affected automated gates. Until all three are approved, status remains `draft_pending_teacher_review` and publication is blocked.

## Required status flow

`idea -> researched -> scoped -> authored -> built -> qa_content -> qa_visual -> automated_complete_human_review_pending -> certified -> published`

## Definition of done

A chapter is finished for automated production only when:

- G0 through G6 pass;
- all final files are rebuilt from the same source;
- every page is visually reviewed;
- listing and package inventories match;
- the exact final ZIP passes malware scan and its hash is recorded;
- catalog, chapter queue, and release evidence are updated;
- G7 remains visibly blocking until real reviewers approve it.

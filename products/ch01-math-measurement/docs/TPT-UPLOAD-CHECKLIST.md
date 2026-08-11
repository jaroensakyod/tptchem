# TPT Upload Checklist — CN-CH01-MATH

## Automated package gate

- [x] Build the PDFs from `source/source.json`.
- [x] Render every page of every final PDF and inspect the 51-page complete file plus the 6-page preview.
- [x] Build and inspect all three 1600 × 1600 listing images.
- [x] Run `source/qa_product.py`; every automated check must pass.
- [x] Package exactly seven buyer PDFs in the ZIP.
- [x] Scan the exact final ZIP with current Microsoft Defender.
- [x] Record the exact ZIP SHA-256 and scan result in `RELEASE-EVIDENCE.md`.

## Exact buyer inventory

- [x] `CurioNest_CH01_Math_and_Measurement_Complete.pdf` — 51 pages
- [x] `CurioNest_CH01_Math_and_Measurement_Lesson_Slides.pdf` — 15 pages
- [x] `CurioNest_CH01_Math_and_Measurement_Student_Guided_Notes_and_Practice.pdf` — 12 pages
- [x] `CurioNest_CH01_Math_and_Measurement_Unit_Test_A.pdf` — 4 pages
- [x] `CurioNest_CH01_Math_and_Measurement_Unit_Test_B.pdf` — 4 pages
- [x] `CurioNest_CH01_Math_and_Measurement_Teacher_Guide_and_Answer_Key.pdf` — 13 pages
- [x] `CurioNest_CH01_Math_and_Measurement_Rights_and_Sources.pdf` — 2 pages

## Three human gates — required before publishing

- [ ] Native/U.S. English reviewer checks grammar, tone, directions, terminology, and listing copy.
- [ ] U.S. chemistry/science teacher independently solves every scored item and checks every answer, rationale, calculation, grade fit, and standards statement.
- [ ] Classroom dry run checks printing, projection, timing, answer space, directions, and preview-to-product match.
- [ ] Names, qualifications, dates, findings, repairs, and decisions are recorded in `RELEASE-EVIDENCE.md`.

## Rights and truth-in-listing gate

- [x] Every instructional visual matches `assets/manifest.json`; creator, license, URL, use, and access date are recorded.
- [x] No benchmark worksheet, textbook exercise, screenshot, wording, answer, image, or layout is reproduced.
- [x] Listing counts match the delivered files exactly.
- [x] The preview and listing images are made from pages included in the product.
- [x] The listing says PDF only and makes no unverified standards, sales, or platform-safety guarantee.
- [x] No external purchase, delivery, contact, or off-platform sales link appears in buyer-facing content.

## TPT draft and release

- [ ] Upload the ZIP, preview PDF, three listing images, and listing copy from `output/tpt-upload/`.
- [ ] Keep **Make Listing Active** unchecked during verification.
- [ ] Download the uploaded product as a buyer would and open every file.
- [ ] Compare the downloaded inventory, title, preview, description, and counts with the local evidence.
- [ ] Activate only after all automated, human, account, and rights checks are approved.
- [ ] Archive the exact uploaded files, listing copy, hash, scan result, and review evidence.

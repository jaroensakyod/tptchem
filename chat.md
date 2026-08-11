# บันทึกการตัดสินใจและมาตรฐานโปรเจกต์ TPT Chemistry

อัปเดต: 2026-08-11

เอกสารนี้สรุปสิ่งที่ตกลงกันจากการทำงานร่วมกัน เพื่อใช้เป็นบริบทสำหรับคนและ agents ในรอบถัดไป ไม่ใช่ transcript คำสนทนาแบบคำต่อคำ

## เป้าหมายของโปรเจกต์

สร้างชุดแบบฝึกหัด STEM สำหรับนักเรียนสหรัฐฯ ที่มีคุณภาพเพียงพอสำหรับขายบน Teachers Pay Teachers โดยต้อง:

- ตรงกับสิ่งที่นักเรียนเรียนจริงในช่วงเวลานั้น
- เทียบหลักสูตร หนังสืออ้างอิง และตัวอย่างแบบฝึกหัดคุณภาพก่อนเขียน
- ใช้โจทย์ คำอธิบาย ภาพ และเฉลยต้นฉบับ
- มีสิทธิ์เชิงพาณิชย์ของภาพ ฟอนต์ และข้อมูลชัดเจน
- ใช้งานง่ายสำหรับครู มี student file, teacher guide, complete key และ preview ที่ตรงกับไฟล์จริง
- หนึ่งหัวข้อพัฒนาเป็นอย่างน้อย 10 รูปแบบที่มีหน้าที่การสอนต่างกันจริง
- ผ่าน content, safety, rights, language, answer, visual/print และ listing QA ก่อนขาย

## ปัญหาที่พบในงานเดิม

งาน Lab Safety รุ่นก่อนยังไม่เหมาะสำหรับขาย เพราะภาพอุปกรณ์วาดอย่างหยาบ ไม่ช่วยวัดความเข้าใจจริง การจัดวางดูบาง และเฉลยยังไม่รองรับเหตุผลของนักเรียนเพียงพอ

มาตรฐานใหม่จึงกำหนดว่า:

- ห้ามวาดอุปกรณ์วิทยาศาสตร์แบบเดาเมื่อรูปร่างมีผลต่อการจำแนกหรือความปลอดภัย
- อุปกรณ์, GHS, กราฟ, scale, diagram และภาพเชิงปริมาณต้องใช้ verified vector, deterministic code หรือ asset ที่ตรวจสิทธิ์แล้ว
- ImageGen ใช้ได้กับภาพบริบทหรือบรรยากาศที่ไม่ต้องการความแม่นยำเชิงเทคนิคเท่านั้น
- ถ้าภาพไม่เพิ่มการเรียนรู้ ไม่ต้องใส่ภาพเพื่อเติมพื้นที่
- ภาพหน้าขายต้องแสดงหน้าจริงแบบขยาย อ่านได้เมื่อเป็น thumbnail และห้ามอ้างสิ่งที่ไม่มีในสินค้า

## สิ่งที่ต้องวิจัยก่อนสร้างสินค้า

1. ตรวจว่านักเรียน US เรียนอะไรในช่วงปัจจุบันจาก official district/state/course sources หลายแหล่ง
2. หาแบบฝึกหัดแจกฟรีที่มีคุณภาพเพื่อศึกษาโครงสร้างและระดับความคิด
3. เทียบ pacing/standards, textbook scope และ worksheet exemplars
4. ระบุ curriculum gap และประโยชน์ที่สินค้าของเราจะเติม
5. ตรวจ license แยกจากคุณภาพของแหล่งอ้างอิง

คำว่า free หรือ classroom use ไม่ได้แปลว่านำมาดัดแปลงขายได้ แหล่ง NC, ND, classroom-only หรือไม่มี commercial permission ใช้เป็น benchmark เท่านั้น

## ข้อสรุปด้านเนื้อหา ณ สิงหาคม 2026

### Chemistry

สำหรับ General/Honors Chemistry ช่วงเปิดเทอม หลายเขตเริ่มด้วย Chemistry Foundations หรือ Unit 0 ได้แก่ lab safety, laboratory equipment, SI measurement, significant figures, scientific notation, dimensional analysis และ density ก่อน atomic theory

AP Chemistry ต้องแยกเป็นสายสินค้าเฉพาะ ไม่ควรนำ pacing ของ General Chemistry ไปอ้างแทน

### Biology

ลำดับแรกที่ควรพัฒนาหลัง Chemistry คือ Cells as Systems, membrane transport, osmosis และ data analysis พร้อม model/data/CER tasks

### Physics

ลำดับแรกคือ Kinematics Graphing Boot Camp: motion maps, position-time/velocity-time graphs, scalar/vector, units และ experimental reasoning

### Mathematics

ต้องแยกตาม grade/course:

- Grade 6: number fluency, fractions และ decimals
- Grade 7: rational numbers และ expressions/equations
- Grade 8: real number system, exponents และ scientific notation
- Algebra 1: ทำ edition แยกตาม sequence ของหลักสูตร ไม่รวมเป็น grades 6–8 แบบกว้าง

โอกาสเฉพาะปี 2026–27 คือ AP Statistics ฉบับปรับใหม่ห้าหน่วยและการฝึกตอบในรูปแบบดิจิทัล

ห้ามอ้าง pacing ของเขตเดียวว่าเป็น nationwide pacing และ NGSS Middle School ต้องอธิบายว่าเป็น grade-band expectation

## Product family chassis

หนึ่งหัวข้อใช้มาตรฐาน 14 รูปแบบ:

1. Scenario/problem analysis worksheet
2. Visual guided notes หลายระดับ
3. Task cards แบบ print/digital
4. Stations circuit
5. No-lock escape challenge
6. Picture reveal/maze/color-by-code
7. Sorting/matching/domino
8. Scavenger hunt/gallery walk
9. Reading/case study/CER sub plan
10. Practical/performance task
11. Quiz/Test Form A–B + retake
12. Digital self-checking
13. Project/choice board + rubric
14. Spiral review/cumulative challenge

แต่ละรูปแบบต้องเปลี่ยนงานทางความคิดหรือสถานการณ์ใช้งาน ไม่ใช่ย้ายคำถามเดิมไปใส่การ์ดหรือเปลี่ยนสี

สร้าง mini bundle หลัง 4 รูปแบบแรกผ่าน QA และสร้าง full-topic bundle เมื่อมีอย่างน้อย 10 รูปแบบที่ผ่าน QA จริง

## ลำดับผลิต Lab Safety

1. Scenario Analysis
2. Task Cards
3. Stations
4. Visual Guided Notes
5. Digital Self-Check
6. Sort/Domino
7. No-Lock Escape Challenge
8. Picture Reveal
9. Reading + CER
10. Quiz A/B + Retake
11. Practical Assessment
12. Project + Rubric
13. Scavenger Hunt
14. Spiral Review

ห้ามเร่งสร้างรูปแบบถัดไปเมื่อรูปแบบปัจจุบันยังมีปัญหา content, safety, rights, answer key หรือ visual QA เพราะข้อผิดพลาดจะกระจายทั้งสายสินค้า

## สินค้าแรกที่สร้างแล้ว

- ชื่อ: **Lab Safety Scenario Analysis: Make the Safe Call**
- กลุ่มเป้าหมาย: Grades 9–11 General/Honors Chemistry
- เวลา: Core 45–55 นาที; Honors 60–75 นาที

โครงคิดของนักเรียน:

1. Evidence noticed
2. Risk / possible harm
3. Safest first action
4. Why the action reduces risk

แพ็กเกจมี:

- 10 original scenarios และ Scenario 0 สำหรับตัวอย่าง
- Student Tool
- Core และ Honors extension
- Exit ticket
- Full key สำหรับ evidence, risk, action และ why
- 3-point rubric, Honors exemplar, CER model และ misconception notes
- Student-only PDF, low-ink/B&W PDF, teacher guide/key PDF, preview และ editable DOCX
- ภาพปกและภาพ listing ที่ใช้หน้าจริงของสินค้า ไม่ใช้รูปอุปกรณ์วาดแบบเดา

## การแก้ Safety ที่สำคัญ

- Broken glass: ไม่สมมติว่ามี chemical contamination เมื่อสถานการณ์ไม่ได้ระบุ
- Skin splash: แจ้งครูพร้อมเริ่ม designated rinse procedure ทันที เว้นแต่ posted site/SDS procedure ระบุเป็นอย่างอื่น
- Hot plate: อยู่ที่สถานี ใช้ normal control ปิดเมื่อได้รับการฝึกและปลอดภัย กันผู้อื่น/วัสดุติดไฟออก และแจ้งครูทันทีเมื่อปิดอย่างปลอดภัยไม่ได้
- Site policy, teacher direction และ current SDS มีลำดับเหนือข้อความทั่วไปในทรัพยากร

## สถานะคุณภาพ

สินค้าแรกผ่าน deterministic package QA, การตรวจ PDF ทุกหน้า, การตรวจ listing และ regression tests แล้ว แต่สถานะยังเป็น:

**Conditional / pilot-ready — not certified for sale**

ก่อนเปลี่ยนเป็น certified ต้องมี:

1. Native-English cold read
2. Certified chemistry/science teacher safety review
3. Classroom timing pilot
4. บันทึก reviewer/date/decision และ rerun QA ทุกชุด

ห้ามเปลี่ยน catalog เป็น certified จนกว่าจะมีหลักฐานครบ

## ขั้นตอนทำงานซ้ำ

1. Demand and pacing research
2. Rights and source ledger
3. Standards × textbook × exemplar crosswalk
4. Product brief และ item blueprint
5. Original authoring + independent answer check
6. Build editable/print/student/teacher/preview files
7. Blind content and safety audit
8. Render ทุกหน้าและตรวจ full size + thumbnail + B&W
9. บันทึก QA decision
10. Pilot, revise, certify และจึงค่อย publish

รายละเอียดปฏิบัติอยู่ใน `docs/STEM-TPT-PRODUCTION-MANUAL.md`, แผนแบบเครื่องอ่านได้อยู่ใน `plans/repeatable-production-plan.json` และผลตรวจสินค้าชิ้นแรกอยู่ใน `qa-reports/lab-safety-scenario-analysis-v1.md`

## การสั่ง Agents

แยกขอบเขตเพื่อให้ตรวจสอบกันได้:

- Research agent: current pacing, standards และ official URLs
- Rights agent: license/terms และ provenance
- Curriculum agent: standards × textbook × assessment crosswalk
- Authoring agent: original item bank จาก brief
- QA agent: blind audit คำตอบ ความกำกวม ความปลอดภัย และ key coverage
- Visual QA agent: ตรวจ render ทุกหน้าและ thumbnail
- Main agent: รวมผล แก้ source ตัดสิน status และอนุมัติ release

ตัวอย่างคำสั่ง:

```text
Research current August pacing for US Grade 10 Biology from at least three official district/state sources. Return dates, unit order, URLs, and product implications. Do not write product questions.
```

```text
Blind-audit this item bank. Check intended answers, defensible alternatives, grade-level language, misconceptions, safety, and answer-key coverage. Do not edit files; report blockers first.
```

```text
Inspect every rendered page at full size and thumbnail size. Report clipping, hierarchy, writing space, print contrast, page-number problems, and listing mismatches.
```

## งานถัดไป

ปิด native-English, U.S. chemistry-teacher และ classroom dry-run gates ของ Chapter 1–2 ก่อน จากนั้นจึงเริ่มวิจัย Chapter 3 ตาม `plans/chapter-production-queue.json` งาน Lab Safety แยกออกจากลำดับ chapter unit นี้

## Permanent production decision - 2026-08-11

- Use `https://chempride.weebly.com/` as the permanent base benchmark for chemistry topic order, classroom workflow rhythm, and package architecture.
- Treat ChemPride as `benchmark_only`. Never copy or adapt its questions, wording, answers, art, screenshots, distinctive layouts, or packet sequence.
- Split every chemistry topic into distinct product formats using the 14-format catalog; each format must change the cognitive task or classroom use, not merely restyle the same questions.
- For a chapter-unit SKU, the first sellable build must be a complete teaching unit. A short visual worksheet may exist only as a separate secondary format and must not replace explicit teaching, modeled examples, practice, review, and assessment.
- Every item/page receives a Visual Plan. When visual evidence is required, use a verified free-source commercial-use asset with provenance. Do not use AI-generated or code-drawn substitute images. Missing required visuals mean `BLOCKED`.
- The authoritative working map is `product-lines/chempride-topic-format-map.md`; it supersedes older notes that conflict with this decision.

## First ChemPride-based product example - 2026-08-11

- Completed the automated package build for `products/math-measurement-visual-worksheet/` as the first CurioNest example. It is not certified for sale until human release gates pass.
- Product: Chemistry Measurement Lab Tools & Density Visual Worksheet, Grades 8-10, English, US Letter.
- Package includes 4 student pages, 4-page teacher key, teacher quick-start, editable DOCX, rights/source file, 3-page preview, 3 listing images, listing copy, upload checklist, and one TPT-ready ZIP.
- Visual gate passed 4/4 using Public Domain and CC BY 3.0 source images; no AI-generated or code-drawn instructional image is used.
- Automated product QA passed with zero product-specific failures and is registered as `CN-MM-VISUAL-01` in `catalog.json` with status `draft_pending_teacher_review`.

## U.S. worksheet release corrections - 2026-08-11

- Target all new TPT student-facing chemistry resources to U.S. students unless a brief explicitly says otherwise: American English, US Letter, U.S. grade bands, and Name/Date/Class Period fields.
- Student response lines and teacher answers are mutually exclusive render states. Never place an answer box or answer text over a student line, prompt, border, or image.
- Retire CHEM P'M from this TPT line. CurioNest is the rights holder/brand and must never be presented as an instructional content reference.
- Every buyer-facing file uses the exact rights line `© 2026 CurioNest · For classroom use only`.
- ChemPride remains an internal topic/workflow benchmark only. Do not present it as a buyer-facing content authority and do not copy or adapt its protected content or layout.
- Use official U.S. content references for buyer-facing scope checks (for example NIST, ACS, and NGSS practices).
- Required instructional images must come from international/public repositories with explicit commercial-use-compatible rights and direct provenance, such as Wikimedia Commons or Bioicons/Servier. Do not use AI-generated, code-drawn, or locally copied worksheet images as substitutes.

## TPT marketplace account-safety decision - 2026-08-11

- Automated QA never means ready to sell. `certified` requires native-English review, Chemistry/Science teacher review, a classroom pilot/dry run, named reviewers, dates, corrections, and a rerun of all QA.
- ChemPride remains `benchmark_only`; public access does not create reuse rights.
- The local OpenStax Chemistry 2e PDF is `blocked_direct_ai_and_commercial_reuse` until exact-version rights are proven. Never upload, paste, extract, or otherwise provide it to generative AI.
- Every non-original visual requires creator, direct URL, license, access date, exact placement, and a retained license snapshot. This product line uses verified free-source visuals only; no AI-generated or code-drawn instructional substitutes.
- One resource may have only one TPT listing unless a separate product is substantively different and the listing explains the similarities and differences.
- Before upload: extract/open every buyer file, run render QA, scan the final ZIP with Microsoft Defender, record SHA-256, back up the exact ZIP/listing/rights/reviewer evidence outside TPT, and complete `RELEASE-EVIDENCE.md`.
- Account identity/tax/payout data must match the rights holder. Never share the seller password; assistants use TPT VA Login only.
- Keep an incident pack per SKU so a report or suspension can be answered with the exact uploaded ZIP, hash, listing snapshot, rights ledger, reviewer evidence, malware result, and factual timeline.

## Complete instructional unit decision - 2026-08-11

- A chapter product must teach before it asks students to practice: `Engage -> Teach -> Model -> Guided Practice -> Independent Practice -> Exit Ticket -> Cumulative Mixed Review -> Unit Test A/B`.
- Each chapter unit contains five lessons, fifteen projectable slides, twelve student lesson/practice/review pages, two 20-item multiple-choice test forms, complete rationales, teacher guidance, and a rights record unless a later brief explicitly raises the requirement.
- A tested skill must have been explicitly taught and practiced. A stated learning target must be checked formatively and represented in the assessment blueprint.
- Final buyer inventory is PDF only unless another format is separately built, rendered, verified, and truthfully listed.
- Every final PDF page must be rendered after the last content change. Component pages must match the complete file, and the preview/listing images must use delivered product pages.
- Automated completion ends at `automated_complete_human_review_pending`; it never changes the product to `certified` without the three real human reviews.
- The governing files are `product-quality-standard.md` v2.1 and `product-lines/complete-unit-instruction-standard.md`; they supersede worksheet-first notes for chapter-unit products.

## Model-independent quality lock - 2026-08-11

- Any replacement LLM or agent must begin with `AGENTS.md` and `.agents/skills/curionest-complete-unit/SKILL.md` before changing a CurioNest chemistry product.
- `product-lines/complete-unit-quality-baseline.json` version `2026-08-11.1` preserves the accepted typography, visual coverage, package counts, instructional sequence, assessment structure, and release gates in machine-readable form.
- Source and catalog records must carry the same `quality_contract_version`; deterministic QA must fail when the version is missing, stale, or the baseline is weakened.
- No model may reduce type sizes, visuals, instruction, practice, assessment support, rights evidence, render checks, malware checks, or human gates merely to finish faster or make a layout fit.
- Lowering a minimum requires explicit user approval, a contract version change, and synchronized updates to the policies, generator, QA, product source, catalog, and release evidence.

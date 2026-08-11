# คู่มือระบบผลิตสื่อ STEM สำหรับ TPT

เวอร์ชัน 1.0 - 2026-08-11

## เป้าหมาย

สร้างสินค้าสำหรับนักเรียนสหรัฐฯ ที่ตรงช่วงเวลา ตรงหลักสูตร ใช้งานได้จริง มีสิทธิ์เชิงพาณิชย์ชัดเจน และทำซ้ำเป็นสายสินค้าได้ โดยหนึ่งหัวข้อมีอย่างน้อย 10 รูปแบบที่มีหน้าที่ทางการสอนต่างกันจริง และวางโครงมาตรฐานไว้ 14 รูปแบบ

## สถานะงานมาตรฐาน

`idea -> researched -> scoped -> authored -> built -> qa_content -> qa_visual -> pilot_ready -> certified -> published`

- ห้ามขายงานก่อน `certified`
- ถ้าพบข้อผิดพลาดหลัง build ให้ย้อนกลับไปแก้ source แล้ว build ใหม่ ห้ามแก้เฉพาะ PDF
- ทุกสถานะต้องมีวันที่ ผู้ตรวจ และหลักฐานใน QA log

## ขั้นตอนทำซ้ำต่อหนึ่งหัวข้อ

### 1. Demand research

1. ระบุวันที่ ฤดูกาล เกรด วิชา และชนิดชั้นเรียน เช่น general, honors, AP
2. ตรวจ pacing guide ปัจจุบันอย่างน้อย 3 แหล่ง โดยให้มี district/state/official source
3. แยกสิ่งที่ “ต้องเรียน” ออกจากสิ่งที่ “ขายดี”
4. บันทึก URL วันที่เข้าถึง ช่วงเวลาที่สอน และผลต่อสินค้า
5. ถ้าข้อมูลอาจเปลี่ยน ให้ค้นใหม่ทุก 90 วัน หรือก่อนฤดูกาลขาย 6-8 สัปดาห์

ผลลัพธ์: `research/YYYY-MM-subject-topic-demand.md`

### 2. Reference triangulation

เทียบข้อมูล 3 ชั้นก่อนเขียนโจทย์:

| ชั้น | ใช้ตอบคำถาม | ตัวอย่าง |
|---|---|---|
| Standards/pacing | เด็กต้องเรียนอะไรและเมื่อไร | district map, NGSS, state standards |
| Reference text | ขอบเขต ศัพท์ ลำดับ และระดับความยาก | NIST, ACS, IUPAC, official course framework, or an OER whose exact-version rights permit the intended commercial/AI use |
| Worksheet exemplars | กิจกรรมที่ใช้งานง่ายหน้าตาเป็นอย่างไร | AACT, PhET, peer-reviewed OER |

ห้ามยึดแหล่งเดียวเป็นทั้งหลักสูตร เนื้อหา และแบบฝึกหัด

### 3. Rights screening

จัดทุกแหล่งลงหนึ่งสถานะ:

- `facts_only`: ใช้ตรวจข้อเท็จจริงและ scope เท่านั้น
- `benchmark_only`: ศึกษาโครงสร้าง แต่ห้ามคัดลอก/ดัดแปลง
- `commercial_reuse_with_attribution`: ใช้ได้เมื่อทำ attribution ตามเงื่อนไข
- `public_domain_or_cc0`: ใช้ได้และยังต้องเก็บ provenance
- `blocked`: ห้ามเข้าสินค้า

คำว่า free, downloadable หรือ classroom use ไม่เท่ากับสิทธิ์ขายต่อ ถ้าไม่ชัดให้ถือเป็น `benchmark_only`.

### 3.1 ChemPride base rule for chemistry

For chemistry products, use `https://chempride.weebly.com/` as the permanent base benchmark for topic mapping, classroom workflow rhythm, and student/teacher/answer-key package architecture. Its rights status is `benchmark_only`: do not copy or adapt questions, wording, answers, images, screenshots, distinctive layout, or packet sequence. Write all sellable content independently as original CurioNest material.

For this chemistry worksheet line, the verified free-source visual rule overrides any later general option that mentions ImageGen or code-drawn substitutes: required instructional visuals must come from documented commercial-use sources, or the work remains `BLOCKED`.

Before a topic enters production, map it in `product-lines/chempride-topic-format-map.md`, select a genuinely different cognitive task from the 14-format catalog, complete the item-level Visual Plan, and build a 4-page Student/Tutor proof. Expand only after the proof passes rights, content, visual, and print QA.

### 3.2 OpenStax Chemistry 2e restriction

The current OpenStax Chemistry 2e page states a CC BY-NC-SA license and prohibits ingestion into generative AI without permission. The local `chemistry2e.pdf` therefore has status `blocked_direct_ai_and_commercial_reuse` until the exact file/version and its commercial permissions are documented. Do not upload, paste, extract, or otherwise provide that PDF to an LLM. Do not copy or adapt its text, questions, answers, figures, or distinctive instructional sequence into a paid product.

### 4. Topic brief

กำหนดก่อนสร้าง:

- buyer และ student grade
- learning targets 2-5 ข้อ
- prerequisite
- เวลาใช้จริง
- Core/Support/Honors pathway
- misconception ที่ต้องตรวจ
- ภาพ/diagram ที่จำเป็น พร้อมแหล่งสิทธิ์
- จำนวนข้อและชนิดคำตอบ
- Definition of Done

ใช้ `templates/product-brief-template.md`.

### 5. Product-family design

ต่อหนึ่งหัวข้อสร้างอย่างน้อย 10 รูปแบบจากรายการมาตรฐาน 14 แบบ:

1. Scenario/problem analysis worksheet
2. Guided notes หลายระดับ
3. Task cards
4. Stations circuit
5. No-lock escape room
6. Color/picture reveal
7. Sorting/matching/domino game
8. Scavenger hunt
9. Reading/close reading/sub plan
10. Practical/performance task
11. Quiz/test A-B-retake
12. Digital self-checking version
13. Project/choice board พร้อม rubric
14. Spiral review/cumulative challenge

แต่ละแบบต้องเปลี่ยน “งานทางความคิด” หรือ “สถานการณ์ใช้” ไม่ใช่แค่เปลี่ยนสีหรือย้ายโจทย์เดิมลงการ์ด

### 6. Authoring

1. เขียนโจทย์และเฉลยใน source ที่อ่านได้ด้วยเครื่องก่อน
2. ระบุ correct answer, acceptable alternatives, rationale และ misconception
3. ทำ answer-key completeness check ก่อนจัดหน้า
4. คำนวณตัวเลข/หน่วยด้วย independent check สำหรับ Math/Physics/Chemistry
5. Biology ต้องตรวจความถูกต้องของ label, scale, process direction และ exceptions
6. Safety/health content ต้องใช้ authoritative current source และมี site-policy disclaimer

### 7. Visual asset selection

- ทำ Visual Plan ระดับ item/page ก่อน authoring: ระบุ `required` หรือ `not required`, learning purpose, asset type, source/license และสถานะ
- งาน observation, hazard recognition, equipment identification, spatial setup, symbols และ particle/model interpretation ต้องมีภาพที่นักเรียนใช้เป็นหลักฐาน
- `not required` ต้องมีเหตุผลเชิงการเรียนรู้เฉพาะข้อ ห้ามใช้เหตุผลกว้าง ๆ ว่า text เพียงพอหรือหาภาพไม่ได้
- ถ้าภาพที่จำเป็นยังไม่มีสิทธิ์ใช้เชิงพาณิชย์ ให้หยุดงานไว้ที่ `BLOCKED`; ห้ามลดโจทย์เป็น text-only เพื่อให้ผ่าน QA
- จำนวน required/completed/missing visuals ต้องถูกบันทึกใน source, catalog visual gate และ QA report
- สัญลักษณ์และอุปกรณ์มาตรฐาน: ใช้ verified SVG/PNG จากแหล่งตรวจสอบได้
- กราฟ สมการ scale และ diagram เชิงปริมาณ: ใช้ deterministic code/native vector
- ภาพบริบท: ใช้ภาพที่มี commercial license หรือ ImageGen เมื่อช่วยการเรียนจริง
- ห้ามให้ ImageGen สร้าง GHS, สูตร, label, ตัวเลข, แผนภาพเชิงปริมาณ หรืออุปกรณ์ที่ต้องจำแนกอย่างแม่นยำ
- บันทึก asset ใน `assets-manifest.json` ก่อนนำเข้าไฟล์ขาย

### 8. Build and package

แพ็กขั้นต่ำ:

- editable source/DOCX/PPTX ตามชนิดสินค้า
- print-ready US Letter PDF
- student-only file เมื่อเหมาะสม
- full answer key
- teacher guide
- source/rights/TOU page
- cover และ preview ที่แสดงหน้าจริง

### 9. QA gates

#### G1 Content

- target ตรง standards/pacing
- ทุกข้อมีคำตอบเดียวที่ตั้งใจ หรือระบุคำตอบสมเหตุผลอื่น
- หน่วย ตัวเลข สูตร label และเหตุผลถูกต้อง
- ไม่สอนพฤติกรรมที่ไม่ปลอดภัยหรือขัด site policy

#### G2 Language

- ภาษาอังกฤษเป็นธรรมชาติ เหมาะกับเกรด และคำสั่งทำได้โดยไม่ต้องเดา
- ใช้ศัพท์สม่ำเสมอ
- ไม่มีคำฟุ่มเฟือยหรือข้อความจาก AI ที่ไม่เพิ่มการเรียนรู้

#### G3 Rights

- ทุก asset และ reference มี ledger
- ไม่มี NC/ND/classroom-only content ถูกดัดแปลงขาย
- attribution ครบตาม license

#### G4 Answer and usability

- ทุกข้อที่ให้คะแนนอยู่ใน key
- key ตรงหมายเลขและเวอร์ชัน
- เวลาใช้จริงสมเหตุผล
- มี support/core/honors หรือเหตุผลชัดเจนว่าไม่จำเป็น

#### G5 Visual/print

- render และตรวจทุกหน้า ไม่ดูแค่ text extraction
- ไม่มี clip, overlap, orphan heading, font substitution หรือหน้าว่างโดยไม่ตั้งใจ
- ขนาดตัวอักษร student body โดยทั่วไปไม่น้อยกว่า 9 pt
- พื้นที่เขียนสอดคล้องกับความยาวคำตอบ
- อ่านได้ทั้งสีและขาวดำ; margin ปลอดภัยสำหรับเครื่องพิมพ์โรงเรียน

#### G6 Listing integrity

- title, grade, time, pages, file types และสิ่งที่รวมตรงกับไฟล์จริง
- preview ไม่เปิดเผย key ทั้งหมดและไม่มี claim เกินจริง
- ห้ามนับ cover, TOU, key หรือ color duplicate เพื่อพอง page count

#### G7 Marketplace/account safety

- ไม่มี duplicate/cosmetic relisting; variant ต้องต่างเชิงสาระและอธิบายความต่างใน listing
- ไม่มี external sales links, required buyer accounts หรือ lower/free duplicate elsewhere
- final ZIP แตกทดสอบ เปิดทุกไฟล์ สแกนด้วย approved antivirus และบันทึก SHA-256
- account identity, tax and payout information ตรงกับเจ้าของสิทธิ์จริง; ผู้ช่วยใช้ TPT VA Login เท่านั้น
- มี backup และ incident pack ต่อ SKU นอก TPT
- automated QA ไม่เปลี่ยนสถานะเป็น `certified` แทน human release gates

### 10. Release decision

- `PASS`: ทุก gate ผ่านและไม่มี blocker
- `CONDITIONAL`: ใช้ pilot ได้ แต่ยังห้ามขาย; ระบุสิ่งค้างและผู้รับผิดชอบ
- `FAIL`: มี factual, safety, rights, key หรือ rendering defect

## Definition of Done ต่อหนึ่ง format

- source สร้างใหม่ได้ deterministically
- PDF เปิดได้และขนาด US Letter
- ตรวจภาพครบทุกหน้าและเก็บ QA record
- Visual Plan ครบทุก item/page และ required visuals มีจริงครบ 100%; ถ้าขาดแม้หนึ่งรายการให้เป็น `FAIL/BLOCKED`
- answer coverage 100%
- ไม่มี unverified asset
- มี differentiation หรือ implementation note
- student instructions ผ่าน cold-read
- status ใน catalog/plan ตรงความจริง
- `RELEASE-EVIDENCE.md` ครบ human signoffs, malware result, ZIP hash และ seller authorization

## การใช้ agents

ให้แต่ละ agent มีขอบเขตแยกกันและห้ามแก้ source เดียวกันพร้อมกัน:

- Research agent: หา current pacing, standards และลิงก์
- Rights agent: ตรวจ license/terms แยกจากคุณภาพเนื้อหา
- Curriculum agent: ทำ crosswalk standards x textbook x assessment
- Authoring agent: เขียน item bank จาก brief โดยไม่เปิดต้นแบบที่อาจทำให้ลอกภาษา
- QA agent: ตรวจคำตอบและความกำกวมแบบ blind review
- Visual QA agent: ตรวจภาพ render ทุกหน้าและ thumbnail
- Main agent: ตัดสินใจ แก้ source รวมผล และอนุมัติ status

ตัวอย่างคำสั่ง:

```text
Research current August pacing for US Grade 10 Biology from at least three official district/state sources. Return dates, unit order, URLs, and product implications. Do not write product questions.
```

```text
Blind-audit this item bank. Check one intended answer, alternate defensible answers, grade-level language, misconceptions, and answer-key coverage. Do not edit files; return blockers first.
```

```text
Inspect every rendered page at full size and thumbnail size. Report clipping, weak hierarchy, insufficient writing space, print contrast, page-number problems, and any mismatch with the listing.
```

## รอบการทำงานรายสัปดาห์

- Monday: demand and standards refresh
- Tuesday: author source + independent answer check
- Wednesday: build format 1 and content QA
- Thursday: visual QA, student/teacher split, preview
- Friday: revise, certify or keep conditional, then update analytics hypothesis

เริ่ม format ถัดไปได้เมื่อ format ปัจจุบันผ่าน content, rights, answer และ visual gates แล้วเท่านั้น

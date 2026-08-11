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

ปิด human/classroom gates ของ Scenario Analysis ก่อน จากนั้นจึงเริ่ม **Lab Safety Task Cards** เป็นรูปแบบที่ 2 โดยเขียนสถานการณ์และงานคิดใหม่ ไม่คัดลอกคำถาม 10 ข้อจากรูปแบบที่ 1

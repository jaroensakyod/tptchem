# ChemNest Product Quality Standard v1.0

> มาตรฐานบังคับก่อนขึ้นร้าน TPT ทุกชิ้น — แก้ไขได้โดย owner เท่านั้น (version bump)
> อนุมัติ: 2026-08-09 · ใช้กับ pilot ชิ้นแรกเป็น Certified Product #CN-AB-001

## หลักการ

1. **ครูซื้อเพราะไว้ใจ** — สินค้าทุกชิ้นต้อง "ผ่านประตูตรวจ" ครบ 4 ประตู ก่อนขึ้นร้าน ไม่มีข้อยกเว้น
2. **Risk-based ไม่ใช่ตรวจเท่ากันหมด** — แบ่ง tier ตามปริมาณภาษาที่ต้องเสี่ยง (ไม่งั้นขยาย 3,349 ข้อไม่จบ)
3. **ตรวจครั้งเดียวให้จบ** — ทุกการแก้ต้อง log ไว้ กันแก้ซ้ำที่เดิม
4. **มาตรฐาน = moat** — กันคู่แข่ง AI slop (TPT demote คุณภาพต่ำ) และเป็นเหตุผลที่ครูเลือกเรา

## สถานะสินค้า (pipeline)

```
draft → translated → lang_qa (G2) → packaged (G3) → certified (G4) → published
```

- ขายได้เฉพาะ status = **certified** ขึ้นไป
- ทุกสถานะมี log (product-qa-log.md หรือ JSON)

## 4 ประตู (Gates)

### G1 — Chemistry Gate (สืบทอดจาก chem-pm-unified)
- ข้อต้องมี `review.chemistry_status = approved` จาก bank ต้นทาง (QA 2 รอบ: Codex chemistry QA + second-pass)
- ห้ามแก้เนื้อหาเคมีหลัง freeze (SHA-256 ของ batch) โดยไม่ผ่าน review ใหม่
- **ตรวจ:** source batch + review trail ตรงกัน

### G2 — Language Gate (ใหม่)
- ภาษาอังกฤษต้องเป็นธรรมชาติแบบเจ้าของภาษา: grammar, word order, ไม่มี "AI-ism" (ประโยคอวยพรซ้ำ, คำฟุ่มเฟือย, ศัพท์ผิดบริบท)
- **ศัพท์ต้องตรง glossary-th-en.md 100%** (ห้าม pH บางชิ้น pOH บางชิ้นใช้คนละคำ)
- ตัวเลข/หน่วย/สูตร/LaTeX ต้องไม่เพี้ยนจากการแปล
- **ตรวจตาม tier:**
  - Tier A (numeric MC, สูตรล้วน): sample 10% + glossary check
  - Tier B (MC ทั่วไป): 100% ภาษา + ทวนเคมีเบา
  - Tier C (short_answer / written_solution): 100% + ทวนคำตอบเชิงคำนวณ + misconception
- Residual risk: ก่อน publish ครั้งแรกของร้าน ควรมีเจ้าของภาษาอ่านทวนทั้งชิ้น 1 รอบ (บันทึกใน log)

### G3 — Product Gate (ใหม่)
- ไฟล์ขาย (product PDF) ครบ: cover + **หน้า Welcome (cover letter ถึงครู — จำเป็นทุกชิ้น ตามธรรมเนียม US sellers)** + TOU + เนื้อหา + answer key
- Answer key ครบทุกข้อ (20/20) + มีคำอธิบาย + misconception
- Review card / teacher guide ตามชนิดสินค้า
- Difficulty ระบุชัด (dots ●○○/●●○/●●●) — สนับสนุนการ differentiate
- Preview images ครบ (อย่างน้อย 3: cover, ตัวอย่างเนื้อหา, ตัวอย่างเฉลย)
- PDF เปิดได้, ฟอนต์ฝัง (ไม่เพี้ยนบนเครื่องครู), ไม่มีแท็กหลุด, US Letter
- ตรวจด้วย pipeline: build ผ่าน + pypdf ตรวจหน้า/แท็ก + vision/มนุษย์ดู layout
- **Roadmap ตามคู่แข่ง (EazyScience):** reading passage ต่อสินค้า (รูปแบบที่ครูซื้อจริง — "independent reading activity") · เวอร์ชัน B&W (ประหยัดหมึก) · real-world connections ในเนื้อหา (ครูชมในรีวิว)

### G4 — Compliance Gate (ใหม่)
- **AI disclosure:** ตอบตามจริงในขั้นตอนอัปโหลด TPT (AI-assisted) + description กล่าวถึง QA ไม่ใช่โฆษณา AI
- **ลิขสิทธิ์:** ฟอนต์ OFL เท่านั้น (Google Fonts ✓) · รูป/ไอคอนสร้างเองหรือ CC · ห้ามคลิปอาร์ต/ตัวการ์ตูนติดลิขสิทธิ์
- **Benchmarking Policy:** ศึกษาโครงสร้าง/ฟีเจอร์/ราคาของร้านขายดีได้ (บันทึกใน tpt-benchmark.md) แต่ห้ามก็อปเนื้อหา/ข้อความ/ดีไซน์/ภาพ/ชื่อร้านของใคร — ห้ามดาวน์โหลดไฟล์ร้านอื่นมาแกะ (DMCA + แบนร้าน)
- TOU อยู่ในไฟล์ (single-teacher license)
- หมวดหมู่/เกรด/แท็ก/ราคา ครบตาม tpt-listing-pack.md
- ไม่มีข้อความ "ฉาบฉวย" แบบ AI slop (ชมตัวเองซ้ำ, คำสัญญาเกินจริง)

## Risk Tiers

| Tier | ประเภทข้อ | ตรวจภาษา | ตรวจเคมี |
|---|---|---|---|
| A | numeric (มี value/unit/tolerance) | sample 10% + glossary | ทวนตัวเลขย้อนกลับ (sample) |
| B | multiple_choice ทั่วไป | 100% | ทวนคำตอบ + เอกฐานตัวเลือก |
| C | short_answer / written_solution | 100% | ทวนเต็ม + misconception |

## Checklist ต่อชิ้น (คัดลอกลง product-qa-log.md ทุกชิ้น)

```
[ ] G1: source batch + chemistry_status=approved
[ ] G2: แปลครบ ไม่มี AI-ism · glossary ตรง · tier ตามชนิดข้อ
[ ] G3: PDF ครบ structure · key ครบ · preview ครบ · ฟอนต์ฝัง
[ ] G4: disclosure · ลิขสิทธิ์ · TOU · หมวด/แท็ก/ราคา
[ ] build + verify: ALL PASS (script)
[ ] (ครั้งแรกของร้าน) เจ้าของภาษาอ่านทวน 1 รอบ
```

## KPI

- 0 บั๊กภาษา/เคมีที่เกิดจากรีวิว 1 ดาว
- ค่าเฉลี่ยรีวิว ≥ 4.8★
- ทุกชิ้นที่ publish ต้องมี log ครบ 4 ประตู

## Anti-AI-look Checklist (กัน "ดูเหมือน AI ทำ" — ตรวจทุกชิ้นก่อน publish)

| # | ตรวจ | ผ่านเมื่อ |
|---|---|---|
| 1 | Cover ไม่ซ้ำแบบกับชิ้นอื่นในร้าน | layout/องค์ประกอบต่างกันตามชนิดสินค้า (worksheet / digital / bundle) |
| 2 | ภาษาไม่เป็น "AI-ism" | ผ่าน glossary §"ห้ามใช้" + อ่านแล้วเหมือนครูเขียน (contraction, พูดตรงกับครู) |
| 3 | มี "สัมผัสครู" อย่างน้อย 2 อย่าง | misconception / review card / teacher tip / ตัวอย่างเจาะจง / ลายมือ (Caveat) |
| 4 | เนื้อหาถูกต้อง (ไม่มีรอย AI มั่ว) | G1-G2 ผ่าน + สุ่มตรวจตัวเลขย้อนกลับ |
| 5 | "Teacher-voice pass" | อ่าน description + หน้าแรกของไฟล์ออกเสียงแล้วฟังดูเป็นคน (ไม่ใช่โบรชัวร์) |
| 6 | มีเรื่องมนุษย์ในร้าน | bio "About the author" มีเรื่องจริง (ครู/ผู้เชี่ยวชาญ/แรงจูงใจ) ไม่ใช่ประโยคgeneric |
| 7 | ไม่มี "AI บอกให้ครูทำอะไร" ที่ห่วย | ตรวจ Q&A/คำแนะนำในสินค้า ว่าเป็นคำแนะนำที่ครูจริงจะใช้ |

> หมายเหตุ: รีวิวจากครูจริงคือสัญญาณ "ไม่ใช่ AI slop" ที่แรงที่สุด — freebie + คุณภาพ = เครื่องมือหลัก ไม่ใช่แค่ดีไซน์

## แหล่งอ้างอิง

- glossary-th-en.md (ศัพท์มาตรฐาน)
- tpt-listing-pack.md (การตั้งค่า listing + นโยบาย AI)
- product-qa-log.md (ประวัติการตรวจรายชิ้น)

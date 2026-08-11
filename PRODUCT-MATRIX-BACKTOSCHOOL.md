# 🏭 CurioNest Product Matrix — 1 หัวข้อ = หลายรูปแบบ (เพิ่มโอกาสขาย)

> หลักการ (จากผู้ใช้ 2026-08-10): **ห้ามผลิตแบบเดียวจบ** — ทุกหัวข้อต้องทำหลายรูปแบบ
> เพราะ: (1) ติด search หลายคำ (2) ครูแต่ละคนชอบรูปแบบต่างกัน (3) เก็บรีวิวหลายทาง
> (4) bundle ได้ทีหลัง (รายได้ต่อลูกค้าสูงขึ้น)

---

## 📐 MATRIX: หัวข้อ Back-to-School × รูปแบบสินค้า

| รูปแบบ | Lab Safety | Sig Figs & Measurement | Scientific Method | Matter (Phys/Chem) | Atomic Structure |
|---|---|---|---|---|---|
| **A. Lesson Pack** (แนวคิด+ตัวอย่าง+ฝึก) | ✅ | ✅ | ✅ | ✅ | ✅ |
| **B. Worksheet Pack** (โจทย์ล้วน+เฉลย) | ✅ | ✅ | ✅ | ✅ | ✅ |
| **C. Scavenger Hunt / Game** | ✅ | ✅ | ✅ | — | ✅ |
| **D. Doodle / Visual Notes** | — | ✅ | ✅ | — | ✅ |
| **E. Quiz + Answer Key** (ตรวจเร็ว) | ✅ | ✅ | ✅ | ✅ | ✅ |
| **F. Freebie** (lead magnet 1 หน้า) | ✅ | — | ✅ | ✅ | — |

**เป้าหมาย: อย่างน้อย 3 รูปแบบ/หัวข้อ** (A/B/E = core + C/D = differentiate + F = free)

---

## 🧰 SKILL INVENTORY — เรามีเครื่องมือทำครบไหม?

### ✅ มีครบ (ใช้ได้เลย)
| Skill | ใช้ทำอะไร |
|---|---|
| `us-chemistry-curriculum` | หลักสูตร/ศัพท์/patterns US (OpenStax) |
| `chem-equations` + `omml.py` | สมการเคมี Word-native ($...$ OMML + \ce) |
| `chem-figures` + `chem_figures.py` | ภาพ deterministic: matplotlib (กราฟ/scale), RDKit (โมเลกุล); ไม่ใช้วาด clipart อุปกรณ์ |
| verified SVG assets | อุปกรณ์/GHS มาตรฐาน พร้อม source/creator/license ใน `assets-manifest.json` |
| ImageGen | เฉพาะภาพบริบทที่ช่วยการเรียน; ไม่สร้างฉลาก สูตร GHS หรืออุปกรณ์สำหรับ identification |
| `math-equations` | สมการคณิต OMML |
| `build_mirror_pack.py` | Lesson Pack (schema: concept/practice/vocab/answer_key) |
| `build_complete_pack.py` | Worksheet Pack (reading+MCQ+calc+short) |
| `build_colorbynumber.py` | Color-by-number (รูปแบบ D ทางเลือก) |
| `build_worksheet.py` | Worksheet ธรรมดา |
| `tpt-product-design-language` | ฟอนต์/สี/เลย์เอาต์ TPT |
| `tpt-channel-ops` | อัปโหลด/ตั้งร้าน browser |
| `humanizer` | ภาษาให้เป็นธรรมชาติ (เสียงครู) |
| `tpt-digital-products` / `tpt-printable-products` | แนวทางการผลิตขาย TPT |
| `docx` / `pdf` / `powerpoint` | ผลิตไฟล์หลายชนิด |
| `excalidraw` | แผนภาพแนวคิด (ถ้าต้องการ doodle) |
| `hormozi-product-design` / `product-offer-design` | ออกแบบ offer/ราคา |

### ⚠️ สถานะ implementation ปัจจุบัน
| ช่องว่าง | ต้องทำอะไร | วิธีแก้ |
|---|---|---|
| **Scavenger Hunt builder** | ✅ มี `build_scavenger_hunt.py` + demo JSON | เพิ่ม regression test และสร้างสินค้าจริง |
| **Doodle/Visual notes builder** | ยังไม่มี | ใช้ layout-native shapes + verified SVG + `chem_figures.py` ตาม §G3-V |
| **Quiz (แบบเร็ว) builder** | ✅ มี `build_quiz.py` + demo JSON | เพิ่ม regression test และสร้างสินค้าจริง |
| **Google Slides/PPTX variant** | ✅ มี `build_ppt_pack.py` | ต้อง QA layout และทดสอบกับ schema รุ่นใหม่ |
| **Reproducible QA** | ✅ มี `qa.py` ระดับ source/package | ยังต้องเพิ่ม render-based visual regression |

### 📌 สรุป 2026-08-10

Builder core มีครบแล้ว แต่ยังไม่ถือว่า production-ready จนกว่าจะ rebuild สินค้า
ปัจจุบัน, ทดสอบ output และผ่าน `qa.py all --strict` งานเร่งด่วนจึงเป็น QA และ
packaging ไม่ใช่สร้าง builder เพิ่ม ส่วน Doodle/Visual notes ยังเป็นช่องว่างจริง

---

## 🎯 แผนผลิต 5 หัวข้อ × 3 รูปแบบ = 15 สินค้า (+5 freebie)

### หัวข้อ 1: Lab Safety (เดือนนี้ hot สุด #43)
- [ ] A. Lesson Pack: Lab Safety Complete Lesson Pack (กฎ+อุปกรณ์+สัญลักษณ์ GHS) — $3.50
- [ ] B. Worksheet Pack: Lab Safety Rules Worksheet + Answer Key — $3.00
- [ ] E. Quiz: Lab Safety Quiz (20 ข้อ MCQ + เฉลย) — $2.50
- [ ] F. Freebie: Lab Safety Rules Poster (1 หน้า) — $0.00
- [ ] (C เพิ่มเติม: Lab Equipment Scavenger Hunt — $3.00)

### หัวข้อ 2: Measurement, Sig Figs & Dimensional Analysis
- [ ] A. Lesson Pack: Measurement & Sig Figs Complete Lesson — $4.00
- [ ] B. Worksheet Pack: Sig Figs Practice (60+ ข้อ) — $3.50
- [ ] E. Quiz: Sig Figs & Unit Conversion Quiz — $2.50
- [ ] D: Sig Figs Doodle Notes — $3.00 (ถ้าเวลาพอ)

### หัวข้อ 3: Scientific Method
- [ ] A. Lesson Pack: Scientific Method Complete Lesson — $3.50
- [ ] B. Worksheet Pack: Scientific Method Practice — $3.00
- [ ] C. Scavenger Hunt: Scientific Method Stations — $3.50 (ต่าง!)
- [ ] F. Freebie: Scientific Method Graphic Organizer — $0.00

### หัวข้อ 4: Physical & Chemical Properties of Matter
- [ ] A. Lesson Pack: Properties & Changes of Matter — $3.50
- [ ] B. Worksheet Pack: Physical vs Chemical Changes (พร้อมตัวอย่างจริง) — $3.00
- [ ] E. Quiz: Matter Properties Quiz — $2.50
- [ ] F. Freebie: Matter Classification Chart — $0.00

### หัวข้อ 5: Atomic Structure (กันยายน)
- [ ] A. Lesson Pack: Atomic Structure Complete Lesson — $4.00
- [ ] B. Worksheet Pack: Protons/Neutrons/Electrons Practice — $3.00
- [ ] C/D: Atomic Structure Crack-the-Code / Doodle — $3.50

---

## ⏱️ ลำดับผลิต (เร่งด่วน → ช้า)

1. **Lab Safety ครบชุด** (A+B+E+F) — สัปดาห์นี้ (Back-to-School peak!)
2. **Scientific Method** (A+B+C+F)
3. **Sig Figs & Measurement** (A+B+E)
4. **Matter Properties** (A+B+E+F)
5. **Atomic Structure** (A+B+C) — กันยายน

---

## 🤖 กฎสำหรับ Teacher Agent (เพิ่มใน DESIGN.md)

1. **ทุกหัวข้อ ≥ 3 รูปแบบ** — ห้ามผลิตแบบเดียวจบ
2. **เช็ค skill inventory ก่อนเริ่ม** — ถ้าขาด builder ให้สร้างก่อน (ไม่ใช่ทำแบบที่ถนัด)
3. **keyword research ทุกหัวข้อ** — ใช้ TPT Search Trends + ตรวจคู่แข่งจริงก่อนตัดสินใจ
4. **product calendar** — ผลิตตามฤดูกาล (ตอนนี้ = Back-to-School; ตุลาคม = Halloween Chem)
5. **freebie ทุกชุด** — อย่างน้อย 1 ชิ้นฟรีต่อหัวข้อ (lead magnet เก็บ follower)

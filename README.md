# CurioNest TPT Chemistry — Production Pipeline

> สินค้าครูเคมี (Teachers Pay Teachers) — สร้างโดยระบบ AI pipeline ครบวงจร
> Brand: **CurioNest** · Seller: phuwasit yodkantha · ล้อ OpenStax Chemistry 2e + ChemPride Regents

---

## 📦 สรุปงานทั้งหมด (2026-08-10)

### 1. สินค้า 6 ชิ้นแรก (Acid-Base, ล้อ OpenStax Ch 14) — ✅ เสร็จ ถูกแทนที่
- Mirror packs b01-b06 (เนื้อหา + โจทย์ล้อเล่ม + เฉลย) — **ปัจจุบันถูกแทนที่ด้วยระบบใหม่แล้ว**

### 2. Builder ระบบ (4 ตัว — ใช้จริง)
| Builder | ผลิต | สถานะ |
|---|---|---|
| `build_mirror_pack.py` | Unit packs / worksheets (รองรับ Regents layout เต็ม) | ✅ verified |
| `build_ppt_pack.py` | PowerPoint decks (JSON → pptxgenjs → .pptx) | ✅ verified |
| `build_quiz.py` | Standalone quizzes (MCQ/TF/calc + เฉลย) | ✅ verified |
| `build_scavenger_hunt.py` | Station hunts (clues → answer sheet) | ✅ verified |
| `omml.py` | LaTeX → Word OMML (สมการคณิต/เคมี) — **แก้ 3 บั๊กจบ** (\, \text \dfrac) | ✅ verified |

### 3. Skills (ระบบความรู้ — 13 สกิล orchestrated)
- **`tpt-master`** 🆕 — Master playbook: pipeline 10 ขั้น + กฎบังคับ + verification checklist
- **`tpt-ppt-products`** 🆕 — ราคา/โครงสร้าง Guided Notes (research จาก ChemKate จริง)
- **`us-chemistry-curriculum`** — OpenStax chapter map ch01-15 + โจทย์จริง (ch01/ch02 เพิ่มใหม่)
- chem-figures / chem-equations / math-equations / docx / powerpoint / pdf + 6 สกิล TPT

### 4. Research ที่ทำ
- **ChemPride Unit 1** (chempride.weebly.com) — โหลด 4 ไฟล์จริง: notes 28p + practice 21p + regents 3p + answer key → blueprint โครงสร้าง Regents
- **ChemKate TPT** — ราคาจริง: PPT lesson $4-6 · Unit bundle $10-15 · curriculum $200-290 · full-year $400-500
- **Regents Atomic packet** — โครงสร้าง 27 หน้า (Assess Yourself / vocab table / LESSON ALL CAPS / objective box / data table / Regents practice 1-4)

### 5. รูป (กฎใหม่: ห้ามวาดเอง — ใช้ของฟรี)
- **NFPA 704 diamond** — Wikimedia Commons **Public domain** → Chrome headless render ✅
- **GHS symbols 10 แบบ** — Bioicons UNECE ทางการ (CC-0) → Chrome render ✅
- **Lab apparatus 8 ชิ้น** — Bioicons CC-0 (Xavax/OpenClipart) → Chrome render ✅
- Pipeline: SVG ฟรี → Chrome headless → PIL grid compose (resvg/cairosvg พังบน Windows)

### 6. สินค้าปัจจุบัน (รอตรวจ)
- **Chapter 1: Math & Measurement** — `products/ch01-math-measurement/` (10 หน้า)
  - vocab ตาราง Word|Definition (แบบ ChemPride)
  - 5 lessons (Measurement / Sig Figs / Density / Scientific Notation / Dimensional Analysis)
  - worked example ทุก lesson + OMML fractions (สมการ stacked)
  - Regents Practice 8 ข้อ (ตัวเลือก 1-4 แบบ NY exam)
  - Answer key + cover + preview 3 หน้า
  - ✅ verification ALL PASS (schema 28 ข้อ / OMML 8 / m:f 4 / ไม่มี LaTeX leak / vision ผ่าน)

---

## 🛠️ วิธีใช้งาน (Developer)

```bash
# สร้างสินค้า
cd tpt-pilot
PYTHONPATH= C:/Users/ASUS/miniconda3/python.exe build_mirror_pack.py mirror-json/<name>.json <name>

# ตรวจ (สร้าง temp script ใต้ Temp เสมอ — prefix hermes-verify-)
# QA เลข → build → ตรวจ OMML XML → vision check → package products/<name>/
```

## 📁 โครงสร้าง

```
tpt-pilot/
├── build_*.py          # 4 builders + omml.py (สมการ)
├── chem_figures.py     # รูป pipeline
├── mirror-json/        # schema สินค้า (ch01-math-measurement.json ฯลฯ)
├── products/           # สินค้าสำเร็จรูป (pdf + docx + cover + preview)
├── figures/            # รูป (Wikimedia PD / Bioicons CC-0 / grid ประกอบ)
├── research-*.pdf      # research คู่แข่ง (ChemPride / Regents / INRS)
└── *.md                # เอกสารแผน (STORE-SETUP / PRODUCT-MATRIX / TEACHER-AGENT-DESIGN)
```

## ⚠️ กฎสำคัญ (user-mandated)
1. **ล้อหนังสือ** — โหลด skill `us-chemistry-curriculum` ก่อนเขียน JSON เสมอ
2. **ห้ามวาดรูปเอง** — ใช้ Wikimedia PD / Bioicons CC-0 → Chrome render
3. **สมการ = OMML** (`$...$` → omml.py) — ห้าม plain text
4. **Regents MCQ = ตัวเลือก 1-4** (ไม่ใช่ A-D)
5. **US Letter** เสมอ · preview = 3 หน้าแรก · 1 หัวข้อ ≥ 3 รูปแบบ + freebie

---

© 2026 CurioNest — For classroom use only

# Product QA Log — CurioNest

## Catalog reconciliation — 2026-08-10

| Product ID | Package | Status | Blocking evidence |
|---|---|---|---|
| `CN-CH01-MATH` | `products/ch01-math-measurement/` | `draft_pending_teacher_review` | automated QA 89/89, PDF/listing visual QA and Defender pass; native-English review, U.S. chemistry teacher review, classroom dry run pending; DOCX excluded |
| `CN-CH01-ESSENTIAL` | `products/ch01-essential-ideas/` | `packaged_pending_qa` | rebuild DOCX/PDF, full-page visual QA, native-English review, attribution verification |

สองรายการนี้เป็นสินค้าปัจจุบันตาม `catalog.json` และยังไม่ certified ส่วน
`CN-AB-001` ด้านล่างเป็น historical QA record ซึ่งไม่มี package/source path ตาม
โครงสร้าง catalog ปัจจุบัน จึงใช้เป็นหลักฐานสำหรับสองสินค้าข้างบนไม่ได้

- 2026-08-10: regenerate cover ทั้งสองชุดด้วย `build_listing_assets.py` แล้ว
- 2026-08-10: ตรวจ cover PNG 1200×1200 ด้วยภาพจริง ไม่พบข้อความล้นหรือถูกตัด

## Chemistry Foundations pilot — Visual Asset Audit — 2026-08-10

> Package สำหรับพัฒนา/ทดสอบ ยังไม่ใช่หลักฐานว่า `catalog.json` มีสถานะ certified

- เพิ่มและผ่านกฎ `G3-V`: GHS ใช้ UNECE; อุปกรณ์ใช้ Servier/OpenClipart ผ่าน Bioicons พร้อม provenance รายไฟล์
- เปลี่ยน GHS บน sample chemical label จากภาพวาดด้วยโค้ดเป็น verified UNECE pictograms
- เก็บ deterministic drawing เฉพาะ measurement schematic/meniscus ที่ค่าทางวิทยาศาสตร์เป็นสาระ
- ลบ drawing functions ของอุปกรณ์/GHS แบบเก่า, orphan GHS derivative, ภาพ ImageGen ทดลอง และ temp QA files หลังตรวจเสร็จ
- Word export + visual review ครบ 20/20 หน้า; student packet 14/14 หน้า; preview 8/8 หน้า; cover/listing 3/3 ภาพ
- Structural check: page counts ตรง, ไม่มี blank page ใน student/preview, source compile ผ่าน
- ลบ legacy `lab*.svg`/NFPA SVG ที่ไม่มีการอ้างอิง; ย้าย GHS source SVG ที่ใช้จริงเข้า `verified-ghs/`
- Attribution QA ของ asset ชุด pilot ผ่าน; repository รวมยังมี warning ของ font licenses/legacy figure derivatives จึงยังห้ามยกสถานะทั้ง catalog เป็น certified

## CN-AB-001 · "Acids & Bases: Theories and Strength" — ✅ CERTIFIED (v1.0)

- **สินค้า:** 20 MC questions + Quick Review Card + Answer Key (คำอธิบาย + misconception)
- **ไฟล์:** acid-base-theories-practice-product.pdf (8 หน้า: cover→TOU→ข้อสอบ→เฉลย) · cover.png · preview ×3
- **ราคา:** $3.50 · **เกรด:** 9-12 (แนะนำ 10-12 Honors/AP/IB)
- **วันที่ certify:** 2026-08-09 · **ตรวจโดย:** Hermes Agent + เกณฑ์ product-quality-standard.md v1.0

### G1 — Chemistry Gate ✅
- Source: `content/intake/2026-08-02-acid-base-b01.intake.json` (20 ข้อ)
- `review.chemistry_status = approved` (Codex chemistry QA + second-pass, 2026-08-02/03)
- ไม่มีการแก้เนื้อหาเคมีหลัง freeze

### G2 — Language Gate ✅
- แปลครบ 20/20 · ศัพท์ตรง glossary-th-en.md v1.0 (en dash Brønsted–Lowry, [H⁺] ในการคำนวณ, US spelling)
- **พบและแก้ 4 จุด:**
  1. ABM-009: "Which statement is correct?" → "Which of the following statements is correct?"
  2. ABM-011: [H₃O⁺] → [H⁺] (ความสม่ำเสมอตาม convention ใน glossary)
  3. ABM-014: เกลากระบวนการ diluted → "A HNO₃ solution is diluted so its concentration drops tenfold..."
  4. ABM-020: "When solving an ICE table... gives" → "An ICE table calculation ... yields"
- ไม่พบ AI-ism (ตัดคำชมตัวเอง/วลีซ้ำ — checklist ผ่าน)
- ⚠️ **Residual risk:** ยังไม่มีเจ้าของภาษา (native) อ่านทวน — ตามมาตรฐานข้อ G2 ต้องทำ **ก่อนอัปโหลดจริง** (ครั้งแรกของร้าน)

### G3 — Product Gate ✅
- Product PDF 8 หน้า โครงสร้างครบ: cover → TOU → review card → 20 ข้อ → answer key
- Answer key 20/20 พร้อมคำอธิบาย + misconception
- Quick Review Card 1 หน้า (4 หัวข้อ)
- **เพิ่มตัวบ่งชี้ difficulty** (●○○/●●○/●●● + legend) — สนับสนุน differentiation
- Preview images ×3 (review / questions / answer key) + cover 1200×1200
- ฟอนต์ฝัง (Poppins/Nunito/Caveat) · ไม่มีแท็กหลุด · US Letter · build + pypdf verify ALL PASS

### G4 — Compliance Gate ✅
- AI disclosure: จะตอบ "AI-assisted" ตามจริงตอนอัปโหลด (แผนใน tpt-listing-pack.md §9)
- ฟอนต์ Google Fonts = OFL ✓ · รูป/ไอคอนสร้างเอง ✓
- TOU อยู่ในไฟล์ (single-teacher license) ✓
- หมวด/แท็ก/ราคา/คำอธิบาย ครบตาม tpt-listing-pack.md ✓

### ขั้นตอนถัดไป (ก่อน publish)
1. [ ] เจ้าของภาษาอ่านทวนภาษาอังกฤษทั้งชิ้น (ตาม G2 residual risk)
2. [ ] สมัคร Seller account + ตั้งร้าน ChemNest
3. [ ] อัปโหลดตาม tpt-listing-pack.md (title §3, description §4, tags §5, settings §6, images §7)

---

## 2026-08-11 — CN-CH02-MATTER

- Automated package QA: `PASS 91/91`
- PDF visual review: `PASS` — 15/15 complete-product pages and 3/3 preview pages
- Listing visual review: `PASS` — 3/3 images
- Visual rights gate: `PASS` — 3/3 assets documented with source and license evidence
- Buyer package: PDF only; no editable file advertised or delivered
- Microsoft Defender: `PASS` — no threats found
- Buyer ZIP SHA-256: `d1ea9a5cbbef2602beb1f792dc4694f8528d10e553b21f6088f07883c718967a`
- Release status: `BLOCKED` pending native-English review, U.S. chemistry-teacher review, and classroom dry run

---

## 2026-08-11 — Complete-unit rebuild closure

| Product | Automated QA | PDF rendering | Visuals | Exact buyer ZIP | Release state |
|---|---:|---:|---:|---|---|
| `CN-CH01-MATH` | `PASS 240/240` | `PASS — 113/113 final pages; component parity verified` | `4/4 documented open assets` | `a6deef48e35cc5d180459878dd7efea68c73acfa2b601bf8bf8f1a91adf1f1c8` | `BLOCKED — three human gates pending` |
| `CN-CH02-MATTER` | `PASS 236/236` | `PASS — 113/113 final pages; component parity verified` | `3/3 documented open assets` | `9a0ebb18c4216338c1bedf5f6460f8b850d6dcd7e7b1d439c13847a46308c766` | `BLOCKED — three human gates pending` |

- Both units now follow `Engage → Teach → Model → Guided Practice → Independent Practice → Exit Ticket → Mixed Review → Test A/B`.
- Every final PDF is US Letter, American English, PDF only, and branded CurioNest.
- Listing images use verified product-page renders; no AI-generated or code-drawn instructional visual is used.
- Microsoft Defender found no threats in either exact ZIP hash above.
- Obsolete student/key PDFs and old listing graphics were removed from the current output folders.

---

## Log เก่า
- (ยังไม่มีสินค้าอื่น — CN-AB-001 เป็นชิ้นแรก)

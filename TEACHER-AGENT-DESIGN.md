# ChemNest Teacher-Agent v2 — Business-Factory Architecture
(ออกแบบ 2026-08-10 · ผู้ใช้ขยายวิสัยทัศน์: ครูสมัยใหม่ + นักผลิต + นักขาย + นักการตลาด + นักวิเคราะห์ข้อมูล)

## วิสัยทัศน์ (จากคำสั่งผู้ใช้)
Agent ต้องเป็น **CPO (Chief Product Officer) ครบวงจร**:
1. **ครูสมัยใหม่** — ค้นคว้าแนวการสอนใหม่ๆ/เทรนด์เอง (NGSS, phenomenon-based, CER, retrieval practice, AI-era pedagogy)
2. **นักวิเคราะห์คู่แข่ง** — เทียบงานคู่แข่ง (โครงสร้าง/ราคา/จุดขาย) แล้วตัดสินใจ
3. **นักผลิต** — ผลิตสินค้าคุณภาพ (Factory v1 เดิม)
4. **นักขาย** — จัดการ listing/ราคา/ช่องทาง
5. **นักการตลาดมืออาชีพ** — วิเคราะห์ **ข้อมูลหลังบ้าน TPT** (views/sales/conversion) ว่าขายได้ไหม ทำไม
6. **นักวางกลยุทธ์** — ปรับแผนตามตลาด/เทศกาล/ปฏิทินโรงเรียน (Back-to-School, AP season, Summer)
7. **นักไอเดีย** — ไอเดียขายใหม่ไม่จำเจ

---

## สถาปัตยกรรม 4 ชั้น

```
┌────────────────────────────────────────────────────────────┐
│ L1 STRATEGY — ตัดสินใจ "ทำอะไร เมื่อไหร่ ทำไม"             │
│   • TPT analytics (หลังบ้าน: views/sales/conversion/รายได้) │
│   • Product calendar (เทศกาล/เปิดเทอม/AP season)           │
│   • Competitor radar (scrape top sellers, teardown)        │
│   • Trend scanner (แนวการสอนใหม่ → สินค้าใหม่)              │
│   • KPI board (kpi_log.json + analytics.py)                │
│   → เอาต์พุต: product backlog ที่จัดลำดับตามโอกาสขาย        │
├────────────────────────────────────────────────────────────┤
│ L2 PRODUCT FACTORY — ผลิต (subject-agnostic)               │
│   • Subject packs (เคมี = ตัวแรก, ฟิสิกส์/คณิต/ชีวะ ต่อ)    │
│   • Deterministic core: docx→Word→PDF, OMML eq, figures,    │
│     verify.py, QA gates                                     │
│   → เอาต์พุต: PDF/docx/cover/preview/listing copy           │
┌────────────────────────────────────────────────────────────┐
│ L3 MARKETING — ขาย + โปรโมต                                 │
│   • Listing optimizer (title/desc/keywords ตาม TPT SEO)     │
│   • Seasonal campaigns (Back-to-School, Halloween Chem,     │
│     Christmas Chem, Valentine, AP crunch, Summer review)    │
│   • Pricing strategy (เทียร์/ราคา/bundle ตาม data)           │
│   • Idea engine (ไอเดียใหม่ไม่จำเจ — หมุนเวียนรูปแบบ)        │
│   • **Channel Ops (browser = ทำเหมือนคนจริง):**              │
│     - Auto-post: login TPT → Seller Dashboard → Add product │
│       → กรอกฟอร์ม → อัปโหลด PDF/docx/cover/preview → publish│
│     - Analytics harvest: เปิดหน้า stats → เก็บ views/sales/  │
│       conversion → บันทึก CSV → วิเคราะห์                    │
│   → เอาต์พุต: listing ที่อัปเดต + แคมเปญ + ไอเดีย           │
├────────────────────────────────────────────────────────────┤
│ L4 INTELLIGENCE LOOP — เรียนรู้จากผลลัพธ์                   │
│   • หลังขาย: product A ทำไมขายดี / product B ทำไมเงียบ       │
│   • ป้อนกลับเข้า L1 (ปรับ backlog) + L2 (ปรับคุณภาพ)         │
│   • รายงานรายสัปดาห์ (dashboard)                            │
└────────────────────────────────────────────────────────────┘
```

---

## L1 Strategy — รายละเอียด

### TPT Analytics (ข้อมูลหลังบ้าน) — เก็บผ่านหน้าเว็บ (browser) ไม่ใช้ API
| ข้อมูล | แหล่ง | ใช้ทำอะไร |
|---|---|---|
| Views / Sales / Revenue | TPT seller dashboard (browser เปิดหน้า stats) | อะไรขายดี/เงียบ |
| Conversion rate | views→sales (คำนวณจากตัวเลขที่เก็บ) | listing/ราคา/หน้าปกดีไหม |
| Sales by month | TPT dashboard + kpi_log.json | seasonality → ปฏิทิน |
| Best sellers of category | TPT search (browser/scrape หน้าสาธารณะ) | ช่องว่างตลาด + แนวโน้ม |
| Top competitor pricing | ร้านคู่แข่ง (browser/scrape หน้า public) | ตั้งราคา/ทำ bundle |

*การเข้าถึง: Browser Use (Nous subscription) เปิดหน้า TPT → login session (user login ครั้งแรก) → เก็บข้อมูลหน้า stats → บันทึก CSV ใน data/tpt/ — เหมือนคนเปิดเว็บดูจริง*

### Product Calendar (ปฏิทินตลาด US)
| เดือน | เทศกาล/เหตุการณ์ | สินค้าที่ควรมี |
|---|---|---|
| ก.ค. | Summer prep | review packs, pacing guide |
| ส.ค.-ก.ย. | **Back-to-School** | ตั้งร้าน, starter packs, freebie lead magnets |
| ต.ค. | Halloween | chemistry of Halloween (pH ของฟักทอง/ฟอง) |
| พ.ย. | Thanksgiving | กิจกรรมสั้น/review ครึ่งเทอม |
| ธ.ค. | Christmas/Winter break | review before finals, gift bundles |
| ม.ค. | New semester | หลักสูตรใหม่ (Equilibrium/Kinetics เริ่ม) |
| ก.พ. | Valentine's Day | chemistry of love (bonding!) |
| มี.ค. | Spring break | test-prep packs |
| เม.ย.-พ.ค. | **AP season** | AP chem review, FRQ practice, CED alignment |
| พ.ค.-มิ.ย. | Finals / End of year | final review, fun summer labs |

### Competitor Radar
- เก็บ `research/tpt-top-sellers-teardown.md` (มีแล้ว) → ขยายเป็นอัตโนมัติ
- สัปดาห์ละครั้ง: search "acids and bases worksheet" → เก็บ top 10 (ชื่อ/ราคา/หน้าแรก/รีวิว)
- วิเคราะห์: เขาทำอะไรที่เราไม่ทำ? เราทำอะไรที่ดีกว่า? → เข้า backlog

### Trend Scanner (ครูสมัยใหม่)
- แหล่ง: NGSS updates, NSTA, ChemEd X, Twitter/X #ChemEd, teacher blogs, TPT trending
- สัญญาณที่ควรจับ: phenomenon-based learning, CER framework, 3D learning,
  retrieval practice, spaced practice, AI-tools-for-teachers (ใหม่!)
- แปลงเป็นสินค้า: "pH CER activity", "Equilibrium phenomenon: The Blood Buffer", "AI-era: ใบงานดิจิทัล"

---

## L3 Marketing — รายละเอียด

### Listing Optimizer (TPT SEO)
- Title: คีย์เวิร์ดที่ครูค้นจริง + grade + topic ("Acids & Bases Unit: pH, Ka, Buffers & Titrations — High School Chemistry Worksheets with Answer Keys")
- Description: bullet จุดขาย (answer keys, editable, NGSS/AP aligned, หน้า preview จำนวน)
- Keywords: 12 คำที่ TPT รับ (search term ที่ครูใช้)
- Preview: 3-5 หน้าแรกสุดสวย (มีแล้ว build_listing_assets.py)

### Seasonal Campaign Engine
- แต่ละเทศกาล → checklist: สินค้าอะไรต้องออก/รีแพ็กเกจ/ลดราคา/โปรโมต (blog/IG/pin)
- ข้อความการตลาดเปลี่ยนตามฤดูกาล ("Get AP-ready", "Back-to-school bundle")

### Pricing Strategy (Hormozi ladder — มีแล้ว)
- Freebie lead magnet → entry ($3-5) → bundle ($12-20) → membership/whole-year
- ใช้ data ตัดสินใจ: ถ้า conversion ต่ำที่ราคานี้ → ลอง $2.99 หรือ bundle

### Idea Engine (ไม่จำเจ)
- หมุนเวียนรูปแบบ: worksheet → CER → lab → escape room → digital (Google Slides) → task cards → boom cards → pixel art (มี CBN แล้ว!) → guided notes → interactive notebook
- "Chemistry of [festival/holiday/real-world]" series — ไม่รู้จบ
- เวลาคิดไม่ออก → ดู L4 data ว่าอะไรทำงาน

---

## L4 Intelligence Loop
- ทุกสัปดาห์: รวบรวม kpi_log.json + TPT CSV → สรุป: 3 สินค้าขายดี (ทำไม?) / 3 เงียบ (ทำไม?)
- ป้อนกลับ: L1 ปรับ backlog (ทำแบบขายดีซ้ำ), L2 ปรับคุณภาพ (แก้จุดที่ conversion ตก), L3 ปรับ listing
- รายงาน: `reports/weekly-YYYY-MM-DD.md`

---

## วิชาใหม่ = เพิ่ม Subject Pack (เหมือนเดิมจาก v1)
```
subject-packs/<subject>/
  SKILL.md          — curriculum map + depth + voice
  references/glossary.md, patterns.md, chapters/, qa-scope.json
  figures/          — generator + รูปสำเร็จ
```
เคมี = subject-pack ตัวแรก (us-chemistry-curriculum มีแล้ว) — เพิ่มวิชา = สร้าง pack ใหม่, core ไม่แตะ

---

## Roadmap
1. ✅ v1 core ครบ (builder/omml/figures/QA) — เคมี 6 สินค้า
2. 🔨 L2 ทำเป็นระบบ: skill `teacher-product-factory` (core pipeline + subject-pack convention)
3. 🔨 L1: `market-intel` — product calendar + competitor radar script + trend scanner
4. 🔨 L3: `listing-optimizer` + seasonal campaign checklist + idea engine
5. 🔨 L4: weekly report script (อ่าน kpi_log + TPT CSV → สรุป)
6. 🧪 ทดสอบวงจรเต็ม: 1 รอบ "วางแผน→ผลิต→QA→listing→วิเคราะห์"

## สิ่งที่ไม่ทำใน v2 (ขอบเขต)
- **ไม่ใช้ API หลังบ้าน TPT** — ใช้ browser automation แทน (เปิดเว็บ→กรอก→อัปโหลด→เก็บข้อมูล เหมือนคนทำจริง)
- **Auto-post ต้อง human-in-the-loop** — agent เตรียมทุกอย่าง + login session ของ user + รัน flow ให้ แต่**ก่อนกด Publish จริง ต้องให้ user กดยืนยัน** (หรือตั้งค่า "auto-publish = off" เป็น default; เปิดได้เมื่อ user ไว้วางใจ) — ไม่มี autopost แบบ blind
- **Login session**: user login TPT ครั้งแรกในเบราว์เซอร์ (credentials ไม่เก็บใน agent) — session ถูกเก็บใน profile เบราว์เซอร์เพื่อใช้ซ้ำ
- ไม่สร้าง UI แยก — ใช้ Hermes chat + browser tools + cron

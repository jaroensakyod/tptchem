# CurioNest TPT Chemistry — Production Pipeline

ระบบผลิตสื่อการสอนเคมีสำหรับ Teachers Pay Teachers:

`JSON ต้นฉบับ → DOCX/PDF/PPTX → QA → package → listing → analytics`

สถานะในไฟล์นี้อ้างอิง repository ปัจจุบันเท่านั้น แหล่งข้อมูลสินค้าแบบ
machine-readable คือ [`catalog.json`](catalog.json)

## สถานะปัจจุบัน — 2026-08-10

### สินค้าปัจจุบัน

| ID | สินค้า | Package | สถานะ |
|---|---|---|---|
| `CN-CH01-MATH` | Chapter 1 — Math & Measurement | `products/ch01-math-measurement/` | `packaged_pending_qa` |
| `CN-CH01-ESSENTIAL` | Chapter 1 — Essential Ideas | `products/ch01-essential-ideas/` | `packaged_pending_qa` |

แต่ละ package มี `product.pdf`, `product-editable.docx`, `cover.png` และ
`preview.pdf` สินค้าทั้งสองยัง **ห้าม publish** จนกว่าจะผ่าน human visual QA,
native-English review และ asset attribution แล้วเปลี่ยนสถานะเป็น `certified`

ไฟล์ b01-b07 ที่ root เป็น legacy/regression artifacts ยังไม่ใช่ upload-ready
packages ส่วน `regents-builder-test` และ JSON ที่ลงท้าย `-demo` เป็น fixtures

### Builder ที่มีจริง

| ไฟล์ | หน้าที่ |
|---|---|
| `build_mirror_pack.py` | Lesson/worksheet/Regents-style DOCX และ PDF |
| `build_ppt_pack.py` | Teacher slide deck ผ่าน PptxGenJS |
| `build_quiz.py` | Standalone quiz + answer key |
| `build_scavenger_hunt.py` | Station/scavenger hunt + answer sheet |
| `omml.py` | แปลง LaTeX/chemistry notation เป็น Word OMML |
| `chem_figures.py` | สร้าง chemistry figures |
| `analytics.py` | เก็บ KPI, CSV snapshots, keywords และ A/B log |
| `qa.py` | ตรวจ source, schema, catalog, package และ attribution |

## ติดตั้ง

ต้องใช้ Python 3.10 ขึ้นไป, Node.js และ Microsoft Word บน Windows สำหรับแปลง
DOCX เป็น PDF

```powershell
py -3.11 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e .
& 'C:\Program Files\nodejs\npm.cmd' install
```

หากเครื่องไม่มี Python ให้ติดตั้ง Python 3.11 หรือ 3.12 ก่อน ห้ามผูกคำสั่งกับ
absolute path ของ Python ในเครื่องใดเครื่องหนึ่ง

## ตรวจโปรเจกต์

QA ระดับ repository ใช้เฉพาะ Python standard library จึงรันได้ก่อนติดตั้ง
dependency ของ Builder:

```powershell
python qa.py all
python qa.py all --strict
python -m unittest discover -s tests -v
```

- โหมดปกติ: warning ไม่ทำให้คำสั่งล้ม
- `--strict`: warning เช่น attribution หรือสินค้ายังไม่ certified ทำให้ exit non-zero
- สินค้าที่จะ publish ต้องผ่าน strict mode และ human visual review

## สร้างไฟล์

```powershell
python build_mirror_pack.py mirror-json/ch01-math-measurement.json ch01-math-measurement
python build_quiz.py mirror-json/quiz-lab-safety-demo.json quiz-lab-safety-demo
python build_scavenger_hunt.py mirror-json/hunt-lab-safety-demo.json hunt-lab-safety-demo
python build_ppt_pack.py mirror-json/b01-mirror.json b01-slides
python build_listing_assets.py all
```

Builder ปัจจุบันเขียน output ที่ root ของ repository การย้ายเข้า `products/`
ต้องทำหลังตรวจไฟล์แล้ว โดย package ต้องใช้ชื่อมาตรฐานจาก `catalog.json`

## Analytics

```powershell
python analytics.py init
python analytics.py log --date 2026-08-10 --product CN-CH01-MATH --views 10 --sales 1 --revenue 3.50
python analytics.py import --file product-statistics.csv --mode snapshot
python analytics.py report --days 7
```

- `snapshot` ใช้กับ CSV ยอดสะสมจาก TPT และเก็บใน `statistics_snapshots`
- `period` ใช้เมื่อ CSV เป็นยอดเฉพาะช่วงเวลาและบันทึกลง daily metrics
- Import ซ้ำวันเดิมเป็น upsert ไม่เพิ่มยอดซ้ำ
- `kpi_log.json` ถูก ignore เพราะเป็นข้อมูลดำเนินงานเฉพาะร้าน

## โครงสร้างสำคัญ

```text
catalog.json               สินค้าปัจจุบันและสถานะเดียวของระบบ
schemas/                   JSON Schema
mirror-json/               ต้นฉบับเนื้อหาสินค้า
products/                  package ที่เป็น sellable candidates
figures/                   รูปและ source SVG
assets-manifest.json       license/provenance แบบ machine-readable
ATTRIBUTION.md             กฎและสถานะ attribution
upload-kit/                listing drafts; ต้องตรวจ catalog ก่อนใช้
product-quality-standard.md มาตรฐาน G1-G4
```

## Release gates

1. JSON และ answer key ผ่าน `qa.py`
2. Rebuild จาก source ได้โดยข้อมูลไม่หาย
3. Product PDF, editable DOCX, cover และ preview ครบ
4. Human visual QA ทุกหน้า ไม่มีข้อความล้น/ทับ/เพี้ยน
5. ภาษาอังกฤษผ่าน native review สำหรับสินค้าเปิดร้าน
6. Asset ทุกกลุ่มใน `assets-manifest.json` เป็น `verified`
7. ผ่าน Visual Asset Gate `G3-V`: อุปกรณ์/GHS ใช้แหล่งมาตรฐาน, ภาพคำนวณใช้ generator, ภาพบริบทจึงใช้ ImageGen
8. มี QA record ของ Product ID ปัจจุบัน
9. เปลี่ยน `catalog.json` เป็น `certified` จึงอัปโหลดได้

## กฎเนื้อหา

- ใช้ศัพท์และระดับความยากให้ตรงหลักสูตร US/OpenStax แต่ห้ามคัดลอกย่อหน้า
- สมการใน Word ต้องเป็น OMML ไม่ใช่ LaTeX ที่แสดงเป็น plain text
- Regents MCQ ใช้ตัวเลือก 1-4
- กระดาษ US Letter; preview ปัจจุบันกำหนด 3 หน้า
- รูปภายนอกต้องมี source URL และ license ใน asset manifest ก่อนใช้งาน
- กฎเลือกแหล่งภาพและการลบไฟล์ทดลองให้ยึด `product-quality-standard.md` หัวข้อ `G3-V`

ดู roadmap เชิงธุรกิจได้ที่ `PRODUCT-MATRIX-BACKTOSCHOOL.md` และ
`TEACHER-AGENT-DESIGN.md` แต่สถานะ implementation ให้ยึด README และ catalog นี้

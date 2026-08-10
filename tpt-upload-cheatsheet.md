# ChemNest — คู่มือกรอกฟอร์มอัปโหลด TPT (ทีละช่อง)

> สำหรับสินค้า CN-AB-001 "Acids & Bases: Theories and Strength" — เปิด Seller Dashboard → **Add new product** → กรอกตามนี้

## ลำดับช่องในฟอร์ม + วิธีกรอก

| # | ช่องฟอร์ม | ใส่อะไร | ค่าของ CN-AB-001 (ก๊อปวางได้) |
|---|---|---|---|
| 1 | **Product type** | เลือกประเภท | Digital download (PDF ไฟล์เดียว) |
| 2 | **Title** | keyword หลักไว้หน้า, สั้น-ตรง | `Acids and Bases Worksheet High School Chemistry: Theories & Strength + Answer Key` |
| 3 | **Description** | ใช้ description ใน tpt-listing-pack.md §4 (ก๊อปทั้งบล็อก) | — |
| 4 | **Grades** | ติ๊กตามเกรด | ☑ 9th ☑ 10th ☑ 11th ☑ 12th |
| 5 | **Subjects** | หมวดวิชา | Science → ☑ Chemistry |
| 6 | **Resource type** | ประเภททรัพยากร | ☑ Worksheets ☑ Printables ☑ Homework (เพิ่ม Assessment ได้) |
| 7 | **Formats** | รูปแบบไฟล์ | ☑ PDF |
| 8 | **Standards** *(optional)* | มาตรฐานการเรียนรู้ — ใส่เฉพาะที่ตรงจริง (ช่วย search ในเขตที่กรองมาตรฐาน) | NGSS HS-PS1-6 (ถ้ามีตัวเลือก) หรือข้ามไป |
| 9 | **Price** | ราคา USD | `3.50` |
| 10 | **Thumbnails** (สูงสุด 4 รูป) | รูปหน้าสินค้า — ใช้ cover + preview ที่ทำไว้ | `cover.png` + `preview-review.png` + `preview-questions.png` + `preview-answerkey.png` |
| 11 | **Preview file** | ไฟล์ตัวอย่าง 1-3 หน้า (โชว์พอจูงใจ ห้ามเฉลยหมด) | `acid-base-theories-practice-preview.pdf` (3 หน้า: cover → review card+คำถาม → เฉลย 5 ข้อตัวอย่าง) |
| 12 | **Main file** | ไฟล์ที่ผู้ซื้อได้ | `acid-base-theories-practice-product.pdf` (8 หน้า ไฟล์เดียว ไม่ต้อง zip) |
| 13 | **Tags** (สูงสุด 12) | keyword ค้นหา — ใช้จาก §5 | ดูรายการด้านล่าง |
| 14 | **Supports / Digital activity** | ระบุชนิด | Printable (ไม่ใช่ Google Apps/Easel ตอนนี้) |
| 15 | **Pages / Answer Key / Duration** *(ถ้ามีช่อง)* | ข้อมูลไฟล์ | Pages `8` · Answer Key `Included` · Teaching Duration `45-50 minutes` |
| 16 | **AI disclosure** | คำถามว่าระบุการใช้ AI — **ตอบตามจริง** (เราใช้ AI ช่วยแปล/ออกแบบ = AI-assisted) | ☑ Yes / AI-assisted (ตามข้อความในฟอร์ม) |
| 17 | **ลิขสิทธิ์ affirmation** | ยืนยันว่าไม่ละเมิดลิขสิทธิ์บุคคลที่สาม | ☑ (เนื้อหา/ฟอนต์/รูปของเราเองหรือ OFL — ผ่าน) |
| 18 | **Make Listing Active** | ติ๊กเมื่อพร้อมขาย | ☑ (หลังตรวจ Preview ผ่าน) |
| 19 | **Submit** | กดส่ง | — |

## Tags ครบ 12 (คัดจาก §5 ของ listing pack)

```
acids and bases, chemistry worksheet, high school chemistry, conjugate acid base pairs,
pH and pOH, acid strength Ka pKa, Arrhenius Bronsted Lowry Lewis, percent ionization,
common ion effect, weak acid equilibrium, no prep printable, answer key included
```

## เคล็ดลับ (จาก research ร้านขายดี)

- **Preview สำคัญที่สุดในฟอร์ม** — TPT ระบุเอง: "Product pages containing preview downloads are better positioned to sell" — อย่าข้าม
- Title อย่าเกิน ~80 ตัวอักษร และอย่าเปลี่ยนบ่อย (SEO สะสม) — เปลี่ยนได้แต่บันทึกใน KPI log
- ถ้าเจอช่อง "Easel by TPT" — ข้ามไปก่อน (เปิดทีหลังเมื่อมีรีวิว)
- หลัง Submit TPT อาจตรวจสินค้าใหม่ (moderation) — ปกติไม่เกิน 1-2 วัน ถ้าถูก suspend ให้ตรวจ G4 (ลิขสิทธิ์/disclosure) ก่อน appeal
- บันทึก `publish_date` + KPI เริ่มต้นลง kpi_log (ตาม chemnest-ops-loop.md §4) ทันทีที่ active

## ไฟล์ที่ต้องมีครบก่อนกรอก (อยู่ใน tpt-pilot/)

- [x] `acid-base-theories-practice-product.pdf` — main file
- [x] `acid-base-theories-practice-preview.pdf` — preview file (สร้างแล้ว 3 หน้า)
- [x] `cover.png` + preview PNG ×3 — thumbnails
- [x] title/description/tags — ใน `tpt-listing-pack.md`

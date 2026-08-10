# ChemNest Analytics System v1.0 — ระบบเก็บ-เชื่อม-วิเคราะห์-ปรับปรุง (ปิด loop)

> ข้อมูลจากเอกสารทางการ TPT (2026-08-09) · ใช้คู่กับ chemnest-ops-loop.md (การผลิต) และ product-quality-standard.md (คุณภาพ)

## 1. แหล่งข้อมูลทางการที่ TPT ให้ (ใช้ให้ครบ — ฟรี ไม่ต้องสแครป)

| แหล่ง | ที่ไหน | ให้อะไร | ข้อจำกัด |
|---|---|---|---|
| **Seller Dashboard** | tpt.com/Dashboard | กราฟภาพรวมรายวัน: views/sales/revenue ทั้งร้าน | ภาพรวม ไม่แยกสินค้า |
| **Product Statistics** ⭐ | My-Statistics | ต่อสินค้า: sales, conversion, earnings + **ดาวน์โหลด CSV ได้** | ไม่รวม Flex earnings (ดูที่ Sales Reports) |
| **Search Analytics** ⭐⭐ | แท็บใน Dashboard | **keyword จริงที่คนค้นแล้วเข้าร้าน**: Keyword Visits / Conversions / Earnings / Resources ต่อ keyword, ดูย้อนหลังได้ (ข้อมูลตั้งแต่ 1 ม.ค. 2025) | **Basic เห็นแค่ 5 keyword อันดับแรก** / Premium เห็นเต็ม + ต่อสินค้า |
| **Product Insights Report** | แยกจาก Dashboard | รายละเอียดต่อสินค้าเชิงลึก | — |
| **Sales Reports** | My-Sales | ยอดขาย + แหล่งที่มา (Marketplace / School Express / Flex) + Last Download | — |
| **School Access (เก่า)** | — | **ปลดระวางแล้ว 30 ก.ย. 2025** — ตัวใหม่คือ **TPT School Express** (curated library) + **Flex Catalog** (beta) | รอ TPT เปิด enrollment แล้วค่อย opt-in ตามประกาศ seller blog |

**ข้อสรุป:** ไม่ต้องพึ่ง third-party ตอนแรก — TPT ให้ keyword data + CSV จริงแล้ว (Basic จำกัด 5 keyword → **Premium $59.95/ปี คุ้มทันทีที่เริ่มจริงจัง** เพราะได้ keyword เต็ม + commission 80% แทน 55%)

## 2. เก็บอะไร เมื่อไหร่ (cadence)

| ความถี่ | อะไร | วิธี | ใช้เวล |
|---|---|---|---|
| **ทุกวัน** | views/sales/revenue ของเมื่อวาน (ต่อสินค้า) | `analytics.py log --date ... --product ... --views ... --sales ...` | ~5 นาที |
| **ทุกวันจันทร์** | export Product Statistics CSV → import | `analytics.py import --file <csv>` | ~3 นาที |
| **สัปดาห์ละครั้ง** | Search Analytics: บันทึก keyword top + conversion | `analytics.py keyword --product ... --kw ... --visits ... --conv ...` | ~10 นาที |
| **ทุกการแก้ listing** | A/B log: เปลี่ยน title/cover/ราคา | `analytics.py ab --product ... --field title --to "..." --reason "views 0 ใน 7 วัน"` | 1 นาที |
| **ทุกวัน** | อ่าน `daily_report.md` (script สร้างให้) + ตัดสินใจ 3 ข้อ | `analytics.py report` | 10 นาที |

## 3. โครงสร้างข้อมูล (kpi_log.json — ไฟล์เดียว เก็บทุกอย่าง)

```json
{
  "schema_version": 1,
  "products": {
    "CN-AB-001": {
      "title": "Acids and Bases Worksheet ...",
      "price": 3.5, "publish_date": null,
      "batch": "2026-08-02-acid-base-b01", "qa_status": "certified",
      "daily": [ {"date": "2026-08-10", "views": 12, "previews": 4, "wishlists": 1, "sales": 0, "revenue": 0.0} ],
      "keywords": [ {"kw": "acids and bases worksheet", "visits": 8, "conversions": 0, "earnings": 0.0, "date": "2026-08-16"} ],
      "ab_tests": [ {"date": "2026-08-17", "field": "title", "from": "...", "to": "...", "reason": "0 views 7 วัน"} ],
      "rating": null
    }
  }
}
```

## 4. วิเคราะห์ (3 ระดับ)

**รายวัน (script `report`):** ยอดรวมวันนี้/7 วัน · ตารางต่อสินค้า (views→sales→revenue→conversion%) · **flag อัตโนมัติ** ตามกฎข้อ 5

**รายสัปดาห์ (จันทร์ เช้า):** เทรนด์ 7 วัน · keyword ตัวไหนพา traffic/conversion · สินค้าไหน trending · เปรียบเทียบ cohort (สินค้าอายุเท่ากัน)

**รายเดือน:** สรุป revenue/ROI · อะไรที่ควรทำซ้ำ (winning keyword → ชุดใหม่) · อะไรควรตัด/แก้ · เตรียม seasonal (ดู keyword เดือนเดียวกันปีก่อน)

## 5. Decision Rules v2 (เพิ่มจาก ops-loop ด้วย Search Analytics)

| สัญญาณ (จากข้อมูล) | การตัดสินใจ |
|---|---|
| keyword มี **conversion** | เก็บ keyword ไว้ใน title **+ ทำสินค้าใหม่ใน keyword นั้น** (ข้อมูลบอกว่ามีคนจ่ายเงิน) |
| keyword มี **visits แต่ไม่มี conversion** | ตรวจ cover/ราคา/ความตรงของสินค้า vs สิ่งที่คนค้น |
| views ขึ้น แต่ sales ไม่ขึ้น | ปัญหา conversion: cover → preview → ราคา → รีวิว (เรียงตามลำดับ) |
| views นิ่ง (SEO ไม่มา) | ปัญหา SEO: title/tags/description 250 ตัวอักษรแรก |
| views = 0 หลัง 7 วัน | เปลี่ยน title/keywords (ครั้งเดียว) แล้วรออีก 7 วัน — ยังไม่ขึ้น → เปลี่ยน cover |
| ขายดี (≥3 ชิ้น/เดือน) | ทำ sequel + เตรียม bundle + ใส่ลิงก์ข้ามสินค้า |
| รีวิว 1 ดาว | ระงับสินค้า ตรวจ G1-G4 + log สาเหตุ |
| เข้าฤดูกาล | ปล่อยชิ้นตรงฤดูกาลก่อน (ดู keyword ย้อนหลังปีก่อน) |
| เปลี่ยน title/cover แล้ว views ขึ้นภายใน 7 วัน | เก็บเวอร์ชันใหม่ (A/B win) — บันทึกใน ab_tests |

## 6. เครื่องมือ (เรียงตามงบ)

1. **ฟรี:** TPT built-in ทั้งหมด (Dashboard, Product Statistics CSV, Search Analytics แบบ Basic, Product Insights)
2. **$59.95/ปี:** TPT Premium — keyword เต็ม + ต่อสินค้า + commission 80% (คุ้มตั้งแต่วันแรกที่จริงจัง)
3. **Third-party (เมื่อมี budget):** SellerSpy.co (300K+ keywords, competition) หรือ SEOLumina (keyword generator, store audit) — ใช้สำหรับหา "unicorn keyword" ตอนวางแผนสินค้าใหม่ ไม่จำเป็นตอนเริ่ม

## 7. Email list (จาก playbook Lindsay Bowden — รายได้ระยะยาว)

- **Freebie = lead magnet** (mini pack จาก Tier A) → แลก email
- วางลิงก์สมัครใน: **หน้า preview, หน้า 2 ของไฟล์, description, หน้า TOU**
- Workflow อัตโนมัติ: ส่ง freebie → แนะนำตัว → แชร์ tip → เปิดตัวสินค้าใหม่
- เริ่มวันแรกเลย (Lindsay: "ถ้าย้อนเวลาได้ จะเริ่ม email list ตั้งแต่วันแรก") — แม้ 50 คน 1 ยอดซื้อ = win

## 8. ปฏิทินขาย 2026 (sitewide sales)

| ช่วง | สถานะ |
|---|---|
| Back-to-School (4-5 ส.ค. 2026, code BTS26) | ✅ ผ่านไปแล้ว — เราเริ่ม 9 ส.ค. พลาดรอบนี้ |
| รอบถัดไป | ~รายไตรมาส (ปีก่อน: $1 deals ก.ย., Cyber/ธ.ค. 1-2, ม.ค., ฤดูใบไม้ผลิ, พ.ค.-มิ.ย.) — **จับตาประกาศใน seller blog + email จาก TPT** |
| ระหว่าง sale | sitewide = TPT ลด 5% + seller ลดซ้อนได้ **รวมไม่เกิน 25%** — เตรียมลด 20% เก็บยอดช่วง sale |

**เตรียมตัว sale:** ปล่อยสินค้าใหม่ 1-2 สัปดาห์ก่อน sale (ให้มีของให้ลด), เตรียม bundle ก่อน sale ใหญ่, ประชาสัมพันธ์ผ่าน email list

## 9. ความจริงที่ต้องยอมรับ (กันตัดสินใจผิด)

- ข้อมูลเริ่มมี **หลัง publish** เท่านั้น — สัปดาห์แรกของร้าน = ข้อมูลน้อยมาก
- **อย่าตัดสินใจใหญ่จากข้อมูล < 7 วัน** (views วันแรกผันผวนตาม luck)
- Basic เห็นแค่ 5 keyword → อย่าเพิ่งสรุป "keyword นี้ไม่ดี" ถ้ายังไม่ Premium
- views ≠ คุณภาพสินค้า (อาจเป็น SEO/cover) · sales = คุณภาพ + trust (รีวิว) — แยกปัญหาคนละอย่าง
- เปลี่ยน title/cover/ราคา **ไม่เกิน 1 ครั้ง/สัปดาห์/สินค้า** — กันสัญญาณรบกวน data

## 10. Loop ปิดครบ (ภาพรวม)

```
ผลิต (ops-loop, 2 ชิ้น/วัน)
  ↓ certified (4 ประตู)
Publish + บันทึก publish_date ใน kpi_log
  ↓ ทุกวัน: log views/sales → report → ตัดสินใจ 3 ข้อ
วิเคราะห์ (สัปดาห์: CSV + Search Analytics)
  ↓
ปรับปรุง: title/cover/ราคา (A/B log) · ทำสินค้าตาม keyword ที่แปลง · bundle · seasonal
  ↓ ข้อมูลป้อนกลับเข้า "ทำสินค้าอะไรต่อ" → ผลิตชุดใหม่
(วนไปเรื่อย ๆ — ทุกวันข้อมูลสะสม = ทุกวันตัดสินใจแม่นขึ้น)
```

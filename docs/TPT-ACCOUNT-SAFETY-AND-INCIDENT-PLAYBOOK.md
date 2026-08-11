# TPT Account Safety and Incident Playbook

ใช้เอกสารนี้คู่กับ `TPT-PRODUCT-RELEASE-CHECKLIST.md` เพื่อลดความเสี่ยงต่อสินค้าและบัญชีร้าน CurioNest ไม่มี workflow ใดรับประกันว่าบัญชีจะไม่ถูกระงับ เพราะ TPT สงวนสิทธิ์ปิดหรือระงับบัญชีได้ แต่หลักฐานที่ครบช่วยลดข้อผิดพลาดและทำให้ตอบ Support ได้เป็นระบบ

## 1. No-go conditions

ห้ามกด **Make Listing Active** เมื่อพบข้อใดข้อหนึ่ง:

- สิทธิ์ของข้อความ ภาพ ฟอนต์ template หรือ reference ไม่ชัดเจน
- มี NC, ND, classroom-only, personal-use-only หรือข้อห้าม generative AI ที่ขัดกับการใช้งาน
- ยังไม่มี native-English cold read, Chemistry/Science teacher review หรือ dry run
- มีคำตอบผิด กำกวม safety action เสี่ยง หรือเฉลยไม่ครบทุกรายการให้คะแนน
- Preview, thumbnails, page count, file types, grade, standards หรือ editable claim ไม่ตรงกับไฟล์จริง
- เป็น duplicate/cosmetic relisting หรือความต่างจากสินค้าเดิมอธิบายไม่ได้
- ZIP ยังไม่ถูกแตกทดสอบ เปิดทุกไฟล์ สแกน malware และบันทึก SHA-256
- ไม่มี `RELEASE-EVIDENCE.md` หรือสถานะใน catalog ไม่ตรงกับหลักฐาน

## 2. Evidence folder per SKU

เก็บหลักฐานต่อสินค้าอย่างน้อยดังนี้:

- source และ revision history
- final buyer ZIP และ SHA-256
- listing copy, preview, thumbnails และ screenshots ของ draft/หน้าร้าน
- rights ledger, direct URLs, creator, license, access date และสำเนาหรือ screenshot ของ license
- native-English, subject-matter และ classroom/dry-run signoffs
- automated QA report, render contact sheet และ malware-scan result
- buyer questions, fixes, refunds, update history และ Support correspondence

สำรองหลักฐานอย่างน้อยสองแห่ง โดยหนึ่งแห่งต้องอยู่นอก TPT

## 3. Account controls

- ใช้อีเมลที่เข้าถึงได้จริง รหัสผ่านเฉพาะร้าน และรักษาข้อมูลกู้บัญชีให้เป็นปัจจุบัน
- ห้ามแชร์ seller password; หากมีผู้ช่วยให้ใช้ TPT VA Login และจำกัดงานตามความจำเป็น
- ชื่อเจ้าของบัญชี ตัวตน ภาษี และ payout ต้องตรงกับผู้มีสิทธิ์และข้อมูลจริง
- เปิดอ่านอีเมลจาก TPT และ Seller Dashboard เป็นประจำ โดยเฉพาะก่อน/หลังอัปโหลดหรือแก้สินค้า
- ห้ามเชื่อว่าการอัปโหลดผ่านหมายถึง TPT รับรองเนื้อหา สิทธิ์ หรือความปลอดภัยแล้ว

## 4. Source boundaries for CurioNest chemistry

- ChemPride: `benchmark_only`; ใช้ดู topic map และ classroom rhythm เท่านั้น
- Local OpenStax Chemistry 2e PDF: `blocked_direct_ai_and_commercial_reuse` จนกว่าจะมีหลักฐานสิทธิ์ของไฟล์ฉบับนั้น; ห้ามส่งเข้า generative AI
- CHEM P'M: retired brand; ห้ามปรากฏใน buyer files, metadata, filenames, listing หรือแหล่งอ้างอิง
- Buyer-facing rights line: `© 2026 CurioNest · For classroom use only`
- ภาพการสอน: ใช้เฉพาะ free-source ที่อนุญาตเชิงพาณิชย์และมี provenance; ห้าม AI-generated/code-drawn substitute ตาม visual policy ของสายสินค้านี้

## 5. If a buyer reports a problem

1. เก็บ exact listing, uploaded ZIP, hash, messages และเวลา ก่อนแก้ไขสิ่งใด
2. ประเมินว่ามี factual, safety, rights, malware หรือ listing mismatch หรือไม่
3. ถ้าความเสี่ยงมีมูล ให้ปิด listing ชั่วคราวโดยไม่ลบหลักฐาน
4. แก้ที่ source, rebuild, rerun QA, scan และสร้าง hash ใหม่
5. ตอบผู้ซื้ออย่างสุภาพด้วยข้อเท็จจริง แก้/คืนเงินเมื่อเหมาะสม และห้ามกดดันให้ลบรายงานหรือรีวิว
6. บันทึกเหตุการณ์และเพิ่ม regression check เพื่อไม่ให้เกิดซ้ำ

## 6. If TPT suspends or deactivates

ส่ง Support เป็นชุดเดียวที่อ่านง่าย:

- account/store name และอีเมล
- product ID/SKU และ URL
- timeline แบบสั้นและข้อเท็จจริงเท่านั้น
- exact uploaded ZIP พร้อม SHA-256
- rights ledger และหลักฐาน license
- reviewer signoffs, QA report และ malware-scan result
- สิ่งที่แก้แล้วและมาตรการป้องกันการเกิดซ้ำ

อย่าเปิดบัญชีใหม่เพื่อหลบการระงับ และอย่าส่งข้อความซ้ำหลายฉบับที่ข้อมูลขัดกัน

## Official references checked 2026-08-11

- https://www.teacherspayteachers.com/Terms-of-Service/
- https://help.teacherspayteachers.com/hc/en-us/articles/360042626591-What-are-TPT-s-Seller-Guidelines
- https://help.teacherspayteachers.com/hc/en-us/articles/360046747572-TPT-Content-Guidelines
- https://help.teacherspayteachers.com/hc/en-us/articles/360043021551-How-do-I-report-or-flag-a-resource-on-TPT
- https://help.teacherspayteachers.com/hc/en-us/articles/360042429692-Can-I-post-the-same-resource-more-than-once
- https://help.teacherspayteachers.com/hc/en-us/articles/12734392776468-What-does-TPT-do-if-they-suspect-a-resource-in-my-store-contains-malware
- https://openstax.org/books/chemistry-2e/pages/preface

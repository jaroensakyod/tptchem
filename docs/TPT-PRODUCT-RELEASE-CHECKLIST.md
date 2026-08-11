# TPT Product Release Checklist

ใช้เช็กลิสต์นี้กับสินค้าทุกชิ้นก่อนเปลี่ยนสถานะใน `catalog.json` เป็น `certified` และก่อนกด **Make Listing Active** บน TPT

## ความหมายของสถานะ

- `draft`: กำลังวิจัยหรือเขียน ยังห้ามอัปโหลด
- `packaged_pending_qa`: มีไฟล์แล้ว แต่ยังตรวจไม่ครบ
- `draft_pending_teacher_review`: ผ่านการตรวจระบบแล้ว แต่ยังขาดผู้ตรวจ/ทดลองใช้จริง
- `certified`: ผ่าน automated QA, human review, rights, malware, duplicate-listing และ account-safety gates พร้อมหลักฐาน release
- `published`: อัปโหลด ตรวจหน้าร้าน และเปิดขายแล้ว

## A. Product brief

- [ ] ระบุหัวข้อ กลุ่มผู้เรียน ระดับชั้น เวลาใช้ และ use case
- [ ] ระบุงานคิดของนักเรียนให้ต่างจากสินค้า format อื่นในหัวข้อเดียวกัน
- [ ] มี learning targets และ prerequisite ชัดเจน
- [ ] มี item blueprint: จำนวนข้อ ระดับความยาก ประเภทคำถาม และ misconception
- [ ] มีรายการไฟล์ที่จะส่งให้ผู้ซื้อก่อนเริ่มผลิต

## B. Research and rights

- [ ] ตรวจ pacing/ความต้องการจากแหล่งปัจจุบันมากกว่าหนึ่งแหล่ง
- [ ] ใช้หนังสือ เว็บไซต์ และใบงานตัวอย่างเป็น benchmark เท่านั้น หากสิทธิ์ไม่อนุญาตเชิงพาณิชย์
- [ ] ไม่คัดลอกคำถาม เฉลย ภาพ ลำดับหน้า หรือการจัดวางเฉพาะตัวของแหล่งอื่น
- [ ] ภาพทุกภาพมีชื่อผลงาน ผู้สร้าง URL ใบอนุญาต และตำแหน่งที่ใช้
- [ ] ใช้เฉพาะภาพฟรีที่อนุญาตการใช้เชิงพาณิชย์ หรือสัญลักษณ์ที่ตรวจสิทธิ์แล้ว
- [ ] ไม่มี code-drawn หรือ ImageGen visual เมื่อข้อกำหนดสินค้าห้ามใช้
- [ ] บันทึกหลักฐานใน `assets/manifest.json`, `assets/license-evidence/` และ source ledger
- [ ] ChemPride มีสถานะ `benchmark_only`; ไม่มีการคัดลอกหรือดัดแปลงข้อความ โจทย์ เฉลย ภาพ เลย์เอาต์ หรือลำดับ packet
- [ ] ไฟล์ OpenStax Chemistry 2e ในเครื่องมีสถานะ `blocked_direct_ai_and_commercial_reuse` จนกว่าจะพิสูจน์สิทธิ์ของไฟล์ฉบับนั้นได้
- [ ] ห้ามส่งหนังสือหรือแหล่งที่มีข้อห้าม LLM เข้า generative AI

## C. Content and answer key

- [ ] คำถามและตัวเลือกเป็นงานเขียนใหม่ทั้งหมด
- [ ] ทุกข้อมีคำตอบที่ตั้งใจไว้เพียงพอและอธิบายเหตุผลได้
- [ ] ตรวจคำตอบที่อาจถูกได้มากกว่าหนึ่งแบบ
- [ ] เฉลยตรงกับรหัสข้อ ลำดับ และเวอร์ชันนักเรียน
- [ ] มี acceptable alternatives, misconception notes และคำแนะนำครูเมื่อจำเป็น
- [ ] ข้อความด้านความปลอดภัยระบุว่า teacher/site policy และ current SDS มีลำดับเหนือคำแนะนำทั่วไป

## D. Buyer files

- [ ] Print-ready complete PDF
- [ ] Student-only PDF
- [ ] Low-ink/B&W PDF
- [ ] Teacher guide and answer key PDF
- [ ] Editable file เมื่อมีการโฆษณาว่า editable
- [ ] ไฟล์แยกสำหรับ station/portion เมื่อช่วยลดเวลาจัดเตรียมของครู
- [ ] Sources, credits, terms of use และ single-classroom license อยู่ในไฟล์สินค้า
- [ ] ชื่อไฟล์อ่านง่ายและไม่มีอักขระที่เสี่ยงต่อปัญหา ZIP

## E. Visual and technical QA

- [ ] มี Visual Plan ครบทุกข้อ/ทุกสถานการณ์/ทุกหน้ากิจกรรมก่อนเริ่มจัดหน้า
- [ ] ระบุเป็นรายข้อว่า `required` หรือ `not required` พร้อมเหตุผลด้านการเรียนรู้ที่ตรวจสอบได้
- [ ] ข้อที่ให้นักเรียนสังเกตอันตราย อุปกรณ์ สัญลักษณ์ ตำแหน่ง การจัดวาง หรือหลักฐานจากภาพ ห้ามเป็น text-only
- [ ] จำนวนภาพที่ต้องมี จำนวนที่มีจริง และรหัสข้อที่ยังขาดตรงกับ source และ QA report
- [ ] ถ้าภาพที่จำเป็นยังขาด ให้ตัดสินเป็น `FAIL/BLOCKED` ห้ามใช้คำว่า internally complete, release-ready หรือ certified
- [ ] ภาพการสอนทุกภาพเป็น free-source ที่อนุญาตเชิงพาณิชย์และมี URL/license/creator/ตำแหน่งใช้งานครบ
- [ ] ห้ามใช้ AI-generated หรือ code-drawn visual แทนภาพจริง เมื่อ product policy กำหนดให้ใช้ free-source verified imagery
- [ ] Render PDF ทุกหน้าและตรวจที่ขนาดอ่านจริง
- [ ] ตรวจ thumbnail view เพื่อดู hierarchy และความน่าอ่านเมื่อย่อ
- [ ] ตรวจ B&W/low-ink ว่าภาพและคำตอบยังแยกออกจากกันได้
- [ ] ไม่มีข้อความตัด ขอบชน ภาพยืด หน้าว่าง หรือเลขหน้าผิด
- [ ] รูปที่มีหน้าที่สอนมองเห็นรายละเอียดที่จำเป็นจริง
- [ ] PDF เปิดและพิมพ์ได้ และขนาดไฟล์ไม่ใหญ่เกินจำเป็น
- [ ] DOCX/PPTX เปิดและ render ในโปรแกรมเจ้าของไฟล์จริง
- [ ] รัน repository QA และไม่มี failure

## F. Human release gates

- [ ] Native-English cold read ผ่าน
- [ ] ครู Chemistry/Science ตรวจเนื้อหาและ safety action ทุกข้อ
- [ ] ทดลองใช้ในชั้นเรียนหรือ dry run เพื่อยืนยันเวลาและคำสั่ง
- [ ] บันทึกชื่อผู้ตรวจ วันที่ ข้อแก้ไข และผลตัดสิน
- [ ] แก้ตามผลตรวจ แล้วรัน content/visual/technical QA ซ้ำ
- [ ] เปลี่ยน `catalog.json` เป็น `certified` เฉพาะเมื่อทุกข้อด้านบนผ่าน

## G. Seller listing assets

- [ ] `TPT-LISTING-DRAFT.md` มีข้อความกรอกครบทุกช่อง
- [ ] Title ตรงกับสิ่งที่ผู้ซื้อได้รับจริง
- [ ] Description ระบุสิ่งที่รวมอยู่ จำนวนหน้า เวลาใช้ ระดับชั้น และ software ที่ต้องมี
- [ ] ระบุ Answer Key และ Editable อย่างตรงไปตรงมา
- [ ] Preview PDF แสดงเนื้อหาจริง แต่ไม่แจกคำตอบหรือสินค้าทั้งชุด
- [ ] Thumbnail 3–4 ภาพ แสดงปก หน้าจริง และ teacher support
- [ ] ภาพ thumbnail อย่างน้อย 750 × 750 px และต่ำกว่า 4 MB
- [ ] ราคาเทียบกับสินค้าที่ใกล้เคียงและสัมพันธ์กับขอบเขตจริง
- [ ] ไม่ติด standards ที่ยังไม่ได้ cross-check โดยตรง

## H. Final upload package

- [ ] สร้างโฟลเดอร์ใหม่สำหรับผู้ซื้อเท่านั้น
- [ ] เปลี่ยนชื่อไฟล์สำหรับผู้ซื้อให้สั้น อ่านง่าย และไม่ใช้อักขระพิเศษ
- [ ] ไม่ใส่ source JSON, QA report, research note, ภาพต้นฉบับ หรือ seller notes ใน ZIP
- [ ] บีบ buyer folder เป็น ZIP เมื่อสินค้ามีมากกว่าหนึ่งไฟล์
- [ ] แตก ZIP ในโฟลเดอร์ทดสอบใหม่และเปิดทุกไฟล์
- [ ] ตรวจว่าคำอธิบายหน้า TPT ระบุ PDF/DOCX/ZIP และ software ที่ต้องใช้
- [ ] บันทึก SHA-256 และเวอร์ชันของ ZIP ที่อัปโหลด
- [ ] สแกน ZIP ด้วย Microsoft Defender หรือ antivirus ที่ TPT ยอมรับ และบันทึกวัน เวลา scanner/version และผล
- [ ] สำรอง source, buyer ZIP, listing copy, listing screenshots, rights evidence และ release evidence ไว้นอก TPT

## I. TPT upload

- [ ] Seller Dashboard → Add new product → Digital Download
- [ ] อัปโหลด buyer ZIP เป็น Product File
- [ ] อัปโหลด `preview.pdf` เป็น Preview
- [ ] อัปโหลด listing images เป็น thumbnails ตามลำดับ
- [ ] กรอก title, description, grades, subjects, resource types, answer key, pages และ price จาก `TPT-LISTING-DRAFT.md`
- [ ] ยืนยันสิทธิ์ในเนื้อหาเฉพาะเมื่อ rights gate ผ่านแล้ว
- [ ] ปล่อย **Make Listing Active** ว่างไว้ระหว่างตรวจ draft
- [ ] เปิดดู listing draft บน desktop และ mobile-width
- [ ] ติ๊ก **Make Listing Active** เมื่อไฟล์ ราคา และข้อความตรงกันทั้งหมด

## J. After publishing

- [ ] ซื้อ/ดาวน์โหลดทดสอบหรือใช้ seller download เพื่อตรวจไฟล์ที่ผู้ซื้อได้รับจริง
- [ ] ตรวจ thumbnail, preview, title, price และ tags บนหน้าร้าน
- [ ] บันทึก product URL, publish date และ uploaded ZIP hash
- [ ] ตรวจคำถามจากผู้ซื้อและแก้ FAQ/description หากเกิดความสับสนซ้ำ
- [ ] ทบทวน views, conversion และ sales หลัง 30 วัน
- [ ] ทำ update log ทุกครั้งที่แก้ไฟล์ และอัปโหลดเวอร์ชันใหม่ให้ผู้ซื้อเดิม
- [ ] เริ่ม format ถัดไปเมื่อสินค้าปัจจุบันผ่าน release gate แล้ว

## K. Marketplace account-safety gate

- [ ] สินค้านี้ไม่ใช่ duplicate listing หรือ cosmetic variant ของสินค้าที่ลงอยู่แล้ว
- [ ] ถ้าเป็น variant มีความต่างเชิงสาระที่เปลี่ยนงานคิด/การใช้งาน และ description อธิบายความเหมือน/ต่างอย่างตรงไปตรงมา
- [ ] ไม่มีลิงก์ไปช่องทางขายอื่น ไม่มีสินค้าชิ้นเดียวกันฟรี/ถูกกว่าที่อื่น และไม่บังคับผู้ซื้อสมัครบัญชีเพิ่มเติม
- [ ] ชื่อบัญชี ตัวตน ภาษี และข้อมูลรับเงินตรงกับเจ้าของสิทธิ์จริง
- [ ] ไม่แชร์รหัสผ่าน; ผู้ช่วยเข้าผ่าน TPT VA Login เท่านั้น และเจ้าของร้านตรวจทุกการเปลี่ยนแปลง
- [ ] `RELEASE-EVIDENCE.md` มีชื่อผู้ตรวจ วันที่ ผลตัดสิน revision log, ZIP hash และ malware-scan result
- [ ] Automated QA ไม่ถูกใช้แทน native-English, subject-matter หรือ classroom review
- [ ] เก็บสำเนากฎ TPT/ใบอนุญาตที่ใช้ตัดสินใจพร้อม access date
- [ ] มี incident pack พร้อมส่ง Support: SKU, exact uploaded ZIP, SHA-256, listing snapshot, rights ledger, reviewer evidence และ timeline
- [ ] ถ้าได้รับ complaint/report ให้เก็บหลักฐานก่อน หยุด listing ชั่วคราวเมื่อมีความเสี่ยงจริง แก้จาก source และสื่อสารด้วยข้อเท็จจริง

## Definition of done

สินค้าถือว่า “ทำเสร็จ” เมื่อ buyer files, automated QA, human review, rights evidence, malware scan, duplicate/listing checks, listing copy, preview, thumbnails, buyer ZIP, release evidence และ post-upload verification ครบทั้งหมด ไม่ใช่เพียงสร้าง PDF สำเร็จ

## Official TPT references checked 2026-08-11

- Add a product: https://help.teacherspayteachers.com/hc/en-us/articles/360042864711-How-do-I-add-a-product-to-my-TPT-store
- Multiple files and ZIP: https://help.teacherspayteachers.com/hc/en-us/articles/360042865391-What-if-my-product-contains-more-than-one-file
- Supported file types: https://help.teacherspayteachers.com/hc/en-us/articles/360042429292-What-file-types-are-supported-on-TPT
- Thumbnail requirements: https://help.teacherspayteachers.com/hc/en-us/articles/360042865791-How-do-I-generate-thumbnails-for-my-products
- Thumbnail versus preview: https://help.teacherspayteachers.com/hc/en-us/articles/360042865851-What-s-the-difference-between-a-thumbnail-and-a-preview
- PDF accessibility for buyers: https://help.teacherspayteachers.com/hc/en-us/articles/360048983771-How-can-I-make-my-PDF-resources-easier-for-Buyers-to-access
- Terms, monitoring, account closure, credentials and backups: https://www.teacherspayteachers.com/Terms-of-Service/
- Seller Guidelines: https://help.teacherspayteachers.com/hc/en-us/articles/360042626591-What-are-TPT-s-Seller-Guidelines
- Content Guidelines: https://help.teacherspayteachers.com/hc/en-us/articles/360046747572-TPT-Content-Guidelines
- Copyright guidance: https://help.teacherspayteachers.com/hc/en-us/articles/360042548092-How-can-I-know-if-something-I-want-to-include-as-part-of-my-resource-is-copyrighted
- Duplicate listings: https://help.teacherspayteachers.com/hc/en-us/articles/360042429692-Can-I-post-the-same-resource-more-than-once
- Reports and Marketplace Protection review: https://help.teacherspayteachers.com/hc/en-us/articles/360043021551-How-do-I-report-or-flag-a-resource-on-TPT
- Malware process and approved scanners: https://help.teacherspayteachers.com/hc/en-us/articles/12734392776468-What-does-TPT-do-if-they-suspect-a-resource-in-my-store-contains-malware
- Third-party delivery restrictions: https://help.teacherspayteachers.com/hc/en-us/articles/360042199032-Can-I-offer-resources-that-are-hosted-on-a-third-party-site
- Current OpenStax Chemistry 2e license/LLM restriction: https://openstax.org/books/chemistry-2e/pages/preface

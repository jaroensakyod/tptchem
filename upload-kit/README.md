# CurioNest Upload Kit — Listing Drafts

> สถานะ 2026-08-10: ไฟล์ในโฟลเดอร์นี้เป็น **legacy listing drafts** ยังไม่ใช่
> ชุดอัปโหลดที่ตรวจว่าตรงกับสินค้าใน `products/`

## แหล่งข้อมูลที่ต้องเชื่อ

ใช้ `../catalog.json` เป็น source of truth ก่อนเปิดไฟล์ listing ทุกครั้ง ปัจจุบัน
catalog มี sellable candidates สองชุดเท่านั้น:

1. `CN-CH01-MATH` — `products/ch01-math-measurement/`
2. `CN-CH01-ESSENTIAL` — `products/ch01-essential-ideas/`

ทั้งสองชุดมีสถานะ `packaged_pending_qa` และยังไม่มี upload kit เวอร์ชันปัจจุบัน

## ไฟล์ 01-07 ในโฟลเดอร์นี้

ไฟล์เหล่านี้อ้างถึง professional/complete acid-base packs และ freebie ซึ่งไม่มี
package ตาม path ที่ระบุใน repository ปัจจุบัน จึงห้ามนำไปกรอก TPT โดยตรง:

- `01-professional-pack-b01.md`
- `02-professional-pack-b02.md`
- `03-professional-pack-b03.md`
- `04-complete-pack-b01.md`
- `05-complete-pack-b02.md`
- `06-complete-pack-b03.md`
- `07-freebie-sample.md`

เก็บไว้เป็น copy/SEO reference เท่านั้น เมื่อจะนำสินค้ากลับมาใช้ ต้องทำ package
มาตรฐานก่อน แล้วเพิ่ม Product ID และสถานะลง `catalog.json`

## เงื่อนไขก่อนสร้าง Upload Kit ใหม่

1. Product ID อยู่ใน `catalog.json`
2. Package มี PDF, editable DOCX, cover PNG และ preview PDF ครบ
3. `python qa.py all --strict` ผ่าน
4. มี QA record G1-G4 ที่ใช้ Product ID เดียวกับ catalog
5. Human visual QA และ native-English review ผ่าน
6. Asset attribution เป็น `verified`

หลังผ่านแล้วจึงสร้างไฟล์ชื่อ `<product-id>-listing.md` และระบุ path จาก package
จริง ห้ามใช้ชื่อไฟล์สำรองหรือข้อความ “ถ้าไม่มีให้ใช้...” ใน listing พร้อมขาย

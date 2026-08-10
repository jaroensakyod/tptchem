# ChemNest Glossary ไทย → อังกฤษ (v1.0)

> มาตรฐานคำศัพท์เดียวทั้งร้าน — ทุกชิ้นต้องใช้คำเหล่านี้เหมือนกัน (G2 Gate)
> เพิ่มเมื่อเจอศัพท์ใหม่ใน unit ถัดไป (โมล, สตอยชิโอเมทรี, อิเล็กโตรเคมี...) พร้อม bump version

## ข้อตกลงการเขียน (Conventions)

- **ตัวแปรเคมี**: ใช้ HTML `<sub>/<sup>` เสมอ (H<sub>2</sub>O, H<sub>3</sub>O<sup>+</sup>) — ห้ามเขียนติดกันแบบ "H2O"
- **สัญลักษณ์ประจุ**: ใช้ − (U+2212) สำหรับลบ, + ธรรมดาสำหรับบวก → H<sup>+</sup>, OH<sup>−</sup>, CO<sub>3</sub><sup>2−</sup>
- **[H⁺] vs [H₃O⁺]**: ใช้ [H<sup>+</sup>] ในบริบทคำนวณ pH (Q11, Q14, Q16, Q17...) · ใช้ H<sub>3</sub>O<sup>+</sup> ในนิยาม Arrhenius / ปฏิกิริยาในน้ำ (Q1, Q2)
- **คำว่า "dissociate"**: ใช้กับทั้งกรด/เบส · "ionize" ใช้กับโมเลกุลกรดได้ (ไม่ผิด) แต่ให้เลือกอย่างใดอย่างหนึ่งต่อชิ้น
- **การสะกด**: ใช้แบบ US (percent, ionization, color) ทั้งร้าน — ไม่ผสม UK
- **ระดับชั้น**: Grades 9-12 (ไม่ใช้ Year 9 / Form 4)
- **ขีดกลาง**: Brønsted–Lowry / acid–base ใช้ en dash (–) เสมอ

## คำศัพท์หลัก (Acid–Base Unit)

| ไทย | อังกฤษ (มาตรฐาน) | หมายเหตุ |
|---|---|---|
| กรด / เบส | acid / base | |
| ทฤษฎีอาร์เรเนียส | Arrhenius theory | "Arrhenius acid/base" |
| ทฤษฎีบรอนสเตด–ลาวรี | Brønsted–Lowry theory | en dash, ไม่ใช่ hyphen |
| ทฤษฎีลิวอิส | Lewis theory | Lewis acid = electron-pair acceptor |
| คู่กรด–เบสสัมพันธ์ | conjugate acid–base pair | conjugate acid / conjugate base |
| กรดแก่ / กรดอ่อน | strong acid / weak acid | |
| เบสแก่ / เบสอ่อน | strong base / weak base | |
| ความแรงของกรด | acid strength | อย่าใช้ "acid power" |
| ความเข้มข้น | concentration | อย่าสับสนกับ strength |
| ค่าคงที่การแตกตัวของกรด | acid dissociation constant (K<sub>a</sub>) | |
| ค่าคงที่การแตกตัวของเบส | base dissociation constant (K<sub>b</sub>) | |
| ผลคูณไอออนของน้ำ | ion-product constant of water (K<sub>w</sub>) | |
| ร้อยละการแตกตัว | percent ionization | US spelling เสมอ |
| ผลไอออนร่วม | common-ion effect | |
| สารละลายบัฟเฟอร์ | buffer solution | |
| ไฮโดรเนียมไอออน | hydronium ion (H<sub>3</sub>O<sup>+</sup>) | |
| การแตกตัว | dissociation | |
| การแตกตัวเป็นไอออน | ionization | |
| สมดุลเคมี | chemical equilibrium | |
| หลักของเลอชาเตอลิเยร์ | Le Chatelier's principle | |
| ตาราง ICE | ICE table | Initial/Change/Equilibrium |
| กฎ 5% | the 5% rule | small-x assumption check |
| การประมาณ x น้อย | small-x approximation | |
| กรดหลายโปรตอน | polyprotic acid | |
| แอมโฟเทอริก | amphoteric | amphiprotic = ให้/รับโปรตอนได้ |
| ไทเทรชัน | titration | |
| จุดสมมูล | equivalence point | |
| อินดิเคเตอร์ | indicator | |
| ไฮโดรไลซิส | hydrolysis | |
| ตัวทำละลาย / ตัวถูกละลาย | solvent / solute | |
| โมลาริตี | molarity (M) | mol/L |
| มวลโมลาร์ | molar mass | g/mol |
| โมล | mole | |
| รากของสมการ | root of the equation | ICE quadratic |
| เงื่อนไข/สมมติฐาน | assumption | |
| สารละลาย | solution | |
| pH | pH | ไม่มีตัวเอียง ไม่ใช่ "PH" |
| pOH / pK<sub>a</sub> / pK<sub>b</sub> | เหมือนเดิม | ใช้ <sub> เสมอ |

## คำ/วลีที่ห้ามใช้ (AI-isms — ตัดออกตอน G2)

- ~~"Dive into the world of..."~~ → ขึ้นตรง ๆ เลย
- ~~"Unlock your potential"~~ / ~~"elevate your classroom"~~ → ตัด
- ~~"This resource is perfect for..."~~ ซ้ำทุกชิ้น → ใช้ไม่เกิน 1 ครั้งต่อ description
- ~~"Engaging!"~~ ลอย ๆ โดยไม่มีเหตุผล → เปลี่ยนเป็นข้อเท็จจริง ("20 questions with answer key")
- ประโยคชมตัวเองซ้ำ ๆ ในทุกหน้า → ตัด

## ขั้นตอนเพิ่มศัพท์ใหม่

1. เจอศัพท์ที่ยังไม่มี → เสนอ + ตัวอย่างบริบท
2. owner อนุมัติ → เพิ่มในตาราง + bump version
3. แก้ทุกชิ้นที่ใช้ศัพท์เก่าให้ตรง (log ใน QA log)

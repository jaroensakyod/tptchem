#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ChemNest Analytics — ระบบเก็บ-วิเคราะห์-ปรับปรุง (kpi_log.json)

คำสั่ง:
  analytics.py init                              สร้าง kpi_log.json skeleton
  analytics.py log --date YYYY-MM-DD --product ID --views N [--previews N]
                   [--wishlists N] [--sales N] [--revenue N] [--notes "..."]
  analytics.py import --file <TPT Product Statistics.csv>
  analytics.py keyword --product ID --kw "..." --visits N --conv N [--earnings N]
  analytics.py ab --product ID --field title|cover|price --to "..." [--reason "..."]
  analytics.py report [--days 7]                 สรุปรายวัน + flag อัตโนมัติ

ใช้ --data <path> เพื่อชี้ไฟล์อื่น (เช่น ทดสอบใน temp)
"""
import argparse, csv, json, os, sys
from collections import defaultdict
from datetime import date, datetime, timedelta

DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kpi_log.json")

def load(path):
    if not os.path.exists(path):
        print(f"ERROR: ไม่พบ {path} — รัน 'analytics.py init' ก่อน", file=sys.stderr)
        sys.exit(1)
    return json.load(open(path, encoding="utf-8"))

def save(path, data):
    data["updated"] = datetime.now().isoformat(timespec="seconds")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

def get_product(data, pid):
    if pid not in data["products"]:
        data["products"][pid] = {"title": pid, "price": None, "publish_date": None,
                                 "batch": None, "qa_status": "draft",
                                 "daily": [], "keywords": [], "ab_tests": [], "rating": None}
    return data["products"][pid]

# ---------------------------------------------------------------- commands
def cmd_init(args, path):
    data = {"schema_version": 1, "updated": None, "products": {}}
    save(path, data)
    print(f"init: สร้าง {path} แล้ว")

def cmd_log(args, path):
    data = load(path)
    p = get_product(data, args.product)
    for d in p["daily"]:
        if d["date"] == args.date:
            d.update(views=args.views, previews=args.previews, wishlists=args.wishlists,
                     sales=args.sales, revenue=args.revenue, notes=args.notes or d.get("notes"))
            break
    else:
        p["daily"].append({"date": args.date, "views": args.views, "previews": args.previews,
                           "wishlists": args.wishlists, "sales": args.sales,
                           "revenue": args.revenue, "notes": args.notes})
    p["daily"].sort(key=lambda x: x["date"])
    save(path, data)
    print(f"log: {args.product} @ {args.date} views={args.views} sales={args.sales} rev=${args.revenue}")

def cmd_import(args, path):
    data = load(path)
    rows = list(csv.DictReader(open(args.file, encoding="utf-8-sig")))
    if not rows:
        print("ERROR: CSV ว่าง", file=sys.stderr); sys.exit(1)
    cols = {k.strip().lower(): k for k in rows[0].keys()}
    def col(*names):
        for n in names:
            if n in cols: return cols[n]
        return None
    c_title, c_views, c_sales, c_earn, c_conv = col("title", "product"), col("views", "page views"), \
        col("sales", "units sold", "downloads"), col("earnings", "revenue", "gross earnings"), \
        col("conversion", "conversion rate")
    if not (c_title and (c_views or c_sales)):
        print("ERROR: หา column ไม่เจอ (คาด: Title/Views/Sales/Earnings) — header จริง:", list(rows[0].keys()), file=sys.stderr)
        sys.exit(1)
    today = date.today().isoformat()
    n = 0
    for r in rows:
        title = (r.get(c_title) or "").strip()
        if not title: continue
        pid = f"CSV-{abs(hash(title)) % 10**7}"  # fallback id; ผู้ใช้ map เป็น CN-xxx ทีหลัง
        p = get_product(data, pid)
        if p["title"] == pid: p["title"] = title
        views = int(float((r.get(c_views) or 0) or 0)); sales = int(float((r.get(c_sales) or 0) or 0))
        earn = float((r.get(c_earn) or 0) or 0)
        p["daily"].append({"date": today, "views": views, "previews": 0, "wishlists": 0,
                           "sales": sales, "revenue": earn, "notes": "imported CSV"})
        n += 1
    save(path, data)
    print(f"import: {n} สินค้า จาก {args.file} — ตรวจสอบ id (CSV-xxxxx) แล้ว map เป็น CN-xxx")

def cmd_keyword(args, path):
    data = load(path)
    p = get_product(data, args.product)
    p["keywords"].append({"kw": args.kw, "visits": args.visits, "conversions": args.conv,
                          "earnings": args.earnings, "date": date.today().isoformat()})
    save(path, data)
    print(f"keyword: {args.product} ← '{args.kw}' visits={args.visits} conv={args.conv}")

def cmd_ab(args, path):
    data = load(path)
    p = get_product(data, args.product)
    p["ab_tests"].append({"date": date.today().isoformat(), "field": args.field,
                          "to": args.to, "reason": args.reason})
    save(path, data)
    print(f"ab: {args.product} เปลี่ยน {args.field} → '{args.to}' ({args.reason})")

def cmd_report(args, path):
    data = load(path)
    days = args.days
    today = date.today()
    since = (today - timedelta(days=days)).isoformat()
    print(f"=== ChemNest Daily Report ({today}) — ช่วง {days} วัน ===")
    tot_v = tot_s = 0; tot_r = 0.0; flag_any = False
    rows = []
    for pid, p in sorted(data["products"].items()):
        dl = [d for d in p["daily"] if d["date"] >= since]
        v = sum(d["views"] for d in dl); s = sum(d["sales"] for d in dl); r = sum(d["revenue"] for d in dl)
        last = dl[-1] if dl else None
        conv = (s / v * 100) if v else 0.0
        tot_v += v; tot_s += s; tot_r += r
        rows.append((pid, p["title"][:40], p.get("publish_date"), v, s, r, conv, last))
    print(f"รวม: views={tot_v} · sales={tot_s} · revenue=${tot_r:.2f} · conv={tot_s/tot_v*100 if tot_v else 0:.1f}%")
    print(f"{'ID':<12}{'views':>6}{'sales':>6}{'rev$':>8}{'conv%':>7}  flag")
    for pid, title, pub, v, s, r, conv, last in rows:
        flags = []
        recent7 = [d for d in p["daily"] if d["date"] >= (today - timedelta(days=7)).isoformat()]
        if v == 0 and len(recent7) >= 7: flags.append("⚠ SEO: 0 views 7 วัน → เปลี่ยน title/keyword")
        if v > 0 and s == 0: flags.append("⚠ conversion: มี views ไม่มี sales → ตรวจ cover/ราคา")
        if s >= 3: flags.append("★ ขายดี → ทำ sequel/bundle")
        print(f"{pid:<12}{v:>6}{s:>6}{r:>8.2f}{conv:>7.1f}  {' | '.join(flags)}")
        if flags: flag_any = True
    if not flag_any: print("(ไม่มี flag — ทุกสินค้าปกติ)")
    print("\nแนะนำ: ดู Search Analytics สัปดาห์ละครั้ง + อย่าตัดสินใจจาก <7 วัน")

def main():
    ap = argparse.ArgumentParser(description="ChemNest Analytics")
    ap.add_argument("--data", default=DEFAULT)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.set_defaults(fn=cmd_init)
    p = sub.add_parser("log"); p.add_argument("--date", required=True); p.add_argument("--product", required=True)
    p.add_argument("--views", type=int, default=0); p.add_argument("--previews", type=int, default=0)
    p.add_argument("--wishlists", type=int, default=0); p.add_argument("--sales", type=int, default=0)
    p.add_argument("--revenue", type=float, default=0.0); p.add_argument("--notes", default=None)
    p.set_defaults(fn=cmd_log)
    p = sub.add_parser("import"); p.add_argument("--file", required=True); p.set_defaults(fn=cmd_import)
    p = sub.add_parser("keyword"); p.add_argument("--product", required=True); p.add_argument("--kw", required=True)
    p.add_argument("--visits", type=int, default=0); p.add_argument("--conv", type=int, default=0)
    p.add_argument("--earnings", type=float, default=0.0); p.set_defaults(fn=cmd_keyword)
    p = sub.add_parser("ab"); p.add_argument("--product", required=True)
    p.add_argument("--field", choices=["title", "cover", "price", "tags"], required=True)
    p.add_argument("--to", required=True); p.add_argument("--reason", default=""); p.set_defaults(fn=cmd_ab)
    p = sub.add_parser("report"); p.add_argument("--days", type=int, default=7); p.set_defaults(fn=cmd_report)
    args = ap.parse_args()
    args.fn(args, args.data)

if __name__ == "__main__":
    main()

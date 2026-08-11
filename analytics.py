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
import argparse, csv, hashlib, json, os, sys
from collections import defaultdict
from datetime import date, datetime, timedelta

DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kpi_log.json")

def load(path):
    if not os.path.exists(path):
        print(f"ERROR: ไม่พบ {path} — รัน 'analytics.py init' ก่อน", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)

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
    product = data["products"][pid]
    product.setdefault("daily", [])
    product.setdefault("keywords", [])
    product.setdefault("ab_tests", [])
    return product

def parse_iso_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        print(f"ERROR: วันที่ต้องเป็น YYYY-MM-DD: {value}", file=sys.stderr)
        sys.exit(1)

def stable_product_id(title):
    digest = hashlib.sha256(title.strip().lower().encode("utf-8")).hexdigest()[:10]
    return f"CSV-{digest}"

def number(value, integer=False):
    raw = str(value or "0").strip().replace(",", "").replace("$", "").replace("%", "")
    try:
        parsed = float(raw or 0)
    except ValueError:
        parsed = 0.0
    return int(parsed) if integer else parsed

def upsert_by_date(items, entry):
    for current in items:
        if current.get("date") == entry["date"]:
            current.update(entry)
            return
    items.append(entry)
    items.sort(key=lambda x: x.get("date", ""))

# ---------------------------------------------------------------- commands
def cmd_init(args, path):
    if os.path.exists(path) and not args.force:
        print(f"ERROR: {path} มีอยู่แล้ว — ใช้ init --force หากต้องการเขียนทับ", file=sys.stderr)
        sys.exit(1)
    data = {"schema_version": 1, "updated": None, "products": {}}
    save(path, data)
    print(f"init: สร้าง {path} แล้ว")

def cmd_log(args, path):
    data = load(path)
    p = get_product(data, args.product)
    log_date = parse_iso_date(args.date)
    previous = next((d for d in p["daily"] if d.get("date") == log_date), {})
    upsert_by_date(p["daily"], {"date": log_date, "views": args.views,
                   "previews": args.previews, "wishlists": args.wishlists,
                   "sales": args.sales, "revenue": args.revenue,
                   "notes": args.notes or previous.get("notes"), "source": "manual"})
    save(path, data)
    print(f"log: {args.product} @ {args.date} views={args.views} sales={args.sales} rev=${args.revenue}")

def cmd_import(args, path):
    data = load(path)
    with open(args.file, encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        print("ERROR: CSV ว่าง", file=sys.stderr); sys.exit(1)
    cols = {k.strip().lower(): k for k in rows[0].keys()}
    def col(*names):
        for n in names:
            if n in cols: return cols[n]
        return None
    c_id = col("product id", "resource id", "id")
    c_title, c_views, c_sales, c_earn, c_conv = col("title", "product"), col("views", "page views"), \
        col("sales", "units sold", "downloads"), col("earnings", "revenue", "gross earnings"), \
        col("conversion", "conversion rate")
    if not (c_title and (c_views or c_sales)):
        print("ERROR: หา column ไม่เจอ (คาด: Title/Views/Sales/Earnings) — header จริง:", list(rows[0].keys()), file=sys.stderr)
        sys.exit(1)
    report_date = parse_iso_date(args.date or date.today().isoformat())
    n = 0
    for r in rows:
        title = (r.get(c_title) or "").strip()
        if not title: continue
        external_id = (r.get(c_id) or "").strip() if c_id else ""
        pid = f"TPT-{external_id}" if external_id else stable_product_id(title)
        p = get_product(data, pid)
        if p["title"] == pid: p["title"] = title
        views = number(r.get(c_views), integer=True) if c_views else 0
        sales = number(r.get(c_sales), integer=True) if c_sales else 0
        earn = number(r.get(c_earn)) if c_earn else 0.0
        entry = {"date": report_date, "views": views, "sales": sales,
                 "revenue": earn, "source": "tpt_csv"}
        if args.mode == "snapshot":
            snapshots = p.setdefault("statistics_snapshots", [])
            upsert_by_date(snapshots, entry)
        else:
            entry.update({"previews": 0, "wishlists": 0, "notes": "imported CSV period"})
            upsert_by_date(p["daily"], entry)
        n += 1
    save(path, data)
    print(f"import: {n} สินค้า จาก {args.file} ({args.mode} @ {report_date})")

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
    old_value = p.get(args.field)
    new_value = number(args.to) if args.field == "price" else args.to
    p["ab_tests"].append({"date": date.today().isoformat(), "field": args.field,
                          "from": old_value, "to": new_value, "reason": args.reason})
    p[args.field] = new_value
    save(path, data)
    print(f"ab: {args.product} เปลี่ยน {args.field} → '{args.to}' ({args.reason})")

def cmd_report(args, path):
    data = load(path)
    days = args.days
    today = date.today()
    since = (today - timedelta(days=max(days - 1, 0))).isoformat()
    print(f"=== ChemNest Daily Report ({today}) — ช่วง {days} วัน ===")
    tot_v = tot_s = 0; tot_r = 0.0; flag_any = False
    rows = []
    for pid, p in sorted(data["products"].items()):
        dl = [d for d in p["daily"] if since <= d["date"] <= today.isoformat()]
        v = sum(d["views"] for d in dl); s = sum(d["sales"] for d in dl); r = sum(d["revenue"] for d in dl)
        last = dl[-1] if dl else None
        basis = "daily"
        if not dl and p.get("statistics_snapshots"):
            eligible = [x for x in p["statistics_snapshots"] if x.get("date", "") <= today.isoformat()]
            if eligible:
                latest = sorted(eligible, key=lambda x: x["date"])[-1]
                before = [x for x in eligible if x.get("date", "") < since]
                baseline = sorted(before, key=lambda x: x["date"])[-1] if before else None
                if baseline:
                    v = max(0, latest["views"] - baseline["views"])
                    s = max(0, latest["sales"] - baseline["sales"])
                    r = max(0.0, latest["revenue"] - baseline["revenue"])
                    basis = "snapshot-delta"
                else:
                    v, s, r = latest["views"], latest["sales"], latest["revenue"]
                    basis = "snapshot-total"
        conv = (s / v * 100) if v else 0.0
        tot_v += v; tot_s += s; tot_r += r
        rows.append((pid, p, v, s, r, conv, last, basis))
    print(f"รวม: views={tot_v} · sales={tot_s} · revenue=${tot_r:.2f} · conv={tot_s/tot_v*100 if tot_v else 0:.1f}%")
    print(f"{'ID':<12}{'views':>6}{'sales':>6}{'rev$':>8}{'conv%':>7}  flag")
    for pid, p, v, s, r, conv, last, basis in rows:
        flags = []
        recent7_since = (today - timedelta(days=6)).isoformat()
        recent7 = [d for d in p["daily"] if d["date"] >= recent7_since]
        if v == 0 and len({d["date"] for d in recent7}) >= 7: flags.append("⚠ SEO: 0 views 7 วัน → เปลี่ยน title/keyword")
        if v > 0 and s == 0: flags.append("⚠ conversion: มี views ไม่มี sales → ตรวจ cover/ราคา")
        if s >= 3: flags.append("★ ขายดี → ทำ sequel/bundle")
        if basis == "snapshot-total": flags.append("ℹ snapshot แรก: ตัวเลขเป็นยอดสะสม")
        print(f"{pid:<12}{v:>6}{s:>6}{r:>8.2f}{conv:>7.1f}  {' | '.join(flags)}")
        if flags: flag_any = True
    if not flag_any: print("(ไม่มี flag — ทุกสินค้าปกติ)")
    print("\nแนะนำ: ดู Search Analytics สัปดาห์ละครั้ง + อย่าตัดสินใจจาก <7 วัน")

def main():
    ap = argparse.ArgumentParser(description="ChemNest Analytics")
    ap.add_argument("--data", default=DEFAULT)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("--force", action="store_true"); p.set_defaults(fn=cmd_init)
    p = sub.add_parser("log"); p.add_argument("--date", required=True); p.add_argument("--product", required=True)
    p.add_argument("--views", type=int, default=0); p.add_argument("--previews", type=int, default=0)
    p.add_argument("--wishlists", type=int, default=0); p.add_argument("--sales", type=int, default=0)
    p.add_argument("--revenue", type=float, default=0.0); p.add_argument("--notes", default=None)
    p.set_defaults(fn=cmd_log)
    p = sub.add_parser("import"); p.add_argument("--file", required=True)
    p.add_argument("--date"); p.add_argument("--mode", choices=["snapshot", "period"], default="snapshot")
    p.set_defaults(fn=cmd_import)
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

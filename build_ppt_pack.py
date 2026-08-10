#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CurioNest PPTX Lesson builder — mirror-json → teacher slide deck (pptxgenjs).

Turns the SAME schema as build_mirror_pack.py into a PowerPoint deck:
  header           → title slide (dark)
  learning_objectives → objectives slide (icon rows)
  concept          → one slide per concept: banner title + body + worked example box
  practice         → practice slides (question list + answer box)
  vocabulary       → key terms slide (2-col)
  answer_key       → answer key slides

Usage: python build_ppt_pack.py mirror-json/b01-mirror.json [outstem]
Writes <stem>.pptx via a generated Node script (pptxgenjs). QA:
  markitdown / validate.py — see powerpoint skill.
"""
import json, os, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))

JS_TEMPLATE = r"""
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const data = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
const out = process.argv[3];

const INDIGO = "312E81", PURPLE = "4F46E5", SLATE = "334155", GRAY = "64748B";
const RED = "9F1239", WHITE = "FFFFFF", GOLD = "FFB84D", GREEN = "15803D";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.3 x 7.5
pptx.author = "CurioNest";
pptx.title = data.title || "CurioNest Lesson";

function stripTags(s) { return (s || "").replace(/<[^>]+>/g, ""); }

// ---------- helpers ----------
function titleSlide(s) {
  const slide = pptx.addSlide();
  slide.background = { color: INDIGO };
  slide.addText("CURIONEST", { x: 0.6, y: 0.5, w: 12, h: 0.6, fontSize: 18, color: GOLD, bold: true, align: "center" });
  slide.addText(stripTags(s.title || ""), { x: 0.8, y: 1.8, w: 11.7, h: 1.4, fontSize: 40, color: WHITE, bold: true, align: "center" });
  slide.addText(stripTags(s.subtitle || ""), { x: 0.8, y: 3.4, w: 11.7, h: 0.9, fontSize: 20, color: GOLD, align: "center" });
  // accent circles motif (molecule)
  slide.addShape("ellipse", { x: 1.0, y: 5.6, w: 0.35, h: 0.35, fill: { color: GOLD } });
  slide.addShape("ellipse", { x: 6.4, y: 5.6, w: 0.35, h: 0.35, fill: { color: "8AB4F8" } });
  slide.addShape("ellipse", { x: 11.9, y: 5.6, w: 0.35, h: 0.35, fill: { color: "7FD1AE" } });
  slide.addText("Made by a chemistry teacher · CurioNest", { x: 0.6, y: 6.6, w: 12, h: 0.5, fontSize: 13, color: "C9D4E8", align: "center" });
}

function objectivesSlide(s) {
  const slide = pptx.addSlide();
  slide.background = { color: WHITE };
  slide.addText(stripTags(s.title || "Learning Objectives"), { x: 0.6, y: 0.4, w: 12, h: 0.8, fontSize: 30, color: INDIGO, bold: true });
  const items = s.items || [];
  items.forEach((obj, i) => {
    const y = 1.5 + i * 0.95;
    slide.addShape("ellipse", { x: 0.8, y: y + 0.05, w: 0.5, h: 0.5, fill: { color: PURPLE } });
    slide.addText(String(i + 1), { x: 0.8, y: y + 0.05, w: 0.5, h: 0.5, fontSize: 18, color: WHITE, bold: true, align: "center", valign: "middle" });
    slide.addText(stripTags(obj), { x: 1.6, y: y, w: 11, h: 0.7, fontSize: 16, color: SLATE, valign: "middle" });
  });
}

function conceptSlide(s) {
  const slide = pptx.addSlide();
  slide.background = { color: WHITE };
  // banner
  slide.addShape("roundRect", { x: 0.6, y: 0.4, w: 12.1, h: 0.9, fill: { color: PURPLE }, rectRadius: 0.08 });
  slide.addText(stripTags(s.title || "Concept"), { x: 0.9, y: 0.4, w: 11.5, h: 0.9, fontSize: 22, color: WHITE, bold: true, valign: "middle" });
  // body text
  const body = (s.body || []).join("\n\n");
  slide.addText(stripTags(body), { x: 0.7, y: 1.5, w: 11.9, h: 3.4, fontSize: 14, color: SLATE, valign: "top", lineSpacing: 22 });
  // worked example box
  const we = s.worked_example;
  if (we) {
    slide.addShape("roundRect", { x: 0.7, y: 5.1, w: 11.9, h: 1.9, fill: { color: "FFF7ED" }, rectRadius: 0.06, line: { color: "FDBA74", width: 1.5 } });
    slide.addText("★ Worked Example", { x: 1.0, y: 5.2, w: 11, h: 0.35, fontSize: 13, color: "C2410C", bold: true });
    slide.addText(stripTags(we.question || ""), { x: 1.0, y: 5.55, w: 11.3, h: 0.6, fontSize: 12, color: SLATE });
    slide.addText("Solution: " + stripTags(we.solution || ""), { x: 1.0, y: 6.2, w: 11.3, h: 0.7, fontSize: 12, color: GREEN, italic: true });
  }
}

function practiceSlide(s, numStart) {
  const slide = pptx.addSlide();
  slide.background = { color: WHITE };
  slide.addText(stripTags(s.title || "Practice"), { x: 0.6, y: 0.4, w: 12, h: 0.7, fontSize: 26, color: INDIGO, bold: true });
  const items = s.items || [];
  const maxRows = 5;
  items.slice(0, maxRows).forEach((item, i) => {
    const n = numStart + i;
    const y = 1.3 + i * 1.1;
    slide.addText(n + ".", { x: 0.7, y: y, w: 0.6, h: 0.5, fontSize: 16, color: INDIGO, bold: true });
    slide.addText(stripTags(item.q || ""), { x: 1.4, y: y, w: 11.2, h: 0.9, fontSize: 14, color: SLATE, valign: "top" });
  });
  if (items.length > maxRows) {
    slide.addText("(continued on next slide…)", { x: 1.4, y: 6.8, w: 10, h: 0.4, fontSize: 11, color: GRAY, italic: true });
  }
}

function vocabSlide(s) {
  const slide = pptx.addSlide();
  slide.background = { color: WHITE };
  slide.addText(stripTags(s.title || "Key Terms"), { x: 0.6, y: 0.4, w: 12, h: 0.7, fontSize: 26, color: INDIGO, bold: true });
  const items = s.items || [];
  const colW = 6.0;
  items.forEach((it, i) => {
    const term = Array.isArray(it) ? it[0] : it.term;
    const def = Array.isArray(it) ? it[1] : it.def;
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.7 + col * colW, y = 1.3 + row * 1.15;
    slide.addShape("roundRect", { x: x, y: y, w: colW - 0.4, h: 1.0, fill: { color: "EEF2FF" }, rectRadius: 0.05 });
    slide.addText(stripTags(term), { x: x + 0.15, y: y + 0.08, w: colW - 0.7, h: 0.35, fontSize: 14, color: INDIGO, bold: true });
    slide.addText(stripTags(def), { x: x + 0.15, y: y + 0.45, w: colW - 0.7, h: 0.5, fontSize: 11, color: SLATE });
  });
}

function answerSlide(s, numStart) {
  const slide = pptx.addSlide();
  slide.background = { color: WHITE };
  slide.addText(stripTags(s.title || "Answer Key"), { x: 0.6, y: 0.4, w: 12, h: 0.7, fontSize: 26, color: GREEN, bold: true });
  const items = s.items || [];
  items.slice(0, 6).forEach((item, i) => {
    const n = numStart + i;
    const y = 1.3 + i * 0.95;
    slide.addText(n + ".", { x: 0.7, y: y, w: 0.6, h: 0.5, fontSize: 15, color: GREEN, bold: true });
    slide.addText(stripTags(item.answer || ""), { x: 1.4, y: y, w: 11.2, h: 0.85, fontSize: 13, color: SLATE });
  });
}

// ---------- build ----------
const sections = data.sections || [];
let practiceIdx = 0;
let numStart = 1;
for (const s of sections) {
  if (s.kind === "header") titleSlide(s);
  else if (s.kind === "learning_objectives") objectivesSlide(s);
  else if (s.kind === "concept") conceptSlide(s);
  else if (s.kind === "practice") {
    practiceSlide(s, numStart);
    numStart += (s.items || []).length;
  } else if (s.kind === "vocabulary") vocabSlide(s);
  else if (s.kind === "answer_key") {
    // answer key: collect all practice items
    const all = [];
    for (const ss of sections) {
      if (ss.kind === "practice") all.push(...(ss.items || []));
    }
    const per = 6;
    for (let i = 0; i < all.length; i += per) {
      const slide = pptx.addSlide();
      slide.background = { color: WHITE };
      slide.addText("Answer Key", { x: 0.6, y: 0.4, w: 12, h: 0.7, fontSize: 26, color: GREEN, bold: true });
      all.slice(i, i + per).forEach((item, k) => {
        const n = i + k + 1;
        const y = 1.3 + k * 0.95;
        slide.addText(n + ".", { x: 0.7, y: y, w: 0.6, h: 0.5, fontSize: 15, color: GREEN, bold: true });
        slide.addText(stripTags(item.answer || ""), { x: 1.4, y: y, w: 11.2, h: 0.85, fontSize: 13, color: SLATE });
      });
    }
  }
}

pptx.writeFile(out).then(() => console.log("PPTX saved: " + out));
"""

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python build_ppt_pack.py mirror-json/b01-mirror.json [outstem]")
    src = sys.argv[1]
    data = json.load(open(src, encoding="utf-8"))
    stem = sys.argv[2] if len(sys.argv) > 2 else data.get("meta", {}).get("file_stem", "pack")
    js_path = os.path.join(BASE, f"_gen_{stem}.js")
    pptx_path = os.path.join(BASE, f"{stem}.pptx")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(JS_TEMPLATE)
    r = subprocess.run(["node", js_path, os.path.abspath(src), os.path.abspath(pptx_path)],
                       capture_output=True, text=True, timeout=120, cwd=BASE)
    os.remove(js_path)
    if r.returncode != 0:
        sys.exit(f"node failed: {r.stderr[-500:]}")
    print(r.stdout.strip())
    print(f"pptx saved: {pptx_path}")

if __name__ == "__main__":
    main()

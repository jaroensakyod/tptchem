#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LaTeX → OMML (Office Math Markup Language) — Word's native equation format.

Turns LaTeX-like strings into real Word equations (Cambria Math, professional
layout) that python-docx can inject into .docx paragraphs.

Supported subset:
  plain text, _{} / ^{} sub/sup, \\frac{a}{b}, \\sqrt{x}, \\text{...},
  \\log, \\ln, \\times, \\rightarrow, \\leftarrow, \\approx, \\cdot,
  \\le, \\ge, \\neq, \\pm, \\infty, \\left( \\right) \\left[ \\right],
  Greek: \\alpha \\beta \\gamma \\delta \\theta \\Delta \\pi \\mu \\nu \\omega,
  [ ] ( ) as delimiters when paired
"""
import re

# ---------------------------------------------------------------- tokens
_SYM = {
    r"\times": "×", r"\rightarrow": "→", r"\leftarrow": "←", r"\approx": "≈",
    r"\cdot": "·", r"\le": "≤", r"\ge": "≥", r"\neq": "≠", r"\pm": "±",
    r"\infty": "∞", r"\cdotp": "·", r"\rightleftharpoons": "⇌", r"\leftrightarrow": "↔",
    r"\degree": "°", r"\circ": "°", r"\propto": "∝", r"\Delta": "Δ",
    r"\Rightarrow": "⇒", r"\Longrightarrow": "⟹", r"\Longleftarrow": "⟸",
    r"\longrightarrow": "⟶", r"\longleftarrow": "⟵", r"\quad": " ", r"\qquad": "  ", r"\,": " ", r"\ ": " ", r"\;": " ",
}
_GREEK = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\theta": "θ", r"\Delta": "Δ", r"\pi": "π", r"\mu": "μ", r"\nu": "ν",
    r"\omega": "ω", r"\lambda": "λ", r"\sigma": "σ", r"\phi": "φ", r"\Phi": "Φ",
}
_OPEN = {"(": "(", "[": "[", "{": "{"}
_CLOSE = {")": ")", "]": "]", "}": "}"}
_MATH_FUNCS = {"\\log", "\\ln", "\\sin", "\\cos", "\\tan", "\\exp", "\\det", "\\lim"}


def _r(text):
    """math run"""
    return '<m:r><m:t xml:space="preserve">%s</m:t></m:r>' % _esc(text)


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _wrap(xml, tag, extra=""):
    return f'<m:{tag}{extra}>{xml}</m:{tag}>'


# ---------------------------------------------------------------- mhchem-style \ce{} support
_CE_ARROWS = {
    "->": "→", "-->": "⟶", "<-": "←", "<-->": "⟷", "<->": "⇌",
    "<=>": "⇌", "<=>>": "⇌", "<<=>": "⇌", "=>": "⇒",
}
_CE_STATES = {"s", "l", "g", "aq", "cr", "am"}


def _ce_tokenize(ce):
    """Split \\ce{} content into (text, sub, sup) runs, mhchem-style."""
    out = []
    i, n = 0, len(ce)
    while i < n:
        ch = ce[i]
        # reaction arrows (longest first)
        matched = None
        for arrow in sorted(_CE_ARROWS, key=len, reverse=True):
            if ce.startswith(arrow, i):
                matched = arrow
                break
        if matched:
            out.append(("arrow", _CE_ARROWS[matched], None, None))
            i += len(matched)
            continue
        # state symbols (aq), (s), (g), (l) — rendered as subscript text
        if ch == "(":
            j = ce.find(")", i)
            if j > i:
                inner = ce[i + 1:j].strip()
                if inner in _CE_STATES:
                    out.append(("state", inner, None, None))
                    i = j + 1
                    continue
        # charges: +/-, 2+, 3-, etc. → superscript
        if ch in "+-" :
            k = i
            while k < n and ce[k] in "+-":
                k += 1
            charge = ce[i:k]
            out.append(("charge", charge, None, None))
            i = k
            continue
        if ch.isdigit() and i + 1 < n and ce[i + 1] in "+-":
            k = i
            while k < n and (ce[k].isdigit() or ce[k] in "+-"):
                k += 1
            out.append(("charge", ce[i:k], None, None))
            i = k
            continue
        # stoichiometric coefficient (leading number) → normal text
        if ch.isdigit():
            k = i
            while k < n and ce[k].isdigit():
                k += 1
            out.append(("text", ce[i:k], None, None))
            i = k
            continue
        # element symbol with following digits → text + auto subscript
        if ch.isalpha():
            k = i
            while k < n and ce[k].isalpha():
                k += 1
            sym = ce[i:k]
            i = k
            # digits right after element → subscript
            if i < n and ce[i].isdigit():
                k = i
                while k < n and ce[k].isdigit():
                    k += 1
                out.append(("text", sym, ce[i:k], None))
                i = k
            else:
                out.append(("text", sym, None, None))
            continue
        # whitespace → skip (but keep as separator)
        if ch in " \t":
            i += 1
            continue
        # single char (brackets, dots, etc.)
        out.append(("text", ch, None, None))
        i += 1
    return out


def _ce_to_omml(ce):
    """Convert mhchem-style \\ce{...} content to OMML XML.

    Charges and state labels must BIND to the element that precedes them
    (e.g. A- → sSup(base=A, sup=-)). An empty base floats the modifier
    detached — the bug reported in display equations.
    """
    parts = []
    for kind, val, sub, sup in _ce_tokenize(ce):
        if kind == "arrow":
            parts.append(_r(val))
        elif kind == "state":
            base = parts.pop() if parts else ""
            parts.append(_wrap(_wrap(base, "e") + _wrap(_r(val), "sub"), "sSub"))
        elif kind == "charge":
            base = parts.pop() if parts else ""
            parts.append(_wrap(_wrap(base, "e") + _wrap(_r(val), "sup"), "sSup"))
        else:  # text with optional auto-subscript
            if sub:
                parts.append(_wrap(_wrap(_r(val), "e") + _wrap(_r(sub), "sub"), "sSub"))
            else:
                parts.append(_r(val))
    return "".join(parts)


def latex_to_omml(latex):
    """Convert a LaTeX string to OMML XML (without the m:oMath wrapper).

    Supports mhchem-style \\ce{...} for chemical equations in addition to
    standard math (sub/sup, \\frac, \\sqrt, \\text{}, symbols, Greek).
    """
    return _latex_to_omml_math(latex)


def _latex_to_omml_math(latex):
    latex = latex.strip().strip("$")
    pos = 0
    n = len(latex)
    out = []

    def peek():
        return latex[pos] if pos < n else ""

    def eat_command():
        nonlocal pos
        # letters command: \\frac, \\text...
        m = re.match(r"\\([a-zA-Z]+)", latex[pos:])
        if m:
            pos += m.end()
            return m.group(1)
        # single non-letter: \\, \\; \\: \\  (thin/medium spaces, escaped char)
        if pos < n and latex[pos] == "\\":
            nxt = latex[pos + 1] if pos + 1 < n else ""
            if nxt and not nxt.isalpha() and nxt not in "{}":
                pos += 2
                return nxt
        return None

    def parse_group(stop_chars="}"):
        """parse until stop char or end; returns (xml, stopped_at_char)"""
        nonlocal pos
        parts = []
        while pos < n:
            ch = latex[pos]
            if ch in stop_chars:
                return "".join(parts), ch
            if ch == " ":
                pos += 1
                continue
            if ch == "\\":
                cmd = eat_command()
                if cmd is None:
                    # escaped literal char
                    parts.append(_r(latex[pos]))
                    pos += 1
                    continue
                sym = _SYM.get("\\" + cmd)
                if sym:
                    parts.append(_r(sym))
                    continue
                greek = _GREEK.get("\\" + cmd)
                if greek:
                    parts.append(_r(greek))
                    continue
                if len(cmd) == 1 and not cmd.isalpha():
                    # escaped punctuation like \, \; \: — render as literal char
                    parts.append(_r(cmd))
                    continue
                if cmd == "text":
                    # \text{...} upright text — txt is already OMML XML
                    while pos < n and latex[pos] in " \t":
                        pos += 1
                    if pos < n and latex[pos] == "{":
                        txt, _ = parse_group()
                        pos += 1
                        parts.append(txt)
                        continue
                if cmd == "mathrm":
                    # \mathrm{...} upright text (same as \text) — append raw XML
                    while pos < n and latex[pos] in " \t":
                        pos += 1
                    if pos < n and latex[pos] == "{":
                        txt, _ = parse_group()
                        pos += 1
                        parts.append(txt)
                        continue
                if cmd in ("bf", "mathit", "mathbf"):
                    # bold/italic text — render inner content as-is
                    while pos < n and latex[pos] in " \t":
                        pos += 1
                    if pos < n and latex[pos] == "{":
                        txt, _ = parse_group()
                        pos += 1
                        parts.append(_r(txt))
                        continue
                if cmd in ("frac", "dfrac", "tfrac"):
                    # \frac{a}{b}
                    # skip spaces and consume two groups
                    while pos < n and latex[pos] in " \t":
                        pos += 1
                    if pos < n and latex[pos] == "{":
                        num, _ = parse_group()
                        pos += 1  # consume }
                    else:
                        num, _ = parse_single()
                    while pos < n and latex[pos] in " \t":
                        pos += 1
                    if pos < n and latex[pos] == "{":
                        den, _ = parse_group()
                        pos += 1
                    else:
                        den, _ = parse_single()
                    parts.append(_wrap(_wrap(num, "num") + _wrap(den, "den"), "f"))
                    continue
                if cmd == "sqrt":
                    while pos < n and latex[pos] in " \t":
                        pos += 1
                    if pos < n and latex[pos] == "{":
                        inner, _ = parse_group()
                        pos += 1
                    else:
                        inner, _ = parse_single()
                    parts.append(_wrap(inner, "rad", '><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/>'.replace("></m:radPr><m:deg/>", "></m:radPr><m:deg></m:deg>") + ""))
                    continue
                if cmd == "ce":
                    # mhchem-style chemical equation → OMML directly
                    while pos < n and latex[pos] in " \t":
                        pos += 1
                    if pos < n and latex[pos] == "{":
                        raw = parse_raw_braces()
                        parts.append(_ce_to_omml(raw))
                    continue
                if cmd == "text":
                    while pos < n and latex[pos] in " \t":
                        pos += 1
                    if pos < n and latex[pos] == "{":
                        txt = parse_raw_braces()
                        parts.append('<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t xml:space="preserve">%s</m:t></m:r>' % _esc(txt))
                    continue
                if cmd in ("left", "right"):
                    # attach bracket char to next item
                    if pos < n and latex[pos] in "([|":
                        parts.append(_r(latex[pos]))
                        pos += 1
                    continue
                if "\\" + cmd in _MATH_FUNCS:
                    # function name run (upright)
                    parts.append('<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>%s</m:t></m:r>' % cmd)
                    continue
                # unknown command — emit literally without backslash
                parts.append(_r(cmd))
                continue
            if ch == "_":
                pos += 1
                sub, _ = parse_group() if peek() == "{" else parse_single()
                if pos < n and latex[pos] == "}":
                    pos += 1
                # check if sup follows (sub+sup combined)
                if pos < n and latex[pos] == "^":
                    pos += 1
                    sup, _ = parse_group() if peek() == "{" else parse_single()
                    if pos < n and latex[pos] == "}":
                        pos += 1
                    base = take_base(parts)
                    parts.append(_wrap(_wrap(base, "e") + _wrap(sub, "sub") + _wrap(sup, "sup"), "sSubSup"))
                else:
                    base = take_base(parts)
                    parts.append(_wrap(_wrap(base, "e") + _wrap(sub, "sub"), "sSub"))
                continue
            if ch == "^":
                pos += 1
                sup, _ = parse_group() if peek() == "{" else parse_single()
                if pos < n and latex[pos] == "}":
                    pos += 1
                base = take_base(parts)
                parts.append(_wrap(_wrap(base, "e") + _wrap(sup, "sup"), "sSup"))
                continue
            if ch == "{" or ch == "}":
                pos += 1
                continue
            if ch in _OPEN:
                # check it's a real open bracket (paired) — render as delimiter
                parts.append(_r(ch))
                pos += 1
                continue
            if ch in _CLOSE:
                parts.append(_r(ch))
                pos += 1
                continue
            # plain char: consume run of letters/digits/symbols
            m = re.match(r"[A-Za-z0-9\.\,\-−\u00B0\u2212%\[\]\(\)'']+", latex[pos:])
            if m:
                parts.append(_r(m.group(0)))
                pos += m.end()
            else:
                parts.append(_r(ch))
                pos += 1
        return "".join(parts), None

    def take_base(parts):
        """Pop the last parsed element to use as the BASE of a sub/sup.

        In OMML, sSub/sSup must bind to a base (m:e). An empty base makes
        the modifier float detached (the bug the user reported in display
        equations). LaTeX semantics: ^ and _ attach to whatever precedes
        them, so we pop the last element from parts.
        """
        if parts:
            return parts.pop()
        return ""

    def parse_single():
        """consume a single token (for _ or ^ without braces) — advances pos"""
        nonlocal pos
        if pos >= n:
            return "", None
        if latex[pos] == "{":
            return parse_group()
        if latex[pos] == "\\":
            cmd = eat_command()
            sym = _SYM.get("\\" + cmd)
            if sym:
                return _r(sym), None
            greek = _GREEK.get("\\" + cmd)
            if greek:
                return _r(greek), None
            if cmd in ("alpha", "beta", "gamma", "delta", "theta", "pi", "mu", "nu", "omega", "lambda", "sigma", "phi"):
                return _r(_GREEK.get("\\" + cmd, cmd)), None
            return _r(cmd), None
        ch = latex[pos]
        pos += 1
        return _r(ch), None

    def parse_raw_braces():
        """capture raw text inside {...} (no math parsing) — for \\text{}"""
        nonlocal pos
        if pos < n and latex[pos] == "{":
            pos += 1
        start = pos
        depth = 1
        while pos < n and depth:
            if latex[pos] == "{":
                depth += 1
            elif latex[pos] == "}":
                depth -= 1
            if depth:
                pos += 1
        txt = latex[start:pos]
        if pos < n:
            pos += 1  # consume }
        return txt

    xml, _ = parse_group(stop_chars="")
    return xml


def omath_paragraph_xml(latex, size_pt=11):
    """Full paragraph XML with a centered display equation."""
    body = latex_to_omml(latex)
    return (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        '<w:pPr><w:jc w:val="center"/></w:pPr>'
        '<m:oMath><m:r><m:rPr><m:sz m:val="%d"/></m:rPr></m:r>%s</m:oMath>'
        "</w:p>" % (int(size_pt * 2), body)
    )


if __name__ == "__main__":
    tests = [
        "pH = pK_a + \\log\\left(\\frac{[A^-]}{[HA]}\\right)",
        "K_a = \\frac{[H^+][A^-]}{[HA]}",
        "K_a \\cdot K_b = K_w = 1.0 \\times 10^{-14}",
        "pH = -\\log[H^+]",
        "pH \\approx \\frac{pK_{a1} + pK_{a2}}{2}",
        "n = M \\times V",
    ]
    for t in tests:
        print("OK:", t)
        print("   ", latex_to_omml(t)[:120], "...")
    print("ALL PARSE OK")
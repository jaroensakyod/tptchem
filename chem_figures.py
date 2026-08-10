#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ChemNest figure generator — original, self-rendered chemistry figures.

Every figure is drawn programmatically (matplotlib) so we OWN the artwork:
no copyrighted textbook images. Matches US textbook conventions (OpenStax 2e).

Figures:
  ph_scale           — pH 0-14 bar with colors + example substances
  titration_curve    — strong/weak acid + strong base curve w/ equivalence & half-equiv
  distribution       — species fraction vs pH for a diprotic acid (H2A/HA-/A2-)
  buffer_action      — how a buffer absorbs added H+/OH- (conceptual)
  conjugate_pairs    — acid/base/conjugate pair arrows

Usage: python chem_figures.py [figure_name ...]   (default: all)
Output: figures/<name>.png  (300 dpi, sized for worksheet insertion)
"""
import os, sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

INDIGO = "#4F46E5"
PURPLE = "#7C3AED"
RED = "#DC2626"
ORANGE = "#EA580C"
GREEN = "#16A34A"
BLUE = "#2563EB"
SLATE = "#334155"
GRAY = "#94A3B8"
CREAM = "#F8FAFC"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": SLATE,
    "axes.linewidth": 1.0,
    "figure.facecolor": "white",
})


def _save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("figure ->", path)


# ---------------------------------------------------------------- pH scale
def ph_scale():
    fig, ax = plt.subplots(figsize=(8.6, 3.1))
    # colored bar 0-14 (continuous hue: red → green → blue)
    colors = ["#EF4444", "#F97316", "#F59E0B", "#FACC15", "#A3E635",
              "#4ADE80", "#22C55E", "#10B981", "#2DD4BF", "#22D3EE",
              "#38BDF8", "#60A5FA", "#818CF8", "#A78BFA", "#C084FC"]
    for i in range(14):
        ax.barh(0, 1, left=i, height=0.85, color=colors[i], edgecolor="white", linewidth=1.5)
    # zone labels with bbox (no overlap with bar)
    ax.text(3.5, 0.62, "ACIDIC", ha="center", fontsize=10.5, fontweight="bold", color="#7F1D1D")
    ax.text(7.0, 0.62, "NEUTRAL", ha="center", fontsize=10.5, fontweight="bold", color="#14532D")
    ax.text(11.5, 0.62, "BASIC", ha="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")
    ax.set_xticks(range(0, 15))
    ax.set_yticks([])
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-1.9, 1.05)
    ax.spines[["left", "right", "top"]].set_visible(False)
    # examples in TWO staggered rows with leader dots (anti-overlap)
    row1 = [(1.0, "stomach acid", "#B91C1C"), (3.5, "lemon juice", "#C2410C"),
            (5.5, "coffee", "#92400E"), (7.0, "pure water", "#166534"),
            (9.5, "baking soda", "#1D4ED8"), (12.0, "ammonia", "#4338CA")]
    row2 = [(2.2, "vinegar", "#B91C1C"), (4.5, "tomato", "#C2410C"),
            (10.5, "soap", "#4338CA"), (13.2, "drain cleaner", "#5B21B6")]
    for x, label, c in row1:
        ax.plot(x, -0.55, "o", color=c, markersize=5.5)
        ax.annotate(label, xy=(x, -0.55), xytext=(x, -1.05), ha="center",
                    fontsize=7.2, color=SLATE,
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))
    for x, label, c in row2:
        ax.plot(x, -0.55, "o", color=c, markersize=5.5)
        ax.annotate(label, xy=(x, -0.55), xytext=(x, -1.65), ha="center",
                    fontsize=7.2, color=SLATE,
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))
    ax.text(7.0, 0.95, "Each step of 1 pH unit = 10× change in [H⁺]",
            ha="center", va="bottom", fontsize=8, color=GRAY, style="italic")
    _save(fig, "ph-scale.png")


# ---------------------------------------------------------------- titration curve
def _titration_curve_data(weak=True, pka=4.76, Ca=0.10, V_a=25.0, Cb=0.10):
    """Compute pH vs volume of strong base added (mL) for acid titration."""
    V = np.linspace(0, 50, 600)
    n_a = Ca * V_a  # mmol acid
    pH = np.zeros_like(V)
    for i, v in enumerate(V):
        n_b = Cb * v  # mmol base added
        if not weak:  # strong acid
            if n_b < n_a:
                pH[i] = -np.log10((n_a - n_b) / (V_a + v))
            elif n_b == n_a:
                pH[i] = 7.0
            else:
                pH[i] = 14 + np.log10((n_b - n_a) / (V_a + v))
        else:
            if v == 0:
                # weak acid alone
                x = np.sqrt(pka * Ca) if False else 10 ** -pka
                # Ka = x^2/(Ca-x)
                Ka = 10 ** -pka
                x = (-Ka + np.sqrt(Ka * Ka + 4 * Ka * Ca)) / 2
                pH[i] = -np.log10(x)
            elif n_b < n_a * 0.999:
                # buffer region: exact equilibrium with A- from added base + self-ionization
                # Ka = x(x + A0)/(HA0 - x)  →  x^2 + (A0+Ka)x - Ka*HA0 = 0
                Ka = 10 ** -pka
                Vt = V_a + v
                HA0 = (n_a - n_b) / Vt
                A0 = n_b / Vt
                x = (-(A0 + Ka) + np.sqrt((A0 + Ka) ** 2 + 4 * Ka * HA0)) / 2
                pH[i] = -np.log10(max(x, 1e-14))
            elif abs(n_b - n_a) <= 1e-6:
                # equivalence: conjugate base hydrolysis
                Kb = 1e-14 / (10 ** -pka)
                C = n_a / (V_a + v)
                x = (-Kb + np.sqrt(Kb * Kb + 4 * Kb * C)) / 2
                pH[i] = 14 + np.log10(x)
            else:
                # excess strong base
                pH[i] = 14 + np.log10((n_b - n_a) / (V_a + v))
    # guard
    pH = np.clip(pH, 0, 14)
    return V, pH


def titration_curve():
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    # weak acid + strong base
    V, pH = _titration_curve_data(weak=True, pka=4.76, Ca=0.10, V_a=25.0, Cb=0.10)
    ax.plot(V, pH, color=INDIGO, lw=2.2, label="0.10 M CH₃COOH + 0.10 M NaOH")
    # strong acid + strong base
    V2, pH2 = _titration_curve_data(weak=False, Ca=0.10, V_a=25.0, Cb=0.10)
    ax.plot(V2, pH2, color=GRAY, lw=1.6, ls="--", label="0.10 M HCl + 0.10 M NaOH")
    # half-equivalence
    ax.plot(12.5, 4.76, "o", color=ORANGE, markersize=8, zorder=5)
    ax.annotate("half-equivalence\npH = pKₐ = 4.76", xy=(12.5, 4.76), xytext=(2, 2.0),
                fontsize=8.5, color=ORANGE,
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
    # equivalence
    ax.plot(25.0, 8.7, "o", color=RED, markersize=8, zorder=5)
    ax.annotate("equivalence point\n(conjugate base → pH > 7)", xy=(25.0, 8.7),
                xytext=(30, 9.6), fontsize=8.5, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    # buffer region bracket
    ax.axvspan(2.5, 12.5, color=INDIGO, alpha=0.07)
    ax.text(7.5, 1.2, "buffer region", fontsize=8.5, color=INDIGO, ha="center", style="italic")
    # indicator range example
    ax.axhspan(8.3, 10.0, xmin=0.42, xmax=0.75, color=GREEN, alpha=0.15)
    ax.text(33.5, 9.2, "phenolphthalein\nrange (8.3-10)", fontsize=7.5, color=GREEN)
    ax.set_xlabel("Volume of 0.10 M NaOH added (mL)")
    ax.set_ylabel("pH")
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 14)
    ax.set_xticks([0, 12.5, 25, 37.5, 50])
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, "titration-curve.png")


# ---------------------------------------------------------------- distribution diagram
def distribution():
    pka1, pka2 = 2.15, 7.20  # H3PO4 first two
    pH = np.linspace(0, 13, 500)
    h = 10 ** -pH
    Ka1, Ka2 = 10 ** -pka1, 10 ** -pka2
    # fractions for H2A / HA- / A2-
    denom = h * h + Ka1 * h + Ka1 * Ka2
    f_h2a = h * h / denom
    f_ha = Ka1 * h / denom
    f_a2 = Ka1 * Ka2 / denom

    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.plot(pH, f_h2a, color=RED, lw=2, label="H₂PO₄⁻" if False else "H₃PO₄" if False else "H₂A")
    ax.plot(pH, f_ha, color=INDIGO, lw=2, label="HA⁻")
    ax.plot(pH, f_a2, color=GREEN, lw=2, label="A²⁻")
    # crossover points
    ax.plot(pka1, 0.5, "o", color=SLATE, markersize=6)
    ax.plot(pka2, 0.5, "o", color=SLATE, markersize=6)
    ax.annotate("pH = pKₐ₁", xy=(pka1, 0.5), xytext=(pka1 - 1.2, 0.62), fontsize=8, color=SLATE)
    ax.annotate("pH = pKₐ₂", xy=(pka2, 0.5), xytext=(pka2 + 0.15, 0.62), fontsize=8, color=SLATE)
    ax.axvline(pka1, color=GRAY, ls=":", lw=1)
    ax.axvline(pka2, color=GRAY, ls=":", lw=1)
    ax.set_xlabel("pH")
    ax.set_ylabel("Fraction of species")
    ax.set_ylim(0, 1.05)
    ax.set_xlim(0, 13)
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(fontsize=9, loc="center right")
    _save(fig, "distribution.png")


# ---------------------------------------------------------------- buffer action
def buffer_action():
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    # HA tank
    ax.add_patch(plt.Rectangle((0.6, 1.6), 3.4, 2.0, fc="#EEF2FF", ec=INDIGO, lw=1.6))
    ax.text(2.3, 3.3, "Buffer: HA + A⁻", ha="center", fontsize=10.5, fontweight="bold", color=INDIGO)
    ax.text(2.3, 2.7, "HA  +  A⁻", ha="center", fontsize=12, color=SLATE)
    ax.text(2.3, 2.15, "many moles", ha="center", fontsize=8.5, color=GRAY)
    # added H+
    ax.add_patch(FancyArrowPatch((4.8, 3.6), (4.2, 3.05), arrowstyle="-|>", mutation_scale=16, color=RED, lw=2))
    ax.text(5.5, 3.75, "add H⁺ (acid)", fontsize=9.5, color=RED, fontweight="bold")
    # added OH-
    ax.add_patch(FancyArrowPatch((4.8, 2.1), (4.2, 2.45), arrowstyle="-|>", mutation_scale=16, color=BLUE, lw=2))
    ax.text(5.5, 1.55, "add OH⁻ (base)", fontsize=9.5, color=BLUE, fontweight="bold")
    # reactions below the tank (no overlap)
    ax.text(2.3, 1.15, "H⁺ + A⁻ → HA", ha="center", fontsize=9.5, color=RED)
    ax.text(2.3, 0.65, "OH⁻ + HA → A⁻ + H₂O", ha="center", fontsize=9.5, color=BLUE)
    ax.text(2.3, 0.2, "→ pH barely changes", ha="center", fontsize=8.5, color=GREEN, style="italic")
    # result badge top-right (clear zone)
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((6.9, 2.6), 2.7, 1.3, boxstyle="round,pad=0.08",
                                fc="#F0FDF4", ec=GREEN, lw=1.6))
    ax.text(8.25, 3.5, "small ΔpH", ha="center", fontsize=11, color=GREEN, fontweight="bold")
    ax.text(8.25, 2.95, "= buffer works!", ha="center", fontsize=9, color=GREEN)
    _save(fig, "buffer-action.png")


# ---------------------------------------------------------------- conjugate pairs
def conjugate_pairs():
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    # HA -> A-
    ax.add_patch(plt.Rectangle((0.8, 2.3), 2.6, 1.2, fc="#FEE2E2", ec=RED, lw=1.6))
    ax.text(2.1, 2.9, "HA\n(acid)", ha="center", va="center", fontsize=11, color="#991B1B")
    ax.add_patch(FancyArrowPatch((3.6, 2.9), (5.4, 2.9), arrowstyle="-|>", mutation_scale=20, color=SLATE, lw=2))
    ax.text(4.5, 3.25, "− H⁺", ha="center", fontsize=9, color=RED)
    ax.text(4.5, 2.55, "+ H⁺", ha="center", fontsize=9, color=BLUE)
    ax.add_patch(plt.Rectangle((5.6, 2.3), 2.6, 1.2, fc="#DBEAFE", ec=BLUE, lw=1.6))
    ax.text(6.9, 2.9, "A⁻\n(conjugate base)", ha="center", va="center", fontsize=10, color="#1E40AF")
    # B -> BH+
    ax.add_patch(plt.Rectangle((0.8, 0.4), 2.6, 1.2, fc="#DBEAFE", ec=BLUE, lw=1.6))
    ax.text(2.1, 1.0, "B\n(base)", ha="center", va="center", fontsize=11, color="#1E40AF")
    ax.add_patch(FancyArrowPatch((3.6, 1.0), (5.4, 1.0), arrowstyle="-|>", mutation_scale=20, color=SLATE, lw=2))
    ax.text(4.5, 1.35, "+ H⁺", ha="center", fontsize=9, color=BLUE)
    ax.text(4.5, 0.65, "− H⁺", ha="center", fontsize=9, color=RED)
    ax.add_patch(plt.Rectangle((5.6, 0.4), 2.6, 1.2, fc="#FEE2E2", ec=RED, lw=1.6))
    ax.text(6.9, 1.0, "BH⁺\n(conjugate acid)", ha="center", va="center", fontsize=10, color="#991B1B")
    ax.text(8.6, 2.9, "conjugate pair:\ndiffer by 1 H⁺", fontsize=8.5, color=GRAY, ha="left")
    _save(fig, "conjugate-pairs.png")


# ---------------------------------------------------------------- RDKit molecules
def rdkit_molecules(names=None):
    """Draw molecules with RDKit (2D depiction, white bg, 300 dpi).

    Uses AddHs so small molecules (NH3, H2O, HF, NH4+) show explicit H bonds
    instead of bare element labels. Output: figures/mol-<slug>.png
    Names: dict of slug -> SMILES (default = acid-base set).
    """
    try:
        from rdkit import Chem
        from rdkit.Chem import Draw, AllChem
    except ImportError:
        print("RDKit not installed — skip molecules")
        return
    default = {
        "acetic-acid": "CC(=O)O", "ammonia": "N", "phosphoric-acid": "OP(=O)(O)O",
        "carbonic-acid": "OC(=O)O", "hf": "F", "water": "O",
        "ammonium": "[NH4+]", "bicarbonate": "O=C(O)[O-]",
        "hydrochloric-acid": "Cl", "nitric-acid": "O[N+](=O)[O-]",
        "sulfuric-acid": "OS(=O)(=O)O", "sodium-hydroxide": "[Na+].[OH-]",
        "conjugate-base-acetate": "CC(=O)[O-]", "methylamine": "CN",
    }
    d = names or default
    for slug, smi in d.items():
        try:
            m = Chem.MolFromSmiles(smi)
            if m is None:
                print("FAIL parse:", slug); continue
            m = Chem.AddHs(m)
            AllChem.Compute2DCoords(m)
            img = Draw.MolToImage(m, size=(480, 340))
            path = os.path.join(OUT, f"mol-{slug}.png")
            img.save(path, dpi=(300, 300))
            print("molecule ->", path)
        except Exception as e:
            print(f"FAIL {slug}: {e}")


# ---------------------------------------------------------------- lab equipment (demo: 8 items)
def lab_equipment():
    """Draw common lab glassware & safety items as flat icons (matplotlib shapes).

    Flat-icon style matches what US teachers actually use on lab-safety sheets
    (per competitor teardown) — clean, printable at 300 dpi, fully original.
    Demo set: 8 items in a 4x2 grid. Extend items dict for more.
    """
    from matplotlib.patches import Polygon, Circle, FancyBboxPatch, Wedge
    fig, axes = plt.subplots(2, 4, figsize=(11, 5.2))
    for ax in axes.flat:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10)
        ax.set_aspect("equal"); ax.axis("off")

    # each item: (draw_fn(ax), label)
    def beaker(ax):
        ax.add_patch(Polygon([[2, 2.2], [8, 2.2], [7.4, 8], [2.6, 8]], closed=True,
                             fc="#DBEAFE", ec="#1D4ED8", lw=2))
        ax.add_patch(Polygon([[2.6, 8], [7.4, 8], [7.6, 8.7], [2.4, 8.7]], closed=True,
                             fc="#BFDBFE", ec="#1D4ED8", lw=1.5))
        ax.plot([3.2, 4.6], [5.2, 5.2], color="#60A5FA", lw=2.5)
        ax.plot([3.2, 4.6], [4.0, 4.0], color="#60A5FA", lw=2.5)

    def erlenmeyer(ax):
        ax.add_patch(Polygon([[4.5, 2.2], [5.5, 2.2], [6.8, 7.4], [6.2, 7.4]], closed=True,
                             fc="#DBEAFE", ec="#1D4ED8", lw=2))
        ax.add_patch(Polygon([[3.6, 2.2], [6.4, 2.2], [5.6, 2.8], [4.4, 2.8]], closed=True,
                             fc="#BFDBFE", ec="#1D4ED8", lw=1.5))
        ax.plot([6.3, 6.3], [7.4, 8.6], color="#1D4ED8", lw=2)
        ax.plot([4.0, 6.0], [3.6, 3.6], color="#60A5FA", lw=2.5)

    def graduated_cylinder(ax):
        ax.add_patch(Polygon([[3.6, 2.2], [6.4, 2.2], [6.1, 8.2], [3.9, 8.2]], closed=True,
                             fc="#DBEAFE", ec="#1D4ED8", lw=2))
        ax.add_patch(Polygon([[3.9, 8.2], [6.1, 8.2], [6.3, 8.9], [3.7, 8.9]], closed=True,
                             fc="#BFDBFE", ec="#1D4ED8", lw=1.5))
        for y in (3.4, 4.6, 5.8):
            ax.plot([4.3, 5.7], [y, y], color="#60A5FA", lw=1.8)

    def bunsen_burner(ax):
        ax.add_patch(Polygon([[4.2, 2.2], [5.8, 2.2], [6.3, 5.0], [3.7, 5.0]], closed=True,
                             fc="#E2E8F0", ec="#475569", lw=2))
        ax.add_patch(Polygon([[3.4, 5.0], [6.6, 5.0], [6.9, 6.0], [3.1, 6.0]], closed=True,
                             fc="#CBD5E1", ec="#475569", lw=2))
        ax.add_patch(Polygon([[4.4, 6.0], [5.6, 6.0], [5.9, 7.6], [4.1, 7.6]], closed=True,
                             fc="#FED7AA", ec="#EA580C", lw=1.8))
        # flame
        ax.add_patch(Polygon([[4.7, 7.6], [5.3, 7.6], [5.0, 9.2]], closed=True,
                             fc="#FDE68A", ec="#F59E0B", lw=1.5))
        ax.plot([3.1, 6.9], [5.5, 5.5], color="#94A3B8", lw=2)

    def goggles(ax):
        ax.add_patch(FancyBboxPatch((2.4, 4.6), 2.2, 1.6, boxstyle="round,pad=0.06",
                                    fc="#E0F2FE", ec="#0369A1", lw=2))
        ax.add_patch(FancyBboxPatch((5.4, 4.6), 2.2, 1.6, boxstyle="round,pad=0.06",
                                    fc="#E0F2FE", ec="#0369A1", lw=2))
        ax.plot([4.6, 5.4], [5.4, 5.4], color="#0369A1", lw=2.5)
        ax.plot([2.4, 1.8], [5.0, 3.4], color="#0369A1", lw=2)
        ax.plot([7.6, 8.2], [5.0, 3.4], color="#0369A1", lw=2)
        ax.plot([1.8, 8.2], [3.4, 3.4], color="#0369A1", lw=2)

    def test_tube(ax):
        ax.add_patch(Polygon([[4.3, 2.2], [5.7, 2.2], [5.7, 8.0], [4.3, 8.0]], closed=True,
                             fc="#FEF9C3", ec="#A16207", lw=2))
        ax.add_patch(Wedge((5.0, 2.2), 0.7, 0, 180, fc="#FEF9C3", ec="#A16207", lw=2))
        ax.add_patch(Polygon([[4.3, 8.0], [5.7, 8.0], [5.7, 8.7], [4.3, 8.7]], closed=True,
                             fc="#FDE68A", ec="#A16207", lw=1.5))

    def fire_extinguisher(ax):
        ax.add_patch(Polygon([[4.1, 2.2], [5.9, 2.2], [5.6, 7.6], [4.4, 7.6]], closed=True,
                             fc="#FEE2E2", ec="#B91C1C", lw=2))
        ax.add_patch(Polygon([[4.0, 7.6], [6.0, 7.6], [5.6, 8.3], [4.4, 8.3]], closed=True,
                             fc="#FECACA", ec="#B91C1C", lw=1.8))
        ax.plot([5.0, 5.0], [8.3, 9.2], color="#B91C1C", lw=2.5)
        ax.text(5.0, 3.8, "ABC", ha="center", va="center", fontsize=7, color="#B91C1C", fontweight="bold")

    def eyewash(ax):
        ax.add_patch(Wedge((5.0, 5.4), 2.2, 180, 360, fc="#E0F2FE", ec="#0369A1", lw=2))
        ax.add_patch(Polygon([[3.2, 5.4], [6.8, 5.4], [5.6, 2.4], [4.4, 2.4]], closed=True,
                             fc="#BAE6FD", ec="#0369A1", lw=2))
        ax.plot([3.4, 2.6], [7.2, 8.0], color="#0369A1", lw=2)
        ax.plot([6.6, 7.4], [7.2, 8.0], color="#0369A1", lw=2)
        for dx in (-0.8, 0.8):
            ax.plot([5.0 + dx, 5.0 + dx], [6.2, 7.6], color="#0EA5E9", lw=2)

    items = [
        (beaker, "Beaker"), (erlenmeyer, "Erlenmeyer flask"), (graduated_cylinder, "Graduated cylinder"),
        (bunsen_burner, "Bunsen burner"), (goggles, "Safety goggles"), (test_tube, "Test tube"),
        (fire_extinguisher, "Fire extinguisher"), (eyewash, "Eyewash station"),
    ]
    for ax, (fn, label) in zip(axes.flat, items):
        fn(ax)
        ax.text(5.0, 1.2, label, ha="center", va="bottom", fontsize=9.5, color=SLATE, fontweight="bold")
    fig.suptitle("Common Lab Equipment", fontsize=13, color=SLATE, fontweight="bold", y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _save(fig, "lab-equipment.png")

FIGURES = {
    "ph_scale": ph_scale,
    "titration_curve": titration_curve,
    "distribution": distribution,
    "buffer_action": buffer_action,
    "conjugate_pairs": conjugate_pairs,
    "molecules": rdkit_molecules,
    "lab_equipment": lab_equipment,
}


def main():
    names = sys.argv[1:] or list(FIGURES.keys())
    for n in names:
        if n in FIGURES:
            FIGURES[n]()
        else:
            print(f"skip unknown figure: {n}")


if __name__ == "__main__":
    main()

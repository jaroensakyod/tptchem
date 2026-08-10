# CurioNest Asset Attribution

This file is the compliance source of truth for third-party fonts and visual assets.
The machine-readable inventory is `assets-manifest.json`.

## Current status

The repository records the intended licenses, but provenance is not yet publish-clear:

- Poppins, Nunito, and Caveat are recorded as Google Fonts under OFL 1.1. A copy of
  the OFL license must be committed before release.
- The GHS/UNECE SVG set used by the Chemistry Foundations pilot is verified as CC0,
  with exact Bioicons repository URLs and a local license copy.
- The pilot equipment set is verified per file: Servier assets are CC BY 3.0 and
  OpenClipart assets are CC0. Exact URLs, creators, and local license copies are in
  `assets-manifest.json`.
- Composed PNG grids must retain the provenance of every SVG used to create them.

Until every `verification_status` in `assets-manifest.json` is `verified`, QA reports
an attribution warning and the product should not be marked `certified`.

## Rules for new assets

Asset routing is governed by `product-quality-standard.md` section `G3-V`.

1. Add the asset to `assets-manifest.json` before using it in a product.
2. Record an exact source URL, creator when available, license identifier, and any
   required attribution text.
3. Store a local license copy under `licenses/` when the license permits it.
4. For generated or composed images, record all source assets used in the derivation.
5. Do not infer a license from a filename or website category alone.
6. After visual QA, remove unused experiments and orphan derivatives while retaining
   the licensed source and every derivative referenced by a builder or final product.

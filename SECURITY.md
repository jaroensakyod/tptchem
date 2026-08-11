# Security Notes

## PptxGenJS transitive image parser

`npm audit` currently reports a high-severity denial-of-service advisory in the
`image-size` version required by PptxGenJS 4.0.1. The affected behavior parses
malformed ICNS, JXL, or HEIF images and can loop indefinitely.

Project mitigation until PptxGenJS ships a compatible fixed dependency:

- Builders accept only repository-controlled PNG/SVG assets listed in
  `assets-manifest.json`.
- Do not run the PPT builder against untrusted JSON or user-uploaded images.
- Do not add ICNS, JXL, or HEIF assets to this repository.
- Re-run `npm audit` whenever `pptxgenjs` or `image-size` is updated.

Do not run `npm audit fix --force`; the suggested downgrade changes the public API
and would invalidate the current builder without a migration and regression test.

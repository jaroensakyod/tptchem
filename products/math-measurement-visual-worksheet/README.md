# CurioNest Chemistry Measurement Visual Worksheet

**Status:** Automated package QA passed; human release gates pending - do not publish yet  
**Format:** US Letter, American English, U.S. Grades 8-10  
**Source model:** official U.S. chemistry/measurement references for content; ChemPride Unit 1 is an internal workflow benchmark only

## Upload-ready folder

Use `output/tpt-upload/`:

- `CurioNest_Measurement_Visual_Worksheet_TPT.zip` - main TPT product file
- `CurioNest_Measurement_Visual_Worksheet_Preview.pdf` - 3-page preview
- `cover.png` - 1200 x 1200 primary thumbnail
- `listing-02-inside.png` and `listing-03-teacher-ready.png` - additional listing images
- `TPT-LISTING-COPY.md` - fields to paste into TPT
- `TPT-UPLOAD-CHECKLIST.md` - upload and post-publish sequence

## Buyer files

`output/buyer-files/` contains the complete PDF, student-only PDF, answer-key PDF, editable DOCX, and separate rights/source page.

## Rebuild and QA

```powershell
python source/build_pdf.py
python source/build_docx.py
python source/package_release.py
python source/build_listing_assets.py
python source/qa_product.py
```

The automated QA report is `docs/QA-REPORT.md`. Rights and source details are in `docs/RIGHTS-AND-SOURCES.md`. Complete `docs/RELEASE-EVIDENCE.md` before changing the catalog status to `certified` or making the TPT listing active.

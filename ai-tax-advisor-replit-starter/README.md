
# AI Tax Advisor — Replit Starter (FastAPI)

A minimal starter you can import to Replit. It lets users upload last year's tax return PDF and returns example "opportunities" (recommendations) using simple text heuristics. This is a scaffold — replace the rules with real ones and hook up proper parsing/OCR later.

## Quick Start on Replit
1) On Replit, click **Create Repl → Import from GitHub** (or **Upload** a .zip) and select this project.  
2) In the **Shell**, run: `pip install -r app/requirements.txt` once (Replit may do this automatically).  
3) Set the **Run** command to:
```
uvicorn app.main:app --host 0.0.0.0 --port 3000
```
4) Press **Run**. Open the webview → you'll see the upload page.  

## Project Structure
```
app/
  main.py          # FastAPI app (upload, analyze, serve UI)
  parser.py        # very naive PDF text extractor + field finders
  rules.py         # example rule checks for recommendations
  requirements.txt # Python deps
  templates/index.html  # simple UI
  static/app.js    # client-side JS for uploads
.replit (optional)      # if you want to fix the run cmd
```

## Next Steps
- Swap heuristic parsing with robust table/line extraction (pdfplumber + templates).
- Add confidence scores, line citations, and advisor review UI.
- Persist uploads to S3 or Replit DB (for demo, in-memory is fine).
- Add authentication + basic RBAC for advisor/client split.

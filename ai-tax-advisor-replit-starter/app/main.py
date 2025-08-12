
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import tempfile, pdfplumber, os
from .parser import extract_text_glance, detect_forms_and_fields
from .rules import run_rules

app = FastAPI(title="AI Tax Advisor (MVP)")

BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Save to temp
    suffix = os.path.splitext(file.filename)[-1] or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Extract quick text
    text = extract_text_glance(tmp_path)
    forms, fields = detect_forms_and_fields(text)

    # Run naive rules to produce example recommendations
    recommendations = run_rules(forms=forms, fields=fields, raw_text=text)

    # Clean up temp file
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    return JSONResponse({
        "filename": file.filename,
        "forms_detected": sorted(list(forms)),
        "fields_found": fields,
        "recommendations": recommendations
    })

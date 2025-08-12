
import pdfplumber, re

def extract_text_glance(pdf_path: str, max_pages: int = 3) -> str:
    """
    Very naive text extraction: reads first up to 3 pages for a quick glance.
    """
    out = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages[:max_pages]):
                out.append(page.extract_text() or "")
    except Exception:
        # If pdfplumber fails, just return empty string
        return ""
    return "\n".join(out)

def detect_forms_and_fields(text: str):
    """
    Super-rough detection based on keywords. Replace with template-based parsing later.
    Returns (forms_set, fields_dict).
    """
    t = text.lower()

    # Forms presence by keyword
    form_keywords = {
        "1040": ["form 1040", "u.s. individual income tax return"],
        "schedule a": ["schedule a (form 1040)", "itemized deductions"],
        "schedule b": ["schedule b (form 1040)", "interest and ordinary dividends"],
        "schedule c": ["schedule c (form 1040)"],
        "schedule d": ["schedule d (form 1040)", "capital gains and losses"],
        "schedule e": ["schedule e (form 1040)"],
        "w-2": ["form w-2", "wage and tax statement"],
        "1099": ["form 1099", "1099-nec", "1099-misc", "1099-int", "1099-div", "1099-b"],
        "k-1": ["schedule k-1", "partner's share", "shareholder's share"],
        "1098": ["form 1098", "mortgage interest statement"],
        "5498": ["form 5498", "ira contribution information"],
        "8889": ["form 8889", "health savings account"],
        "8606": ["form 8606", "nondeductible iras"],
        "8995": ["form 8995", "qualified business income deduction"],
        "2441": ["form 2441", "child and dependent care expenses"],
        "8863": ["form 8863", "education credits"],
        "5695": ["form 5695", "residential energy credits"]
    }

    forms_detected = set()
    for form, kws in form_keywords.items():
        if any(kw in t for kw in kws):
            forms_detected.add(form)

    # Quick fields (extremely rough, regex based on common 1040 words)
    fields = {}

    # Adjusted Gross Income (AGI) hint
    agi_match = re.search(r"adjusted gross income.*?\$?([0-9,]+)", t, flags=re.I|re.S)
    if agi_match:
        fields["agi_guess"] = agi_match.group(1)

    # dependents hint
    if "dependents" in t:
        fields["dependents_section_present"] = True

    # mortgage interest hint
    if "mortgage interest" in t or "form 1098" in t:
        fields["mortgage_interest_hint"] = True

    # hsa hint
    if "health savings account" in t or "form 8889" in t:
        fields["hsa_hint"] = True

    # education credit hint
    if "form 8863" in t or "education credits" in t or "1098-t" in t:
        fields["education_hint"] = True

    return forms_detected, fields

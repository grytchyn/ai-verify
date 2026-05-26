import uuid
import logging
from fastapi import FastAPI, Form, Request, BackgroundTasks, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Submission
from .llm import call_ollama
from .search import duckduckgo_instant_answer
from .prompts import build_user_prompt, build_enhanced_prompt
from .utils import save_report
import os
import json
import markdown

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Compliance Consultant")
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content=content, media_type="text/html", headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })

@app.get("/submit-page", response_class=HTMLResponse)
async def submit_page():
    with open("static/submit.html", "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content=content, media_type="text/html", headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })

@app.get("/result-page", response_class=HTMLResponse)
async def result_page():
    with open("static/result.html", "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content=content, media_type="text/html", headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })

@app.post("/submit")
async def submit_full(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    # Company info
    company: str = Form(...),
    url: str = Form(""),
    email: str = Form(""),
    company_size: str = Form(""),
    sector: str = Form(""),
    employees: str = Form(""),
    annual_revenue: str = Form(""),
    hq_location: str = Form(""),
    description: str = Form(""),
    # AI system details
    ai_systems_count: str = Form(""),
    ai_system_names: str = Form(""),
    ai_purpose: str = Form(""),
    deployment_type: str = Form(""),
    data_sources: str = Form(""),
    decision_type: str = Form(""),
    risk_self_assessment: str = Form(""),
    # Technical
    model_types: str = Form(""),
    training_data_origin: str = Form(""),
    human_oversight: str = Form(""),
    explainability: str = Form(""),
    data_retention: str = Form(""),
    # Compliance
    has_documentation: str = Form(""),
    dpo_appointed: str = Form(""),
    gdpr_compliant: str = Form(""),
    existing_certifications: str = Form(""),
    previous_audits: str = Form(""),
    ce_marking: str = Form(""),
    # Risk checkboxes
    risk_biometrics: bool = Form(False),
    risk_critical_infra: bool = Form(False),
    risk_education: bool = Form(False),
    risk_employment: bool = Form(False),
    risk_credit: bool = Form(False),
    risk_law_enforcement: bool = Form(False),
    risk_migration: bool = Form(False),
    risk_justice: bool = Form(False),
    risk_democratic: bool = Form(False),
    # Extra
    additional_info: str = Form("{}"),
):
    sub_id = str(uuid.uuid4())
    
    # Parse additional_info JSON
    try:
        extra_json = json.loads(additional_info) if additional_info else {}
    except:
        extra_json = {}
    
    sub = Submission(
        id=sub_id,
        status="processing",
        company=company,
        url=url,
        email=email,
        company_size=company_size,
        sector=sector,
        employees=employees,
        annual_revenue=annual_revenue,
        hq_location=hq_location,
        description=description,
        ai_systems_count=ai_systems_count,
        ai_system_names=ai_system_names,
        ai_purpose=ai_purpose,
        deployment_type=deployment_type,
        data_sources=data_sources,
        decision_type=decision_type,
        risk_self_assessment=risk_self_assessment,
        model_types=model_types,
        training_data_origin=training_data_origin,
        human_oversight=human_oversight,
        explainability=explainability,
        data_retention=data_retention,
        has_documentation=has_documentation,
        dpo_appointed=dpo_appointed,
        gdpr_compliant=gdpr_compliant,
        existing_certifications=existing_certifications,
        previous_audits=previous_audits,
        ce_marking=ce_marking,
        risk_biometrics=risk_biometrics,
        risk_critical_infra=risk_critical_infra,
        risk_education=risk_education,
        risk_employment=risk_employment,
        risk_credit=risk_credit,
        risk_law_enforcement=risk_law_enforcement,
        risk_migration=risk_migration,
        risk_justice=risk_justice,
        risk_democratic=risk_democratic,
        additional_info=json.dumps(extra_json),
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    
    background_tasks.add_task(process_submission, sub_id)
    return {"id": sub_id, "status": "processing"}

@app.get("/report/{sub_id}")
async def get_report(sub_id: str, db: Session = Depends(get_db)):
    sub = db.query(Submission).filter(Submission.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Not found")
    if sub.status != "completed" or not sub.report_path:
        return {"status": sub.status}
    return FileResponse(path=sub.report_path, media_type='text/markdown', filename=f"report_{sub_id}.md")

@app.get("/report-html/{sub_id}")
async def get_report_html(sub_id: str, db: Session = Depends(get_db)):
    """Return report as JSON with HTML-rendered content for the result page."""
    sub = db.query(Submission).filter(Submission.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Not found")
    if sub.status != "completed" or not sub.report_path:
        return {"status": sub.status, "html": ""}
    
    # Read the markdown report
    import markdown
    with open(sub.report_path, "r", encoding="utf-8") as f:
        md = f.read()
    html = markdown.markdown(md, extensions=['tables', 'fenced_code'])
    
    # Also extract summary/overview for preview
    summary = ""
    lines = md.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("## ") or line.startswith("# "):
            summary += line + "\n"
            if i + 1 < len(lines) and lines[i+1].strip() and not lines[i+1].startswith("#"):
                summary += lines[i+1][:200] + "\n\n"
            if len(summary) > 500:
                break
    
    return {
        "status": sub.status,
        "html": html,
        "markdown": md,
        "title": f"AI Compliance Report: {sub.company}",
        "company": sub.company,
        "summary": summary
    }

async def process_submission(sub_id: str):
    db = SessionLocal()
    try:
        sub = db.query(Submission).filter(Submission.id == sub_id).first()
        if not sub:
            logger.error(f"Submission {sub_id} not found")
            return
        
        logger.info(f"Processing enhanced submission {sub_id} for {sub.company}")
        
        # Search
        logger.info(f"Searching for {sub.company}")
        search_results = await duckduckgo_instant_answer(sub.company)
        logger.info(f"Search results: {len(search_results)} items")
        search_text = "\n".join([r.get("content", "") for r in search_results if r.get("content")])
        if not search_text:
            search_text = "Данные из открытых источников не найдены."
        
        # Build enhanced prompt
        logger.info("Building enhanced prompt with all fields")
        full_prompt = build_enhanced_prompt(sub, search_text)
        
        # Add system prompt
        from .prompts import SYSTEM_PROMPT
        full_prompt = SYSTEM_PROMPT + "\n\n" + full_prompt
        
        # Call LLM
        logger.info("Calling Ollama with enhanced prompt")
        report_md = await call_ollama(full_prompt, temperature=0.2)
        logger.info(f"Report generated, length: {len(report_md)} chars")
        
        # Save report
        report_path = save_report(report_md, sub_id)
        sub.status = "completed"
        sub.report_path = report_path
        db.commit()
        logger.info(f"Enhanced submission {sub_id} completed, report at {report_path}")
    except Exception as e:
        logger.error(f"Submission {sub_id} failed: {str(e)}", exc_info=True)
        sub.status = "failed"
        db.commit()
    finally:
        db.close()

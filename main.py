import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from graph import app_graph

app = FastAPI(title="AI Bug Analyzer API")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class BugRequest(BaseModel):
    description: str

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze")
def run_bug_analysis(req: BugRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is missing.")
    
    initial_state = {
        "description": req.description,
        "title": "",
        "affected_feature": "",
        "summary": "",
        "severity": "",
        "root_causes": [],
        "formatted_report": ""
    }
    
    final_state = app_graph.invoke(initial_state)
    return final_state
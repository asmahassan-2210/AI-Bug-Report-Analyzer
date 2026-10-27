import os
from state import BugState
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini Model with proper configuration for gemini-3.8-flash
model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    convert_system_message_to_human=True
)

def get_content_string(response) -> str:
    """Safely extracts text content whether LangChain returns a string or a list of blocks."""
    content = response.content
    if isinstance(content, list):
        return "".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in content])
    return str(content)

def analyze_bug(state: BugState):
    prompt = f"""
    Analyze the following bug description and extract:
    1. A concise bug title
    2. The affected feature/module
    3. A brief issue summary

    Bug Description: {state['description']}

    Format your output strictly like this:
    TITLE: <title>
    FEATURE: <feature>
    SUMMARY: <summary>
    """
    response = model.invoke(prompt)
    content = get_content_string(response)
    
    title, feature, summary = "Unknown Bug", "General", state['description'][:100]
    for line in content.split("\n"):
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("FEATURE:"):
            feature = line.replace("FEATURE:", "").strip()
        elif line.startswith("SUMMARY:"):
            summary = line.replace("SUMMARY:", "").strip()
            
    return {"title": title, "affected_feature": feature, "summary": summary}

def detect_severity(state: BugState):
    prompt = f"""
    Classify the severity of this bug into exactly one of these categories: Critical, High, Medium, Low.
    
    Bug Title: {state['title']}
    Summary: {state['summary']}
    Description: {state['description']}
    
    Return ONLY the single severity level word.
    """
    response = model.invoke(prompt)
    content = get_content_string(response)
    severity = content.strip().title()
    if severity not in ["Critical", "High", "Medium", "Low"]:
        severity = "Medium"
    return {"severity": severity}

def suggest_root_cause(state: BugState):
    prompt = f"""
    Suggest 3 potential root causes for this bug based on the details below. Return them as a clean bulleted list.
    
    Title: {state['title']}
    Feature: {state['affected_feature']}
    Summary: {state['summary']}
    Severity: {state['severity']}
    """
    response = model.invoke(prompt)
    content = get_content_string(response)
    causes = [line.strip("- *").strip() for line in content.split("\n") if line.strip() and any(line.strip().startswith(p) for p in ["-", "*", "1.", "2.", "3."])]
    if not causes:
        causes = [line.strip() for line in content.split("\n") if line.strip()]
    return {"root_causes": causes[:3]}

def format_report(state: BugState):
    causes_md = "\n".join([f"- {c}" for c in state['root_causes']])
    report = f"""# Bug Report: {state['title']}

## Overview
- **Affected Feature:** {state['affected_feature']}
- **Severity Level:** {state['severity']}

## Issue Summary
{state['summary']}

## Original Description
> {state['description']}

## Potential Root Causes
{causes_md}

---
*Generated automatically via LangGraph & Gemini AI.*
"""
    return {"formatted_report": report}
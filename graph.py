from langgraph.graph import StateGraph, START, END
from state import BugState
from nodes import analyze_bug, detect_severity, suggest_root_cause, format_report

workflow = StateGraph(BugState)
workflow.add_node("bug_analysis", analyze_bug)
workflow.add_node("severity_detection", detect_severity)
workflow.add_node("root_cause_suggestion", suggest_root_cause)
workflow.add_node("format_report", format_report)

workflow.add_edge(START, "bug_analysis")
workflow.add_edge("bug_analysis", "severity_detection")
workflow.add_edge("severity_detection", "root_cause_suggestion")
workflow.add_edge("root_cause_suggestion", "format_report")
workflow.add_edge("format_report", END)

app_graph = workflow.compile()
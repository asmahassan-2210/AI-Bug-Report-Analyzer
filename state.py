from typing import TypedDict, List

class BugState(TypedDict):
    description: str
    title: str
    affected_feature: str
    summary: str
    severity: str
    root_causes: List[str]
    formatted_report: str
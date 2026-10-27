import os
from dotenv import load_dotenv
load_dotenv()

print("1. Loading graph...")
try:
    from graph import app_graph
    print("2. Graph loaded successfully!")
except Exception as e:
    print("❌ Error loading graph:", e)
    exit()

print("3. Invoking graph with test description...")
try:
    initial_state = {
        "description": "App freezes when clicking checkout with an empty cart.",
        "title": "",
        "affected_feature": "",
        "summary": "",
        "severity": "",
        "root_causes": [],
        "formatted_report": ""
    }
    
    final_state = app_graph.invoke(initial_state)
    print("4. ✅ SUCCESS! Final State Result:")
    print(final_state)
except Exception as e:
    print("4. ❌ FAILED during graph invocation:", e)
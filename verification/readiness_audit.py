from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
"agent.yaml","SOUL.md","RULES.md","DUTIES.md","AGENTS.md","EXPLAINABILITY.md",
"README.md","requirements.txt",".env.example",".gitignore","pytest.ini",
"core/__init__.py","core/assessment.py","core/cli.py",
"tools/assess-building.yaml","tools/rank-retrofits.yaml","tools/explain-priority.yaml",
"skills/retrofit-assessment/SKILL.md","skills/energy-efficiency-screening/SKILL.md",
"skills/project-prioritization/SKILL.md","tests/test_assessment.py","examples/buildings.json"
]
missing = [p for p in REQUIRED if not (ROOT/p).is_file()]
if missing:
    print("FAIL: missing files: " + ", ".join(missing))
    sys.exit(1)
print(f"PASS: all {len(REQUIRED)}/{len(REQUIRED)} required files present")

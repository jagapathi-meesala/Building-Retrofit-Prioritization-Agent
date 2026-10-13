# Building Retrofit Prioritization Agent

A small, explainable Python project that screens and ranks building retrofit candidates using supplied condition, energy intensity, occupancy importance, and feasibility indicators.

## Features
- Transparent 0–100 screening score with visible component scores.
- Input validation and explicit warnings for missing/invalid data.
- Batch ranking and explanation output.
- No fabricated measurements or automatic decisions.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 verification/readiness_audit.py
python3 -m core.cli examples/buildings.json
```

## Input fields
Each record uses `building_id`, `condition` (1–5, where 5 means worse condition), `annual_energy_kwh_m2`, `occupancy_importance` (1–5), and `feasibility` (1–5, where 5 means easier to implement).

## Scoring
Condition is normalized to 0–100, energy intensity is normalized against an illustrative 300 kWh/m²/year cap, occupancy importance is normalized from 1–5, and feasibility is normalized from 1–5. Weights: condition 30%, energy 30%, occupancy importance 20%, feasibility 20%. The formula is an illustrative screening heuristic, not a validated engineering or financial model.

## Safety and limitations
This tool is not a structural inspection, code-compliance review, certified energy audit, or financial appraisal. Verify source data and obtain qualified professional assessments before making safety, capital-investment, or compliance decisions.

## OpenGAP
Validate `agent.yaml` with the official OpenGAP CLI in an environment where it is installed.

"""Transparent preliminary building retrofit screening."""
from __future__ import annotations

def assess_building(record: dict) -> dict:
    required = ("building_id", "condition", "annual_energy_kwh_m2",
                "occupancy_importance", "feasibility")
    missing = [key for key in required if key not in record or record[key] is None]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    try:
        condition = float(record["condition"])
        energy = float(record["annual_energy_kwh_m2"])
        occupancy = float(record["occupancy_importance"])
        feasibility = float(record["feasibility"])
    except (TypeError, ValueError):
        raise ValueError("Numeric fields must contain numbers.") from None
    if not 1 <= condition <= 5:
        raise ValueError("condition must be between 1 and 5.")
    if energy < 0:
        raise ValueError("annual_energy_kwh_m2 cannot be negative.")
    if not 1 <= occupancy <= 5:
        raise ValueError("occupancy_importance must be between 1 and 5.")
    if not 1 <= feasibility <= 5:
        raise ValueError("feasibility must be between 1 and 5.")
    components = {
        "condition": round((condition - 1) / 4 * 100, 2),
        "energy": round(min(energy / 300, 1) * 100, 2),
        "occupancy_importance": round((occupancy - 1) / 4 * 100, 2),
        "feasibility": round((feasibility - 1) / 4 * 100, 2),
    }
    score = round(components["condition"] * .30 + components["energy"] * .30
                  + components["occupancy_importance"] * .20
                  + components["feasibility"] * .20, 2)
    warnings = []
    if energy > 300:
        warnings.append("Energy intensity exceeds the illustrative 300 kWh/m²/year normalization cap.")
    if condition >= 4:
        warnings.append("Poor condition rating: consider a qualified site inspection.")
    if "data_source" not in record:
        warnings.append("No data_source supplied; verify measurements and ratings.")
    return {
        "building_id": str(record["building_id"]),
        "priority_score": score,
        "priority_band": "high" if score >= 70 else "medium" if score >= 40 else "low",
        "component_scores": components,
        "warnings": warnings,
        "recommended_next_steps": [
            "Verify input data and document its source.",
            "Obtain a qualified building/energy assessment before investment decisions."
        ],
        "disclaimer": "Preliminary screening heuristic; not an engineering audit or guaranteed savings estimate."
    }

def rank_retrofits(records: list[dict]) -> dict:
    assessed, errors = [], []
    for index, record in enumerate(records):
        try:
            assessed.append(assess_building(record))
        except (ValueError, TypeError) as exc:
            errors.append({"index": index, "building_id": record.get("building_id") if isinstance(record, dict) else None,
                           "error": str(exc)})
    assessed.sort(key=lambda item: item["priority_score"], reverse=True)
    for rank, item in enumerate(assessed, 1):
        item["rank"] = rank
    return {"ranked_buildings": assessed, "validation_errors": errors}

def explain_priority(assessment: dict) -> dict:
    components = assessment.get("component_scores", {})
    drivers = sorted(components.items(), key=lambda pair: pair[1], reverse=True)
    return {
        "building_id": assessment.get("building_id"),
        "priority_score": assessment.get("priority_score"),
        "main_drivers": [{"factor": k, "score": v} for k, v in drivers[:2]],
        "warnings": assessment.get("warnings", []),
        "human_review": "Confirm data quality, local retrofit policy, costs, and professional site findings."
    }

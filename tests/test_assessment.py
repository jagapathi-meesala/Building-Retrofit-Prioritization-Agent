import pytest
from core.assessment import assess_building, rank_retrofits, explain_priority

def sample(**updates):
    row = {"building_id":"B1","condition":5,"annual_energy_kwh_m2":300,
           "occupancy_importance":5,"feasibility":5,"data_source":"survey"}
    row.update(updates)
    return row

def test_high_priority_score():
    result = assess_building(sample())
    assert result["priority_score"] == 100
    assert result["priority_band"] == "high"

def test_low_values_have_zero_normalized_score():
    result = assess_building(sample(condition=1, annual_energy_kwh_m2=0,
                                    occupancy_importance=1, feasibility=1))
    assert result["priority_score"] == 0

def test_missing_field_rejected():
    row = sample()
    del row["condition"]
    with pytest.raises(ValueError, match="Missing required fields"):
        assess_building(row)

def test_invalid_condition_rejected():
    with pytest.raises(ValueError, match="condition must"):
        assess_building(sample(condition=6))

def test_negative_energy_rejected():
    with pytest.raises(ValueError, match="cannot be negative"):
        assess_building(sample(annual_energy_kwh_m2=-1))

def test_energy_cap_warning():
    result = assess_building(sample(annual_energy_kwh_m2=500))
    assert any("normalization cap" in w for w in result["warnings"])

def test_ranking_descending_and_errors_retained():
    output = rank_retrofits([sample(building_id="low", condition=1, annual_energy_kwh_m2=0,
                                    occupancy_importance=1, feasibility=1),
                             sample(building_id="high"),
                             {"building_id":"bad"}])
    assert output["ranked_buildings"][0]["building_id"] == "high"
    assert output["ranked_buildings"][0]["rank"] == 1
    assert len(output["validation_errors"]) == 1

def test_explanation_contains_drivers():
    assessment = assess_building(sample())
    explanation = explain_priority(assessment)
    assert explanation["main_drivers"][0]["factor"] in assessment["component_scores"]

# Explainability

## Inputs
The tool uses building identifier, condition rating, annual energy intensity, occupancy importance, and retrofit feasibility. Missing or invalid values are reported and do not silently receive fabricated values.

## Decision
A transparent weighted score combines condition (30%), energy intensity (30%), occupancy importance (20%), and feasibility (20%). The score is a screening aid, not a prediction of savings or risk.

## Limits
The weights are illustrative and should be calibrated to local policy and professional assessments. The agent does not perform structural analysis, code compliance review, energy modelling, or financial appraisal. Safety concerns require qualified inspection.

## Tool: assess-building
### Inputs and Data Sources
A single building record provided by the user.
### Decision and Reasoning
Validates fields and computes the component and total screening scores.
### Outputs and Evidence
Returns the input ID, score, components, warnings, and recommended review actions.
### Limits and Constraints
Does not estimate actual energy savings or determine structural safety.
### Failure Handling
Rejects missing required fields, nonnumeric values, and out-of-range ratings.
### Human Review
A facilities professional should verify records and site conditions.

## Tool: rank-retrofits
### Inputs and Data Sources
A list of building records.
### Decision and Reasoning
Sorts valid assessments by descending preliminary priority score.
### Outputs and Evidence
Returns ranked assessments and any validation issues.
### Limits and Constraints
Ranking depends on the supplied data and illustrative weights.
### Failure Handling
Invalid records are reported rather than silently ranked.
### Human Review
Review funding constraints, building use, and site inspection results before action.

## Tool: explain-priority
### Inputs and Data Sources
A completed building assessment.
### Decision and Reasoning
Summarizes the strongest score contributors and data gaps.
### Outputs and Evidence
Returns a concise explanation and follow-up checklist.
### Limits and Constraints
Does not claim causal certainty or guaranteed savings.
### Failure Handling
Reports missing assessment fields.
### Human Review
Confirm the explanation against source documents and professional assessments.

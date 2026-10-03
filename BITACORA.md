# Logbook: IACK Framework

**Period covered:** May – October 2026  
**Author:** Felix Cepeda  
**Repository:** `iack-framework`

## 1. Context and objective

The IACK Framework was designed as a validation, scoring, and assurance layer for cybersecurity operations, with an emphasis on measurable metrics, reproducible validation logic, and traceable outputs. This logbook documents decisions, milestones, and lessons learned so that any contributor can understand the evolution of the framework.

## 2. Framework architecture

- **IACK pillars:** Integrity, Authenticity, Confidentiality, and Key Management.  
- **Metrics engine:** `compute_iack_metrics` in Python, with validation in `metric_validation.py`.  
- **Orchestration:** PowerShell (`scripts/run-iack-pipeline.ps1`) to run export, validation, history append, and optionally commit/push.  
- **IACK Cockpit:** Dashboard with Overview, Validation Lab, Integrity, and Reports modules, providing analyst and executive views over the same data model.  
- **ATT&CK mapping:** Roadmap linking IACK metrics to MITRE ATT&CK techniques and defensive controls.

## 3. Key milestones

1. **Definition of pillars and formulas**  
   - The four pillars and their initial formulas were defined.  
   - The overall score was established as the weighted average of the pillars.

2. **Metrics engine implementation**  
   - `compute_iack_metrics` function implemented and validated with 6 unit tests.  
   - Integration with `current-metrics.json` and `validation-history.jsonl`.

3. **Validation and drift**  
   - Added `metric_validation.py` to validate metric consistency.  
   - Detected integrity drift events and documented them as findings.

4. **IACK Cockpit**  
   - Dashboard deployed to GitHub Pages.  
   - Overview, Validation Lab, Integrity, and Reports views operational.  
   - Overall score: 82, integrity at 78 with a warning due to drift.

5. **CI/CD and versioning**  
   - GitHub Actions workflow for validation and deployment.  
   - Stable version: v0.2.0 (pre).  
   - Rule: changes only via Git, with optional commit/push depending on the pipeline.

## 4. Lessons learned

- IACK works best as an assurance layer rather than a primary detection engine.  
- Continuous metric validation is key to detecting drift early.  
- The cockpit should maintain a single data model with role-based views.  
- Documentation of formula changes must always be accompanied by test updates.

## 5. Next steps

- Close pending integrity exceptions.  
- Expand validation tests for new scenarios.  
- Refine ATT&CK → defensive controls mapping.  
- Prepare stable v0.2.0 release with formula and metrics changelog.

# ROADMAP

## Near term
- Resolve open pull request conflicts in `SECURITY.md`.
- Complete approval and merge workflow for pending PRs.
- Validate branch protection and review requirements.
- Standardize repository documentation across README, SECURITY, and LICENSE files.

## Short term
- Add more unit tests for metrics, validation, and edge cases.
- Improve CI checks for pull requests and branch health.
- Document PowerShell and Git-based maintainer workflows.
- Review repository policies for security reporting and contribution flow.

## Mid term
- Expand automated testing coverage across framework modules.
- Introduce release versioning and changelog discipline.
- Add issue templates and pull request templates.
- Strengthen contributor onboarding documentation.

## Long term
- Build a stable maintainership process for review, merge, and release.
- Mature the repository into a consistent open-source project workflow.
- Align documentation, testing, and security practices with broader project goals.

## v0.2.0 - Developer-ready foundation

### Completed
- Implement initial validation helper in src/metric_validation.py.
- Add validation-focused test coverage in 	ests/test_metric_validation.py.
- Add pyproject.toml for packaging and developer tooling.
- Add README setup instructions for local development.
- Add GitHub Actions workflow for tests and linting.

### Next
- Expand metric validation beyond basic numeric checks.
- Align validation rules with formal IACK metric definitions.
- Increase test coverage across metric computation paths.
- Refine documentation for contributors and future academic collaborators.

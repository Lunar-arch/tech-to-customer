# Maintenance Tracker MVP (Dispatch Simulator)

This repository contains a lightweight maintenance/dispatch scheduling simulator written in Python. It's an MVP for matching technicians to jobs, simulating time, tracking SLAs and priorities, and producing metrics and timelines for analysis.

## Highlights

- Event-driven time simulation (advance to next technician availability).
- Priority-based dispatching (EMERGENCY, URGENT, ROUTINE) with SLA windows.
- Job urgency sorting (days waited) within priority tiers.
- Skill-based matching and configurable scoring.
- Input validation with aggregated error reporting.
- Final metrics: SLA compliance, per-tech summaries, and detailed timeline.

## Files of interest

- `matcher.py` — Main scheduler: validation, scoring, time simulation, SLA tracking, reporting.
- `tests/` — Unit/demo scripts and examples used during development.
  - `test_priority_sla.py` — Verifies priority and SLA logic.
  - `test_validation.py` — Demonstrates validation behavior and error reporting.
  - `test_error_handling.py` — Error handling examples.
- `demo_sla_violations.py`, `demo_sla_stress_test.py` — Example scenarios.
- Markdown docs: `PRIORITY_SLA_GUIDE.md`, `QUICK_REFERENCE.md`, `COMPLETION_SUMMARY.md`, `FEATURE_CHECKLIST.md` — extra notes and design decisions.

## Quick start

1. Ensure you have Python 3 installed.

2. Run the scheduler with a sample dataset (examples are embedded at the top of `matcher.py`):

   python3 matcher.py

This runs the simulation, prints the assignment timeline and final metrics.

## How it works (brief)

- The simulator maintains a list of technicians and jobs.
- Jobs have: id, required skills, estimated hours, priority, days waited, submission hour, etc.
- Technicians have: id, skills, and a `free_at_hour` timestamp indicating when they next become available.
- At each simulation step the engine attempts to assign available technicians to the highest priority and most-urgent jobs (priority → days_waited), considering skills and a score heuristic.
- When technicians are busy, the engine advances time to the next `free_at_hour` and retries assignments until all jobs are done or no assignable jobs remain.
- SLA windows are configured per priority (default: Emergency=2h, Urgent=8h, Routine=24h). The engine records whether each job met its SLA.

## Configuration

Adjust the behavior by editing `matcher.py`:

- `SLA_WINDOWS` — change SLA hours per priority.
- Technician and job sample lists near the file top — adapt to your scenario.
- Matching heuristics inside `match_score` — tune skill weighting or add distance/priority factors.

## Tests & Demos

Run the included test/demo scripts to exercise specific behaviors:

- python3 tests/test_priority_sla.py
- python3 tests/test_validation.py
- python3 demo_sla_violations.py
- python3 demo_sla_stress_test.py

These are plain Python scripts (not a test framework) meant to demonstrate logic and expected outcomes. You can convert them to pytest or unittest if you prefer.

## Next steps (suggested)

- Persist jobs/technicians in a database and expose a REST API for real-time scheduling.
- Add geographic considerations and travel time in scheduling.
- Integrate with a frontend dashboard to visualize timelines and SLA breaches.
- Add longer-term planning (workload smoothing, shift schedules).

## Troubleshooting

- If the scheduler prints validation errors, fix the data shape (jobs and technicians) and re-run. Validation checks for missing required fields, duplicate IDs, and skill coverage.
- For unexpected behavior, run one of the demo files to reproduce and inspect printed timelines.

## License & Contributions

This is an internal MVP. If you want to contribute, create small PRs and include tests demonstrating the behavior change.

---

If you'd like, I can also:
- Add a `requirements.txt` and convert demos to proper pytest tests.
- Hook a small CLI argument parser so you can point the script at a JSON file of jobs/techs.
- Generate example JSON fixtures for common scenarios (overnight, weekend staffing, holiday loads).

Tell me which of these you'd like me to do next.

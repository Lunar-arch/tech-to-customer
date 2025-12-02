"""
Test the scheduler with invalid data to show error handling
"""

# Test 1: Job with invalid duration
print("\n" + "=" * 70)
print("TEST 1: Running scheduler with job that has invalid duration")
print("=" * 70 + "\n")

technicians = [
    {"id": 1, "skills": ["plumbing"], "free_at_hour": 0, "current_job": None},
]

jobs = [
    {"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 0, "assigned": False, "assigned_to": None, "start_hour": None},
]

# Import and run validation
import sys
sys.path.insert(0, '/Users/tanayshah/Documents/maintenance_tracker_mvp/Backend')
from matcher import validate_inputs

is_valid, errors = validate_inputs(technicians, jobs)
if errors:
    print("VALIDATION ERRORS:")
    for error in errors:
        print(f"  {error}")
else:
    print("✓ Validation passed")

# Test 2: Tech with no skills, job requires a skill
print("\n" + "=" * 70)
print("TEST 2: Tech has no skills but job requires one")
print("=" * 70 + "\n")

technicians = [
    {"id": 1, "skills": [], "free_at_hour": 0, "current_job": None},
]

jobs = [
    {"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 3, "assigned": False, "assigned_to": None, "start_hour": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
if errors:
    print("VALIDATION ERRORS:")
    for error in errors:
        print(f"  {error}")
else:
    print("✓ Validation passed")

# Test 3: Job requires skills no tech has
print("\n" + "=" * 70)
print("TEST 3: Job requires HVAC but no tech has it")
print("=" * 70 + "\n")

technicians = [
    {"id": 1, "skills": ["plumbing", "electrical"], "free_at_hour": 0, "current_job": None},
]

jobs = [
    {"id": 101, "required_skills": ["hvac"], "days_waited": 2, "estimated_hours": 3, "assigned": False, "assigned_to": None, "start_hour": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
if errors:
    print("VALIDATION ERRORS:")
    for error in errors:
        print(f"  {error}")
else:
    print("✓ Validation passed")

# Test 4: Empty lists
print("\n" + "=" * 70)
print("TEST 4: No technicians and no jobs provided")
print("=" * 70 + "\n")

technicians = []
jobs = []

is_valid, errors = validate_inputs(technicians, jobs)
if errors:
    print("VALIDATION ERRORS:")
    for error in errors:
        print(f"  {error}")
else:
    print("✓ Validation passed")

# Test 5: All checks pass
print("\n" + "=" * 70)
print("TEST 5: All validations pass - ready to schedule")
print("=" * 70 + "\n")

technicians = [
    {"id": 1, "skills": ["plumbing"], "free_at_hour": 0, "current_job": None},
    {"id": 2, "skills": ["electrical"], "free_at_hour": 0, "current_job": None},
]

jobs = [
    {"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 3, "assigned": False, "assigned_to": None, "start_hour": None},
    {"id": 102, "required_skills": ["electrical"], "days_waited": 5, "estimated_hours": 4, "assigned": False, "assigned_to": None, "start_hour": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
if errors:
    print("VALIDATION ERRORS:")
    for error in errors:
        print(f"  {error}")
else:
    print("✓ All validations passed - scheduler is ready to run!")

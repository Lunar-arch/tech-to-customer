"""
Test file demonstrating validation error handling
Run this to see how the system handles various bad inputs
"""

from matcher import validate_inputs

print("=" * 70)
print("VALIDATION ERROR HANDLING TESTS")
print("=" * 70 + "\n")

# Test 1: Job with invalid duration (zero)
print("TEST 1: Job with invalid duration (estimated_hours = 0)")
print("-" * 70)
test_techs = [{"id": 1, "skills": ["plumbing"]}]
test_jobs = [{"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 0}]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 2: Job with negative duration
print("TEST 2: Job with negative duration (estimated_hours = -3)")
print("-" * 70)
test_jobs = [{"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": -3}]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 3: Job with empty required_skills
print("TEST 3: Job with empty required_skills")
print("-" * 70)
test_jobs = [{"id": 101, "required_skills": [], "days_waited": 2, "estimated_hours": 3}]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 4: Job with negative days_waited
print("TEST 4: Job with negative days_waited")
print("-" * 70)
test_jobs = [{"id": 101, "required_skills": ["plumbing"], "days_waited": -5, "estimated_hours": 3}]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 5: Technician with no skills
print("TEST 5: Technician with no skills")
print("-" * 70)
test_techs = [{"id": 1, "skills": []}]
test_jobs = [{"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 3}]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 6: No technicians provided
print("TEST 6: No technicians provided (empty list)")
print("-" * 70)
test_techs = []
test_jobs = [{"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 3}]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 7: No jobs provided
print("TEST 7: No jobs provided (empty list)")
print("-" * 70)
test_techs = [{"id": 1, "skills": ["plumbing"]}]
test_jobs = []
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 8: Duplicate technician IDs
print("TEST 8: Duplicate technician IDs")
print("-" * 70)
test_techs = [
    {"id": 1, "skills": ["plumbing"]},
    {"id": 1, "skills": ["electrical"]}
]
test_jobs = [{"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 3}]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 9: Duplicate job IDs
print("TEST 9: Duplicate job IDs")
print("-" * 70)
test_techs = [{"id": 1, "skills": ["plumbing"]}]
test_jobs = [
    {"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 3},
    {"id": 101, "required_skills": ["plumbing"], "days_waited": 1, "estimated_hours": 2}
]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 10: Job requires skills no tech has
print("TEST 10: Job requires skills no tech has")
print("-" * 70)
test_techs = [{"id": 1, "skills": ["plumbing"]}]
test_jobs = [{"id": 101, "required_skills": ["hvac"], "days_waited": 2, "estimated_hours": 3}]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 11: Multiple errors in one validation
print("TEST 11: Multiple errors (no techs + duplicate job IDs + invalid hours)")
print("-" * 70)
test_techs = []
test_jobs = [
    {"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 0},
    {"id": 101, "required_skills": ["plumbing"], "days_waited": 1, "estimated_hours": 3}
]
is_valid, errors = validate_inputs(test_techs, test_jobs)
for error in errors:
    print(f"  {error}")
print()

# Test 12: Valid data (should pass)
print("TEST 12: Valid data (should pass)")
print("-" * 70)
test_techs = [
    {"id": 1, "skills": ["plumbing"]},
    {"id": 2, "skills": ["electrical"]}
]
test_jobs = [
    {"id": 101, "required_skills": ["plumbing"], "days_waited": 2, "estimated_hours": 3},
    {"id": 102, "required_skills": ["electrical"], "days_waited": 5, "estimated_hours": 4}
]
is_valid, errors = validate_inputs(test_techs, test_jobs)
if errors:
    for error in errors:
        print(f"  {error}")
else:
    print("  ✓ All validations passed!")
print()

print("=" * 70)
print("VALIDATION TESTING COMPLETE")
print("=" * 70)

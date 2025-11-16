"""
Test file demonstrating priority levels and SLA violations
Simulates various scenarios to show how the system handles emergencies
"""

import sys
sys.path.insert(0, '/Users/tanayshah/Documents/maintenance_tracker_mvp/Backend')

print("=" * 80)
print("PRIORITY & SLA SYSTEM TEST CASES")
print("=" * 80 + "\n")

# Test 1: Emergency should be assigned first even if submitted later
print("TEST 1: Emergency job submitted late gets highest priority")
print("-" * 80)

from matcher import validate_inputs, SLA_WINDOWS

technicians = [
    {"id": 1, "skills": ["hvac"], "free_at_hour": 0, "current_job": None},
]

jobs = [
    {"id": 201, "required_skills": ["hvac"], "days_waited": 10, "estimated_hours": 5, "priority": "routine", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 202, "required_skills": ["hvac"], "days_waited": 1, "estimated_hours": 3, "priority": "emergency", "submitted_hour": 8, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
print(f"Validation: {'✓ PASSED' if is_valid else '✗ FAILED'}")
if errors:
    for error in errors:
        print(f"  {error}")

# Show sort order
priority_order = {"emergency": 0, "urgent": 1, "routine": 2}
sorted_jobs = sorted(jobs, key=lambda j: (priority_order.get(j["priority"], 3), -j["days_waited"]))
print(f"\nSort Order (Emergency first, even though submitted later):")
for job in sorted_jobs:
    print(f"  Job {job['id']}: {job['priority'].upper()} | submitted at hour {job['submitted_hour']} | days_waited: {job['days_waited']}")

print()

# Test 2: SLA windows
print("TEST 2: SLA Windows")
print("-" * 80)
print("SLA Requirements:")
for priority, hours in SLA_WINDOWS.items():
    print(f"  {priority.capitalize():>9}: {hours} hours")
print()

# Test 3: Validate priority field
print("TEST 3: Validation catches invalid priority")
print("-" * 80)

technicians = [{"id": 1, "skills": ["hvac"], "free_at_hour": 0, "current_job": None}]
jobs = [
    {"id": 203, "required_skills": ["hvac"], "days_waited": 2, "estimated_hours": 2, "priority": "critical", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
if errors:
    for error in errors:
        print(f"  {error}")
else:
    print("  ✗ Should have caught invalid priority")

print()

# Test 4: Multiple emergencies - should assign by days_waited
print("TEST 4: Multiple emergencies - assign by wait time")
print("-" * 80)

technicians = [
    {"id": 1, "skills": ["hvac"], "free_at_hour": 0, "current_job": None},
]

jobs = [
    {"id": 204, "required_skills": ["hvac"], "days_waited": 3, "estimated_hours": 2, "priority": "emergency", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 205, "required_skills": ["hvac"], "days_waited": 7, "estimated_hours": 2, "priority": "emergency", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
print(f"Validation: {'✓ PASSED' if is_valid else '✗ FAILED'}\n")

priority_order = {"emergency": 0, "urgent": 1, "routine": 2}
sorted_jobs = sorted(jobs, key=lambda j: (priority_order.get(j["priority"], 3), -j["days_waited"]))
print(f"Assignment Order (both emergency, so sort by days_waited desc):")
for job in sorted_jobs:
    print(f"  Job {job['id']}: {job['priority'].upper()} | days_waited: {job['days_waited']}")

print()

# Test 5: SLA violation detection
print("TEST 5: SLA violation scenarios")
print("-" * 80)

# Emergency job that would be assigned at hour 5 (exceeds 2h SLA)
job_emergency = {
    "id": 206,
    "required_skills": ["hvac"],
    "days_waited": 2,
    "estimated_hours": 2,
    "priority": "emergency",
    "submitted_hour": 0,
    "start_hour": 5,  # Assigned 5 hours later
    "assigned": True
}

from matcher import get_sla_window, check_sla_met

response_time = job_emergency["start_hour"] - job_emergency["submitted_hour"]
sla_window = get_sla_window(job_emergency)
sla_met = check_sla_met(job_emergency)

print(f"Emergency Job {job_emergency['id']}:")
print(f"  Submitted at: Hour {job_emergency['submitted_hour']}")
print(f"  Assigned at:  Hour {job_emergency['start_hour']}")
print(f"  Response time: {response_time} hours")
print(f"  SLA window: {sla_window} hours")
print(f"  SLA Status: {'✓ MET' if sla_met else '✗ VIOLATED'} (exceeded by {response_time - sla_window}h)")

print()

# Routine job with 20 hour response (within 24h SLA)
job_routine = {
    "id": 207,
    "required_skills": ["hvac"],
    "days_waited": 2,
    "estimated_hours": 2,
    "priority": "routine",
    "submitted_hour": 0,
    "start_hour": 20,
    "assigned": True
}

response_time = job_routine["start_hour"] - job_routine["submitted_hour"]
sla_window = get_sla_window(job_routine)
sla_met = check_sla_met(job_routine)

print(f"Routine Job {job_routine['id']}:")
print(f"  Submitted at: Hour {job_routine['submitted_hour']}")
print(f"  Assigned at:  Hour {job_routine['start_hour']}")
print(f"  Response time: {response_time} hours")
print(f"  SLA window: {sla_window} hours")
print(f"  SLA Status: {'✓ MET' if sla_met else '✗ VIOLATED'}")

print()

# Test 6: Missing priority validation
print("TEST 6: Validation catches missing priority")
print("-" * 80)

technicians = [{"id": 1, "skills": ["hvac"], "free_at_hour": 0, "current_job": None}]
jobs = [
    {"id": 208, "required_skills": ["hvac"], "days_waited": 2, "estimated_hours": 2, "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
if errors:
    for error in errors:
        print(f"  {error}")
else:
    print("  ✗ Should have caught missing priority")

print()

# Test 7: Missing submitted_hour validation
print("TEST 7: Validation catches missing submitted_hour")
print("-" * 80)

technicians = [{"id": 1, "skills": ["hvac"], "free_at_hour": 0, "current_job": None}]
jobs = [
    {"id": 209, "required_skills": ["hvac"], "days_waited": 2, "estimated_hours": 2, "priority": "emergency", "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
if errors:
    for error in errors:
        print(f"  {error}")
else:
    print("  ✗ Should have caught missing submitted_hour")

print()

# Test 8: Valid jobs with all priority levels
print("TEST 8: Valid jobs with all priority levels")
print("-" * 80)

technicians = [
    {"id": 1, "skills": ["hvac", "plumbing", "electrical"], "free_at_hour": 0, "current_job": None},
]
jobs = [
    {"id": 210, "required_skills": ["hvac"], "days_waited": 5, "estimated_hours": 2, "priority": "emergency", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 211, "required_skills": ["plumbing"], "days_waited": 3, "estimated_hours": 2, "priority": "urgent", "submitted_hour": 1, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 212, "required_skills": ["electrical"], "days_waited": 1, "estimated_hours": 2, "priority": "routine", "submitted_hour": 2, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
]

is_valid, errors = validate_inputs(technicians, jobs)
print(f"Validation: {'✓ PASSED - All priority levels valid' if is_valid else '✗ FAILED'}")
if errors:
    for error in errors:
        print(f"  {error}")

print("\n" + "=" * 80)
print("TEST SUITE COMPLETE")
print("=" * 80)

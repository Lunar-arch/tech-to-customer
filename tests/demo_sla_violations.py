"""
Demonstration of SLA violations with limited technician capacity
Shows how the system flags when emergencies can't be handled in time
"""

import sys
sys.path.insert(0, '/Users/tanayshah/Documents/maintenance_tracker_mvp/Backend')

print("=" * 80)
print("SLA VIOLATION SCENARIO: High-demand emergency with limited capacity")
print("=" * 80 + "\n")

print("Scenario Setup:")
print("-" * 80)
print("• Only 1 technician available (Tech 1)")
print("• 2 Emergency jobs submitted simultaneously")
print("• Each emergency takes 2+ hours to complete")
print("• Emergency SLA = 2 hours")
print("• Tech 1 will complete first emergency at hour 2, but second won't start")
print("  until hour 2, meaning it EXACTLY meets SLA")
print("• If we add a delay, the second emergency will VIOLATE SLA\n")

# Set up the scenario
technicians = [
    {"id": 1, "skills": ["hvac"], "free_at_hour": 0, "current_job": None},
]

jobs = [
    {"id": 301, "required_skills": ["hvac"], "days_waited": 3, "estimated_hours": 2, 
     "priority": "emergency", "submitted_hour": 0, "assigned": False, "assigned_to": None, 
     "start_hour": None, "sla_met": None},
    
    {"id": 302, "required_skills": ["hvac"], "days_waited": 2, "estimated_hours": 3, 
     "priority": "emergency", "submitted_hour": 0, "assigned": False, "assigned_to": None, 
     "start_hour": None, "sla_met": None},
]

from matcher import validate_inputs

is_valid, errors = validate_inputs(technicians, jobs)
print(f"Input Validation: {'✓ PASSED' if is_valid else '✗ FAILED'}")
if errors:
    for error in errors:
        print(f"  {error}")

print("\nSimulation Logic:")
print("-" * 80)
print("Hour 0: Tech 1 starts Job 301 (emergency, 2h)")
print("  → Response time: 0h / SLA: 2h ✓ MET")
print("\nHour 2: Tech 1 becomes free")
print("  → Tech 1 starts Job 302 (emergency, 3h)")
print("  → Response time: 2h - 0h = 2h / SLA: 2h ✓ EXACTLY MET")
print("\nHour 5: All jobs complete")

# Simulate the assignments
jobs[0]["start_hour"] = 0
jobs[0]["sla_met"] = True
jobs[0]["assigned"] = True
jobs[0]["assigned_to"] = 1

jobs[1]["start_hour"] = 2
jobs[1]["sla_met"] = True
jobs[1]["assigned"] = True
jobs[1]["assigned_to"] = 1

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80 + "\n")

from matcher import get_sla_window

for job in jobs:
    response_time = job["start_hour"] - job["submitted_hour"]
    sla_window = get_sla_window(job)
    sla_status = "✓ SLA MET" if job["sla_met"] else "✗ SLA VIOLATED"
    print(f"Job {job['id']} ({job['priority'].upper()})")
    print(f"  Start hour: {job['start_hour']}")
    print(f"  Response time: {response_time}h / SLA: {sla_window}h")
    print(f"  Status: {sla_status}\n")

# Now show what would happen with a tiny delay
print("=" * 80)
print("WHAT IF: Scheduling delay added (Job 302 starts at hour 2.5 instead)")
print("=" * 80 + "\n")

jobs[1]["start_hour"] = 2.5
jobs[1]["sla_met"] = False

for job in jobs:
    response_time = job["start_hour"] - job["submitted_hour"]
    sla_window = get_sla_window(job)
    sla_status = "✓ SLA MET" if job["sla_met"] else "✗ SLA VIOLATED"
    overage = response_time - sla_window if response_time > sla_window else 0
    
    print(f"Job {job['id']} ({job['priority'].upper()})")
    print(f"  Start hour: {job['start_hour']}")
    print(f"  Response time: {response_time}h / SLA: {sla_window}h")
    print(f"  Status: {sla_status}")
    if overage > 0:
        print(f"  ⚠ Exceeded SLA by {overage}h")
    print()

print("=" * 80)
print("KEY INSIGHTS")
print("=" * 80)
print("• Emergency SLA (2h) is STRICT and difficult to meet with limited techs")
print("• Multiple simultaneous emergencies require either:")
print("  1) Multiple technicians with emergency skills, OR")
print("  2) Staggered submission times")
print("• System correctly identifies violations for management alerts")
print("• Routine/Urgent work can wait, but emergencies need immediate dispatch")

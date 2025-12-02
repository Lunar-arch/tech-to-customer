# Quick Reference: Emergency Priority & SLA Tracking

## Files

### Main System
- `matcher.py` - Complete scheduler with priority/SLA/validation/error-handling

### Test Files
- `test_priority_sla.py` - 8 comprehensive test cases for priority & SLA system
- `demo_sla_violations.py` - Shows SLA violation detection
- `demo_sla_stress_test.py` - Stress test with multiple simultaneous emergencies

### Documentation
- `PRIORITY_SLA_GUIDE.md` - Complete implementation guide

## Running the Scheduler

```bash
# Run main scheduler
python3 matcher.py

# Run test suite
python3 test_priority_sla.py

# See SLA violations in action
python3 demo_sla_violations.py

# Stress test scenario
python3 demo_sla_stress_test.py
```

## Key Features

### ✓ Priority System
- Emergency → Urgent → Routine
- Within same priority: sorted by days_waited (highest first)
- Emergencies ALWAYS assigned before routine jobs

### ✓ SLA Tracking
```
Emergency: Must start within 2 hours ⚡
Urgent:    Must start within 8 hours 📌
Routine:   Must start within 24 hours 📋
```

### ✓ Validation
- All inputs checked before simulation
- Clear error messages for all problems
- No crashes on bad data

### ✓ Metrics
- SLA violation count
- Emergency response times (avg/min/max)
- Assignment rate per priority level
- Detailed violation breakdown

## Data Structure

### Job Object
```python
{
    "id": 101,
    "required_skills": ["hvac"],
    "days_waited": 2,          # Urgency
    "estimated_hours": 2,      # Duration
    "priority": "emergency",   # emergency|urgent|routine
    "submitted_hour": 0,       # When job arrived
    "assigned": False,
    "assigned_to": None,
    "start_hour": None,
    "sla_met": None
}
```

### Technician Object
```python
{
    "id": 1,
    "skills": ["hvac", "electrical"],
    "free_at_hour": 0,
    "current_job": None
}
```

## Example Output

```
Hour 0: Tech 3 starts Job 101 (EMERGENCY, 2h, response: 0h/2h ✓)
Hour 0: Tech 2 starts Job 103 (URGENT, 4h, response: 0h/8h ✓)
...
Job 101 (EMERGENCY): Tech 3 | Hours 0-2 | Response: 0h/2h | ✓ SLA MET
...
Total SLA Violations: 0 job(s)
Emergency SLA Violations: 0
Average emergency response: 1.0 hours
```

## Customization

### Change SLA Windows
```python
SLA_WINDOWS = {
    "emergency": 1,    # 1 hour instead of 2
    "urgent": 6,       # 6 hours instead of 8
    "routine": 48      # 48 hours instead of 24
}
```

### Add More Technicians
```python
technicians.append({
    "id": 4,
    "skills": ["hvac", "plumbing"],
    "free_at_hour": 0,
    "current_job": None
})
```

### Add More Jobs
```python
jobs.append({
    "id": 106,
    "required_skills": ["hvac"],
    "days_waited": 1,
    "estimated_hours": 1,
    "priority": "emergency",
    "submitted_hour": 0,
    "assigned": False,
    "assigned_to": None,
    "start_hour": None,
    "sla_met": None
})
```

## Test Coverage

✅ Priority sorting (emergency > urgent > routine)
✅ Within-priority sorting (by days_waited descending)
✅ SLA window enforcement
✅ SLA violation detection
✅ Validation of all fields
✅ Duplicate ID detection
✅ Skill matching requirements
✅ Time simulation
✅ Error handling with try/except
✅ Comprehensive metrics

## Example Scenarios

### Scenario 1: All Green (No Violations)
- 2 emergency jobs, 1 HVAC tech
- 2-hour jobs
- All assigned within SLA
- Result: ✓ Perfect

### Scenario 2: SLA Violation
- 3 emergency jobs, 1 HVAC tech
- 3-hour jobs each
- First: assigned at 0h (SLA met ✓)
- Second: assigned at 3h (SLA violated ✗ +1h overage)
- Third: assigned at 6h (SLA violated ✗ +4h overage)

### Scenario 3: Mixed Priorities
- 2 emergency, 2 urgent, 1 routine
- 3 technicians (1 HVAC, 1 electrical, 1 multi-skill)
- Emergencies assigned first
- Within urgency: longest waiting jobs first

## Validation Checks

```python
✓ Jobs with estimated_hours <= 0    → REJECTED
✓ Jobs with empty required_skills   → REJECTED
✓ Jobs with negative days_waited    → REJECTED
✓ Jobs with invalid priority        → REJECTED
✓ Jobs missing submitted_hour       → REJECTED
✓ Techs with empty skills           → REJECTED
✓ No technicians provided           → REJECTED
✓ No jobs provided                  → REJECTED
✓ Duplicate job IDs                 → REJECTED
✓ Duplicate tech IDs                → REJECTED
✓ Job requires skills no tech has   → REJECTED
```

## Metrics Explained

### SLA Violations
Count of jobs that were assigned AFTER their SLA window expired.

### Emergency Response Times
- Average: Mean response time for all emergency jobs
- Min: Fastest emergency assignment
- Max: Slowest emergency assignment

### Assignment Rate
Percentage of jobs assigned in each priority category.

## Key Business Rules

1. **Emergency Priority**: AC failures in extreme heat get immediate dispatch
2. **SLA Tracking**: Every missed SLA is logged for management reporting
3. **Skill Matching**: Jobs only assigned to techs with required skills
4. **Workload Fairness**: Time simulation ensures fair tech utilization
5. **Capacity Planning**: Metrics help identify staffing gaps

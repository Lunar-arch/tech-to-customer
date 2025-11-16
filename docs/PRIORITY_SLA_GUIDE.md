# Emergency Priority & SLA Tracking System - Complete Implementation

## Overview
A sophisticated HVAC job scheduling system that prioritizes emergency jobs, tracks SLA compliance, and provides comprehensive validation and error handling.

## Features Implemented

### 1. Priority Levels
- **Emergency** (SLA: 2 hours) - AC failure in extreme heat
- **Urgent** (SLA: 8 hours) - Important but not critical
- **Routine** (SLA: 24 hours) - Standard maintenance

### 2. Job Sorting Logic
```
Highest Priority → Emergency jobs
Middle Priority  → Urgent jobs (by days_waited DESC)
Lowest Priority  → Routine jobs (by days_waited DESC)
```

Within each priority level, jobs are sorted by `days_waited` in descending order (longest waiting first).

### 3. Time Simulation
- Starts at hour 0
- Attempts to assign unassigned jobs to available techs
- Jumps to the next hour when a tech becomes free
- Repeats until all jobs assigned or no progress possible

### 4. SLA Tracking
Each job tracks:
- `submitted_hour`: When the job entered the system
- `start_hour`: When assignment actually occurred
- `sla_met`: Boolean flag (true if assigned within SLA window)

**Response Time Calculation:**
```
response_time = start_hour - submitted_hour
sla_violated = (response_time > SLA_WINDOWS[priority])
```

### 5. Comprehensive Validation
Validates:
- ✓ Non-empty technician and job lists
- ✓ Valid job duration (estimated_hours > 0)
- ✓ Valid priority levels (emergency, urgent, routine)
- ✓ Required fields present and properly typed
- ✓ No duplicate IDs
- ✓ Skills coverage (at least one tech can do each job)
- ✓ No negative days_waited or submitted_hour

### 6. Metrics & Reporting
Output includes:
- Real-time assignment log with SLA indicators
- Final timeline sorted by start time
- SLA performance metrics
- Emergency response time statistics
- Tech availability summary with job assignments

## Sample Data Structure

```python
Job:
{
    "id": 101,
    "required_skills": ["hvac"],
    "days_waited": 2,          # How long waiting (urgency)
    "estimated_hours": 2,      # Duration
    "priority": "emergency",   # emergency | urgent | routine
    "submitted_hour": 0,       # When job entered system
    "assigned": False,         # Has it been assigned?
    "assigned_to": None,       # Tech ID
    "start_hour": None,        # When tech starts work
    "sla_met": None           # SLA compliance
}

Technician:
{
    "id": 1,
    "skills": ["hvac", "plumbing"],
    "free_at_hour": 0,        # When becomes available
    "current_job": None       # Job ID if busy
}
```

## Example Output

```
Hour 0: Tech 3 starts Job 101 (EMERGENCY, 2h, response: 0h/2h ✓)
Hour 0: Tech 2 starts Job 103 (URGENT, 4h, response: 0h/8h ✓)
Hour 2: Tech becomes available...
Hour 2: Tech 3 starts Job 102 (EMERGENCY, 1h, response: 2h/2h ✓)

SLA METRICS:
- Total SLA Violations: 0 job(s)
- Emergency SLA Violations: 0
- Average emergency response: 1.0 hours
```

## Error Handling

All errors collected and reported together (not stopping at first error):
- Invalid priority: "ERROR: Job X has invalid priority 'Y' (must be 'emergency', 'urgent', or 'routine')"
- Missing SLA field: "ERROR: Job X missing submitted_hour"
- Duplicate IDs: "ERROR: Duplicate job ID: X"
- Impossible jobs: "ERROR: Job X requires skills [...] but no tech has these skills"

## Key Design Decisions

1. **Priority Over Urgency**: Emergencies always assigned first, regardless of days_waited
2. **Within-Priority Sorting**: Uses days_waited to fairly distribute urgent/routine jobs
3. **SLA Calculation**: Based on actual assignment time, not completion time
4. **Validation First**: All inputs validated before simulation starts
5. **Comprehensive Metrics**: Tracks emergency-specific performance (critical for SLA audits)

## Usage

```python
# Run the scheduler
python3 matcher.py

# Run validation tests
python3 test_priority_sla.py

# See SLA violation scenarios
python3 demo_sla_violations.py
```

## Customization

Edit these values in matcher.py:

```python
# Adjust SLA windows
SLA_WINDOWS = {
    "emergency": 2,    # Change 2 to any hours
    "urgent": 8,       # Change 8 to any hours
    "routine": 24      # Change 24 to any hours
}

# Add more technicians
technicians = [
    {"id": 4, "skills": ["hvac", "electrical"], "free_at_hour": 0, "current_job": None},
]

# Add more jobs
jobs = [
    {"id": 206, "required_skills": ["hvac"], "days_waited": 1, "estimated_hours": 1.5, 
     "priority": "emergency", "submitted_hour": 0, "assigned": False, "assigned_to": None, 
     "start_hour": None, "sla_met": None},
]
```

## Test Coverage

✓ Priority sorting (emergency > urgent > routine)
✓ Within-priority sorting by days_waited
✓ SLA window enforcement
✓ SLA violation detection
✓ Validation of all fields
✓ Duplicate ID detection
✓ Skill matching requirements
✓ Time simulation with multiple jobs
✓ Error handling and reporting

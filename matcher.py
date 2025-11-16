# Phase 2: Time-simulated weighted matching with workload and urgency
# WITH ROBUST VALIDATION, ERROR HANDLING, PRIORITY LEVELS, AND SLA TRACKING

# Step 1: Define technicians
technicians = [
    {"id": 1, "skills": ["plumbing"], "free_at_hour": 0, "current_job": None},
    {"id": 2, "skills": ["electrical"], "free_at_hour": 0, "current_job": None},
    {"id": 3, "skills": ["plumbing", "electrical", "hvac"], "free_at_hour": 0, "current_job": None}
]

# Step 2: Define jobs with priority levels, SLA, and urgency
jobs = [
    {"id": 100, "required_skills": ["hvac"], "days_waited": 2, "estimated_hours": 2, "priority": "critical", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 101, "required_skills": ["hvac"], "days_waited": 2, "estimated_hours": 2, "priority": "emergency", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 102, "required_skills": ["hvac"], "days_waited": 1, "estimated_hours": 1, "priority": "emergency", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 103, "required_skills": ["electrical"], "days_waited": 5, "estimated_hours": 4, "priority": "urgent", "submitted_hour": 0, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 104, "required_skills": ["plumbing"], "days_waited": 4, "estimated_hours": 3, "priority": "urgent", "submitted_hour": 1, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
    {"id": 105, "required_skills": ["plumbing"], "days_waited": 3, "estimated_hours": 2, "priority": "routine", "submitted_hour": 2, "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None}
]

# Step 3: SLA definitions (in hours)
SLA_WINDOWS = {
    "critical": 1,
    "emergency": 2,
    "urgent": 8,
    "routine": 24
}

# Step 4: Validation function (enhanced with priority validation)
def validate_inputs(technicians, jobs):
    """
    Validate all inputs before simulation.
    Returns: (is_valid: bool, error_messages: list)
    """
    errors = []
    
    # Validate technicians list exists
    if not technicians:
        errors.append("ERROR: No technicians available")
        return False, errors
    
    # Validate each technician
    tech_ids_seen = set()
    for tech in technicians:
        # Check for missing id
        if "id" not in tech:
            errors.append(f"ERROR: Technician missing 'id' field: {tech}")
            continue
        
        tech_id = tech["id"]
        
        # Check for duplicate IDs
        if tech_id in tech_ids_seen:
            errors.append(f"ERROR: Duplicate technician ID: {tech_id}")
        tech_ids_seen.add(tech_id)
        
        # Check for empty skills
        if "skills" not in tech or not tech["skills"]:
            errors.append(f"ERROR: Tech {tech_id} has no skills")
        elif not isinstance(tech["skills"], list):
            errors.append(f"ERROR: Tech {tech_id} skills must be a list")
    
    # Validate jobs list exists
    if not jobs:
        errors.append("ERROR: No jobs provided")
        return len(errors) == 0, errors
    
    # Validate each job
    job_ids_seen = set()
    all_skills_in_jobs = set()
    
    for job in jobs:
        # Check for missing id
        if "id" not in job:
            errors.append(f"ERROR: Job missing 'id' field: {job}")
            continue
        
        job_id = job["id"]
        
        # Check for duplicate IDs
        if job_id in job_ids_seen:
            errors.append(f"ERROR: Duplicate job ID: {job_id}")
        job_ids_seen.add(job_id)
        
        # Check for required_skills
        if "required_skills" not in job or not job["required_skills"]:
            errors.append(f"ERROR: Job {job_id} has no required skills")
        elif not isinstance(job["required_skills"], list):
            errors.append(f"ERROR: Job {job_id} required_skills must be a list")
        else:
            all_skills_in_jobs.update(job["required_skills"])
        
        # Check estimated_hours
        if "estimated_hours" not in job:
            errors.append(f"ERROR: Job {job_id} missing estimated_hours")
        elif not isinstance(job["estimated_hours"], (int, float)) or job["estimated_hours"] <= 0:
            errors.append(f"ERROR: Job {job_id} has invalid duration (must be > 0)")
        
        # Check days_waited
        if "days_waited" not in job:
            errors.append(f"ERROR: Job {job_id} missing days_waited")
        elif not isinstance(job["days_waited"], (int, float)) or job["days_waited"] < 0:
            errors.append(f"ERROR: Job {job_id} has negative wait time")
        
        # Check priority
        if "priority" not in job:
            errors.append(f"ERROR: Job {job_id} missing priority field")
        elif job["priority"] not in ["critical", "emergency", "urgent", "routine"]:
            errors.append(f"ERROR: Job {job_id} has invalid priority '{job['priority']}' (must be 'emergency', 'urgent', or 'routine')")
        
        # Check submitted_hour
        if "submitted_hour" not in job:
            errors.append(f"ERROR: Job {job_id} missing submitted_hour")
        elif not isinstance(job["submitted_hour"], (int, float)) or job["submitted_hour"] < 0:
            errors.append(f"ERROR: Job {job_id} has invalid submitted_hour")
    
    # Check if any tech can do any job
    all_tech_skills = set()
    for tech in technicians:
        if "skills" in tech and tech["skills"]:
            all_tech_skills.update(tech["skills"])
    
    for job in jobs:
        if "required_skills" in job and job["required_skills"]:
            job_skills = set(job["required_skills"])
            if not job_skills.intersection(all_tech_skills):
                errors.append(f"ERROR: Job {job['id']} requires skills {list(job_skills)} but no tech has these skills")
    
    return len(errors) == 0, errors

# Step 5: Function to calculate tech-job match score
def match_score(tech, job):
    skill_match_count = sum(1 for skill in job["required_skills"] if skill in tech["skills"])
    skill_score = skill_match_count / len(job["required_skills"])  # fraction of skills matched
    urgency_score = job["days_waited"] / 5                          # normalize urgency
    total_score = skill_score + urgency_score
    return total_score

# Step 6: Helper function to check if tech has required skills
def can_do_job(tech, job):
    """Check if technician has all required skills"""
    return all(skill in tech["skills"] for skill in job["required_skills"])

# Step 7: Helper function to get SLA window for a job
def get_sla_window(job):
    """Return the SLA window in hours for this job"""
    return SLA_WINDOWS.get(job["priority"], 24)

# Step 8: Helper function to check if job meets SLA
def check_sla_met(job):
    """Check if a job was assigned within its SLA window"""
    if not job["assigned"] or job["start_hour"] is None:
        return False  # Not assigned
    
    assignment_delay = job["start_hour"] - job["submitted_hour"]
    sla_window = get_sla_window(job)
    return assignment_delay <= sla_window

# Step 9: Try to assign unassigned jobs to available techs at given time
def assign_jobs_at_time(current_hour):
    """
    Find unassigned jobs and try to assign them to available techs.
    Prioritizes by: priority level first, then days_waited
    Returns True if any jobs were assigned, False otherwise.
    """
    unassigned = [j for j in jobs if not j["assigned"]]
    if not unassigned:
        return False
    
    # Sort by priority first, then by days_waited
    priority_order = {"critical": 0, "emergency": 1, "urgent": 2, "routine": 3}
    unassigned.sort(key=lambda j: (priority_order.get(j["priority"], 3), -j["days_waited"]))
    
    assigned_this_round = False
    
    for job in unassigned:
        # Find techs that are free at this time
        available_techs = [t for t in technicians if t["free_at_hour"] <= current_hour and can_do_job(t, job)]
        
        if not available_techs:
            continue  # No tech available for this job right now
        
        # Find best tech by match score
        best_tech = max(available_techs, key=lambda t: match_score(t, job))
        
        # Assign the job
        job["assigned"] = True
        job["assigned_to"] = best_tech["id"]
        job["start_hour"] = current_hour
        job["sla_met"] = check_sla_met(job)
        best_tech["current_job"] = job["id"]
        best_tech["free_at_hour"] = current_hour + job["estimated_hours"]
        
        sla_indicator = "✓" if job["sla_met"] else "✗"
        assignment_time = current_hour - job["submitted_hour"]
        sla_window = get_sla_window(job)
        
        print(f"Hour {current_hour}: Tech {best_tech['id']} starts Job {job['id']} "
              f"({job['priority'].upper()}, {job['estimated_hours']}h, "
              f"response: {assignment_time}h/{sla_window}h {sla_indicator})")
        assigned_this_round = True
    
    return assigned_this_round

# Step 10: Main simulation with error handling
def run_simulation():
    """Run the scheduling simulation with comprehensive error handling"""
    print("=" * 80)
    print("EMERGENCY PRIORITY SCHEDULING SYSTEM WITH SLA TRACKING")
    print("=" * 80 + "\n")
    
    # Step 10a: Validate inputs
    print("Validating inputs...\n")
    is_valid, error_messages = validate_inputs(technicians, jobs)
    
    if error_messages:
        print("VALIDATION ERRORS FOUND:\n")
        for error in error_messages:
            print(f"  {error}")
        print()
    
    if not is_valid:
        print("✗ Validation failed. Stopping simulation.\n")
        return False
    
    print("✓ Validation passed\n")
    
    # Step 10b: Run simulation with try/except
    try:
        print("=" * 80)
        print("TIME SIMULATION: Jobs assigned based on priority and tech availability")
        print("=" * 80 + "\n")
        
        current_hour = 0
        max_hours = 100  # Safety limit to prevent infinite loops
        
        while True:
            # Try to assign jobs at current time
            if assign_jobs_at_time(current_hour):
                # Jobs were assigned, continue
                pass
            
            # Check if all jobs are assigned
            if all(j["assigned"] for j in jobs):
                print(f"\n✓ All jobs assigned!")
                break
            
            # Find next time when a tech becomes free
            unassigned = [j for j in jobs if not j["assigned"]]
            if not unassigned:
                break
            
            busy_techs = [t for t in technicians if t["free_at_hour"] > current_hour]
            
            if not busy_techs:
                print(f"\n✗ No techs available for remaining jobs:")
                for job in unassigned:
                    print(f"   - Job {job['id']} ({job['priority']}) requires {job['required_skills']}")
                break
            
            next_free_hour = min(t["free_at_hour"] for t in busy_techs)
            
            if next_free_hour > current_hour:
                print(f"Hour {next_free_hour}: Tech becomes available...")
                current_hour = next_free_hour
            else:
                # Safety break
                break
            
            if current_hour > max_hours:
                print(f"\nReached max simulation hours ({max_hours}). Stopping.")
                break
        
        # Step 10c: Print final results
        print_final_results()
        return True
        
    except Exception as e:
        print(f"\n✗ SIMULATION ERROR: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("\nTraceback:")
        traceback.print_exc()
        return False

# Step 11: Print final timeline, SLA metrics, and summary
def print_final_results():
    """Print final assignment timeline, SLA tracking, and tech summary"""
    print("\n" + "=" * 80)
    print("FINAL ASSIGNMENT TIMELINE")
    print("=" * 80)
    
    for job in sorted(jobs, key=lambda j: j["start_hour"] if j["start_hour"] is not None else float('inf')):
        if job["assigned"]:
            end_hour = job["start_hour"] + job["estimated_hours"]
            response_time = job["start_hour"] - job["submitted_hour"]
            sla_window = get_sla_window(job)
            sla_status = "✓ SLA MET" if job["sla_met"] else "✗ SLA VIOLATED"
            
            print(f"Job {job['id']:>3} ({job['priority'].upper():>9}): "
                  f"Tech {job['assigned_to']} | "
                  f"Hours {job['start_hour']:>2}-{end_hour:<2} | "
                  f"Response: {response_time}h/{sla_window}h | {sla_status}")
        else:
            print(f"Job {job['id']:>3} ({job['priority'].upper():>9}): UNASSIGNED")
    
    # Calculate metrics
    print("\n" + "=" * 80)
    print("SLA AND PRIORITY METRICS")
    print("=" * 80)
    
    emergencies = [j for j in jobs if j["priority"] == "emergency"]
    urgents = [j for j in jobs if j["priority"] == "urgent"]
    routines = [j for j in jobs if j["priority"] == "routine"]
    
    assigned_emergencies = [j for j in emergencies if j["assigned"]]
    assigned_urgents = [j for j in urgents if j["assigned"]]
    assigned_routines = [j for j in routines if j["assigned"]]
    
    sla_violations = [j for j in jobs if j["assigned"] and not j["sla_met"]]
    emergency_violations = [j for j in emergencies if j["assigned"] and not j["sla_met"]]
    
    print(f"\nTotal Jobs: {len(jobs)}")
    print(f"  - Emergency: {len(emergencies)} (SLA: {SLA_WINDOWS['emergency']}h)")
    print(f"  - Urgent:    {len(urgents)} (SLA: {SLA_WINDOWS['urgent']}h)")
    print(f"  - Routine:   {len(routines)} (SLA: {SLA_WINDOWS['routine']}h)")
    
    print(f"\nAssignment Rate:")
    print(f"  - Emergency: {len(assigned_emergencies)}/{len(emergencies)} assigned")
    print(f"  - Urgent:    {len(assigned_urgents)}/{len(urgents)} assigned")
    print(f"  - Routine:   {len(assigned_routines)}/{len(routines)} assigned")
    
    print(f"\nSLA Performance:")
    print(f"  - Total SLA Violations: {len(sla_violations)} job(s)")
    print(f"  - Emergency SLA Violations: {len(emergency_violations)}")
    
    if sla_violations:
        print(f"\nSLA Violation Details:")
        for job in sla_violations:
            response_time = job["start_hour"] - job["submitted_hour"]
            sla_window = get_sla_window(job)
            overage = response_time - sla_window
            print(f"  - Job {job['id']} ({job['priority']}): "
                  f"Response {response_time}h exceeded SLA by {overage}h (SLA: {sla_window}h)")
    
    if assigned_emergencies:
        emergency_response_times = [j["start_hour"] - j["submitted_hour"] for j in assigned_emergencies]
        avg_emergency_response = sum(emergency_response_times) / len(emergency_response_times)
        print(f"\nEmergency Response Times:")
        print(f"  - Average: {avg_emergency_response:.1f} hours")
        print(f"  - Min: {min(emergency_response_times)} hour(s)")
        print(f"  - Max: {max(emergency_response_times)} hour(s)")

    if assigned_urgents:
        urgent_response_times = [j["start_hour"] - j["submitted_hour"] for j in assigned_urgents]
        avg_urgent_response = sum(urgent_response_times) / len(urgent_response_times)
        print(f"\nUrgent Response Times:")
        print(f"  - Average: {avg_urgent_response:.1f} hours")
        print(f"  - Min: {min(urgent_response_times)} hour(s)")
        print(f"  - Max: {max(urgent_response_times)} hour(s)")
        print("\n" + "=" * 80)
        print("TECH AVAILABILITY SUMMARY")
        print("=" * 80)
    
    for tech in technicians:
        assigned_jobs = [j for j in jobs if j["assigned_to"] == tech["id"]]
        total_hours = sum(j["estimated_hours"] for j in assigned_jobs)
        job_list = [f"{j['id']}({j['priority'][0].upper()})" for j in assigned_jobs]
        print(f"Tech {tech['id']}: Free at hour {tech['free_at_hour']} | "
              f"Jobs: {job_list if job_list else 'None'} | "
              f"Total hours: {total_hours}h")

# Step 12: Run the simulation
if __name__ == "__main__":
    run_simulation()

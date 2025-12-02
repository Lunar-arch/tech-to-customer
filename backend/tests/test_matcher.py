import pytest
from matcher import (
    validate_inputs, 
    match_score, 
    can_do_job, 
    get_sla_window, 
    check_sla_met,
    SLA_WINDOWS
)

def test_no_technicians():
    technicians = []
    jobs = [
        {"id": 101, "required_skills": ["plumbing"], "days_waited": 2, 
         "estimated_hours": 3, "priority": "emergency", "submitted_hour": 0,
         "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None}
    ]
    is_valid, errors = validate_inputs(technicians, jobs)
    assert not is_valid
    assert len(errors) > 0
    assert any("No technicians" in err for err in errors)

def test_invalid_job_duration():
    technicians = [{"id": 1, "skills": ["plumbing"], "free_at_hour": 0, "current_job": None}]
    jobs = [
        {"id": 101, "required_skills": ["plumbing"], "days_waited": 2,
         "estimated_hours": 0, "priority": "emergency", "submitted_hour": 0,
         "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None}
    ]
    is_valid, errors = validate_inputs(technicians, jobs)
    assert not is_valid
    assert any("invalid duration" in err for err in errors)

def test_invalid_priority():
    technicians = [{"id": 1, "skills": ["plumbing"], "free_at_hour": 0, "current_job": None}]
    jobs = [
        {"id": 101, "required_skills": ["plumbing"], "days_waited": 2,
         "estimated_hours": 3, "priority": "super_urgent", "submitted_hour": 0,
         "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None}
    ]
    is_valid, errors = validate_inputs(technicians, jobs)
    assert not is_valid
    assert any("invalid priority" in err for err in errors)

def test_match_score_perfect():
    tech = {"id": 1, "skills": ["plumbing", "electrical", "hvac"], "free_at_hour": 0, "current_job": None}
    job = {"id": 101, "required_skills": ["plumbing", "electrical"], "days_waited": 5, "estimated_hours": 3, "priority": "emergency", "submitted_hour": 0}
    score = match_score(tech, job)
    assert score == 2.0

def test_match_score_partial():
    tech = {"id": 1, "skills": ["plumbing"], "free_at_hour": 0, "current_job": None}
    job = {"id": 101, "required_skills": ["plumbing", "electrical"], "days_waited": 5, "estimated_hours": 3, "priority": "emergency", "submitted_hour": 0}
    score = match_score(tech, job)
    assert score == 1.5

def test_can_do_job_yes():
    tech = {"id": 1, "skills": ["plumbing", "electrical", "hvac"]}
    job = {"required_skills": ["plumbing", "electrical"]}
    assert can_do_job(tech, job) is True

def test_can_do_job_no():
    tech = {"id": 1, "skills": ["plumbing"]}
    job = {"required_skills": ["plumbing", "electrical"]}
    assert can_do_job(tech, job) is False

def test_sla_windows():
    assert SLA_WINDOWS["critical"] == 1
    assert SLA_WINDOWS["emergency"] == 2
    assert SLA_WINDOWS["urgent"] == 8
    assert SLA_WINDOWS["routine"] == 24

def test_get_sla_window():
    emergency_job = {"priority": "emergency"}
    urgent_job = {"priority": "urgent"}
    routine_job = {"priority": "routine"}
    assert get_sla_window(emergency_job) == 2
    assert get_sla_window(urgent_job) == 8
    assert get_sla_window(routine_job) == 24

def test_sla_met_within_window():
    job = {"priority": "emergency", "submitted_hour": 0, "start_hour": 1, "assigned": True}
    assert check_sla_met(job) is True

def test_sla_violated_outside_window():
    job = {"priority": "emergency", "submitted_hour": 0, "start_hour": 3, "assigned": True}
    assert check_sla_met(job) is False

def test_valid_data():
    technicians = [
        {"id": 1, "skills": ["plumbing"], "free_at_hour": 0, "current_job": None},
        {"id": 2, "skills": ["electrical"], "free_at_hour": 0, "current_job": None}
    ]
    jobs = [
        {"id": 101, "required_skills": ["plumbing"], "days_waited": 2,
         "estimated_hours": 3, "priority": "emergency", "submitted_hour": 0,
         "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None},
        {"id": 102, "required_skills": ["electrical"], "days_waited": 5,
         "estimated_hours": 4, "priority": "urgent", "submitted_hour": 0,
         "assigned": False, "assigned_to": None, "start_hour": None, "sla_met": None}
    ]
    is_valid, errors = validate_inputs(technicians, jobs)
    assert is_valid
    assert len(errors) == 0
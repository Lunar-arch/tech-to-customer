from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Any
import matcher
import io
import sys

app = FastAPI(title="HVAC Scheduler API", version="1.0.0")

class Technician(BaseModel):
    id: int
    skills: List[str]
    free_at_hour: int = 0
    current_job: Any = None

class Job(BaseModel):
    id: int
    required_skills: List[str]
    days_waited: int
    estimated_hours: int
    priority: str
    submitted_hour: int
    assigned: bool = False
    assigned_to: Any = None
    start_hour: Any = None
    sla_met: Any = None

class ScheduleRequest(BaseModel):
    technicians: List[Technician]
    jobs: List[Job]

@app.get("/")
def read_root():
    return {"message": "HVAC Scheduler API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/schedule")
def create_schedule(request: ScheduleRequest):
    # Capture print output from matcher.py
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    try:
        # Convert Pydantic models to dicts
        techs = [t.dict() for t in request.technicians]
        jobs_list = [j.dict() for j in request.jobs]
        
        # Update matcher.py's global variables
        matcher.technicians = techs
        matcher.jobs = jobs_list
        
        # Run the simulation
        success = matcher.run_simulation()
        
        # Get the output
        output = buffer.getvalue()
        
        # Return the results
        return {
            "success": success,
            "output": output,
            "technicians": matcher.technicians,
            "jobs": matcher.jobs
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": buffer.getvalue()
        }
    
    finally:
        # Restore stdout
        sys.stdout = old_stdout
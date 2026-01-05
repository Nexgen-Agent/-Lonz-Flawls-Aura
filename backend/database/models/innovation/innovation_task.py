# backend/database/models/innovation/innovation_task.py

from datetime import datetime
from typing import Optional, Dict, Any

class InnovationTask:
    """
    Represents a single task associated with an innovation proposal.

    This model breaks down a proposal into actionable steps, tracking their
    status, assignment, and outcomes.
    """
    def __init__(
        self,
        proposal_id: str,
        description: str,
        task_id: Optional[str] = None,
        status: str = "pending",
        assignee: Optional[str] = None,
        due_date: Optional[datetime] = None,
        results: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Initializes an InnovationTask instance.

        Args:
            task_id (Optional[str]): The unique identifier for the task.
            proposal_id (str): The ID of the parent innovation proposal.
            description (str): A description of the task.
            status (str): The current status (e.g., pending, assigned, in_progress, completed).
            assignee (Optional[str]): The person or team responsible for the task.
            due_date (Optional[datetime]): The target completion date.
            results (Optional[Dict[str, Any]]): The outcome or deliverables of the task.
            created_at (Optional[datetime]): Timestamp of creation.
            updated_at (Optional[datetime]): Timestamp of last update.
        """
        self.task_id = task_id
        self.proposal_id = proposal_id
        self.description = description
        self.status = status
        self.assignee = assignee
        self.due_date = due_date
        self.results = results or {}
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the task object to a dictionary."""
        return {
            "task_id": self.task_id,
            "proposal_id": self.proposal_id,
            "description": self.description,
            "status": self.status,
            "assignee": self.assignee,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "results": self.results,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

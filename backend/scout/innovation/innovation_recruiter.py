# backend/scout/innovation/innovation_recruiter.py

from typing import List, Dict, Any

class InnovationRecruiter:
    """
    A specialized recruiter for sourcing talent for innovation projects.

    This module interfaces with the broader 'scout' domain to identify and vet
    candidates (internal or external) with the skills required for approved

    innovation proposals.
    """

    def __init__(self, talent_pool_connector: Any, task_manager_api: Any):
        """
        Initializes the InnovationRecruiter.

        Args:
            talent_pool_connector: A connector to the main talent pool database.
            task_manager_api: An API client for the InnovationTaskManager.
        """
        self.talent_pool = talent_pool_connector
        self.task_manager_api = task_manager_api

    def find_talent_for_proposal(self, proposal_id: str) -> List[Dict[str, Any]]:
        """
        Identifies suitable talent for all tasks within a given proposal.

        Args:
            proposal_id (str): The ID of the innovation proposal.

        Returns:
            A list of candidate profiles suited for the proposal's tasks.
        """
        tasks = self.task_manager_api.get_all_tasks_for_proposal(proposal_id)
        required_skills = self._extract_skills_from_tasks(tasks)

        print(f"Searching for candidates with skills: {required_skills}")
        # In a real system, this would query a database of talent
        # candidates = self.talent_pool.search_by_skills(required_skills)
        candidates = [
            {"name": "Jane Doe", "skills": ["Python", "AI", "UX Design"]},
            {"name": "John Smith", "skills": ["Data Science", "React", "DevOps"]},
        ]
        return candidates

    def _extract_skills_from_tasks(self, tasks: List[Dict[str, Any]]) -> List[str]:
        """A simple helper to parse required skills from task descriptions."""
        skills = set()
        for task in tasks:
            # This is a placeholder for a more sophisticated skill extraction logic
            if "prototype" in task.get("details", {}).get("name", "").lower():
                skills.add("UX Design")
                skills.add("React")
            if "ai" in task.get("details", {}).get("name", "").lower():
                skills.add("Python")
                skills.add("AI")
        return list(skills)

    def assign_candidate_to_task(self, candidate_id: str, task_id: str) -> bool:
        """
        Assigns a vetted candidate to a specific innovation task.

        Args:
            candidate_id: The ID of the candidate.
            task_id: The ID of the task.

        Returns:
            True if the assignment is successful, False otherwise.
        """
        print(f"Assigning candidate {candidate_id} to task {task_id}")
        return self.task_manager_api.assign_task(task_id, candidate_id)

# backend/ai/innovation/innovation_task_manager.py

from typing import Dict, Any, List

import uuid

class InnovationTaskManager:
    """
    Manages the lifecycle of innovation tasks, from creation to completion.
    This includes creating, assigning, tracking, and reporting on tasks.
    """

    def __init__(self, db_connection: Any):
        """
        Initializes the InnovationTaskManager.

        Args:
            db_connection (Any): A database connection object.
        """
        self.db_connection = db_connection
        self.collection = self.db_connection.tasks

    def create_task(self, proposal_id: str, task_details: Dict[str, Any]) -> str:
        """
        Creates a new innovation task based on a proposal.

        Args:
            proposal_id (str): The ID of the parent innovation proposal.
            task_details (Dict[str, Any]): Details of the task to be created.

        Returns:
            str: The ID of the newly created task.
        """
        task_id = str(uuid.uuid4())
        task = {
            "_id": task_id,
            "proposal_id": proposal_id,
            "details": task_details,
            "status": "pending",
            "assignee": None,
        }
        self.collection.insert_one(task)
        print(f"Created task {task_id} for proposal {proposal_id}")
        return task_id

    def assign_task(self, task_id: str, assignee: str) -> bool:
        """
        Assigns a task to a specific team or individual.

        Args:
            task_id (str): The ID of the task to assign.
            assignee (str): The identifier of the assignee.

        Returns:
            bool: True if assignment is successful, False otherwise.
        """
        result = self.collection.update_one(
            {"_id": task_id},
            {"$set": {"assignee": assignee, "status": "assigned"}}
        )
        if result.modified_count == 1:
            print(f"Assigned task {task_id} to {assignee}")
            return True
        return False

    def track_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Tracks the status of a specific innovation task.

        Args:
            task_id (str): The ID of the task to track.

        Returns:
            Dict[str, Any]: A dictionary containing the task's status and details.
        """
        task = self.collection.find_one({"_id": task_id})
        return task or {"error": "Task not found"}

    def complete_task(self, task_id: str, results: Dict[str, Any]) -> bool:
        """
        Marks a task as complete and records the results.

        Args:
            task_id (str): The ID of the task to complete.
            results (Dict[str, Any]): The results or outcomes of the task.

        Returns:
            bool: True if completion is successful, False otherwise.
        """
        result = self.collection.update_one(
            {"_id": task_id},
            {"$set": {"status": "completed", "results": results}}
        )
        if result.modified_count == 1:
            print(f"Completed task {task_id}")
            return True
        return False

    def get_all_tasks_for_proposal(self, proposal_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks associated with a given proposal.

        Args:
            proposal_id (str): The ID of the proposal.

        Returns:
            List[Dict[str, Any]]: A list of tasks for the proposal.
        """
        return list(self.collection.find({"proposal_id": proposal_id}))

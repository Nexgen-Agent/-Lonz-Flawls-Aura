# backend/services/innovation_service.py

from typing import Dict, Any, List
from backend.ai.innovation import AutonomousInnovationEngine, InnovationTaskManager
from backend.database.models.innovation import InnovationProposal
from backend.core.private_ledger import PrivateLedger

class InnovationService:
    """
    Orchestrates the innovation process, from opportunity identification to task management.

    This service integrates the AutonomousInnovationEngine and InnovationTaskManager
    to provide a cohesive workflow for creating, approving, and executing on
    innovation proposals.
    """

    def __init__(self, config: Dict[str, Any], db_connection: Any, private_ledger: PrivateLedger):
        """
        Initializes the InnovationService.

        Args:
            config (Dict[str, Any]): Application configuration.
            db_connection (Any): Database connection object.
        """
        self.config = config
        self.db_connection = db_connection
        self.proposals_collection = db_connection.proposals
        self.innovation_engine = AutonomousInnovationEngine(config)
        self.task_manager = InnovationTaskManager(db_connection)
        self.private_ledger = private_ledger

    def find_and_propose_innovations(self) -> List[Dict[str, Any]]:
        """
        Runs the full cycle of identifying opportunities and generating proposals.

        Returns:
            List[Dict[str, Any]]: A list of newly created innovation proposals.
        """
        opportunities = self.innovation_engine.identify_innovation_opportunities()
        new_proposals = []
        for opportunity in opportunities:
            proposal_data = self.innovation_engine.generate_innovation_proposal(opportunity)
            proposal = InnovationProposal(**proposal_data)
            # Generate a unique ID for the proposal before saving
            proposal.proposal_id = f"prop-{self.proposals_collection.count_documents({}) + 1}"
            self.proposals_collection.insert_one(proposal.to_dict())
            new_proposals.append(proposal.to_dict())
        return new_proposals

    def get_proposal_details(self, proposal_id: str) -> Dict[str, Any]:
        """
        Retrieves the details of a specific innovation proposal.

        Args:
            proposal_id (str): The ID of the proposal to retrieve.

        Returns:
            Dict[str, Any]: The details of the proposal.
        """
        proposal = self.proposals_collection.find_one({"proposal_id": proposal_id})
        return proposal or {"error": "Proposal not found"}

    def approve_proposal(self, proposal_id: str) -> bool:
        """
        Approves an innovation proposal and initiates task creation.

        Args:
            proposal_id (str): The ID of the proposal to approve.

        Returns:
            bool: True if approval was successful, False otherwise.
        """
        # 1. Update proposal status in the database
        result = self.proposals_collection.update_one(
            {"proposal_id": proposal_id},
            {"$set": {"status": "approved"}}
        )
        if result.modified_count == 0:
            print(f"Failed to approve proposal {proposal_id}. Not found or no change.")
            return False

        # 2. Log the approval event in the PrivateLedger
        self.private_ledger.add_entry(
            domain="innovation",
            event_type="PROPOSAL_APPROVED",
            details={"proposal_id": proposal_id}
        )

        # 3. Create initial tasks using the InnovationTaskManager
        print(f"Approving proposal {proposal_id} and creating initial tasks.")
        tasks = [
            {"name": "Project Kick-off Meeting", "priority": "high"},
            {"name": "Develop Technical Specification", "priority": "high"},
            {"name": "Create UX/UI Mockups", "priority": "medium"},
        ]
        for task_details in tasks:
            self.task_manager.create_task(proposal_id, task_details)

        return True

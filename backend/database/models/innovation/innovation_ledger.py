# backend/database/models/innovation/innovation_ledger.py

from datetime import datetime
from typing import Optional, Dict, Any

class InnovationLedger:
    """
    Represents an entry in the innovation ledger.

    This model provides an immutable, auditable record of significant events
    in the innovation lifecycle, such as proposal approvals, task completions,
    and value realization. It links to the core private ledger.
    """
    def __init__(
        self,
        entry_id: Optional[str],
        proposal_id: str,
        event_type: str,
        event_details: Dict[str, Any],
        recorded_at: Optional[datetime] = None,
        related_transaction_id: Optional[str] = None
    ):
        """
        Initializes an InnovationLedger entry.

        Args:
            entry_id (Optional[str]): The unique identifier for the ledger entry.
            proposal_id (str): The innovation proposal this entry relates to.
            event_type (str): The type of event (e.g., 'PROPOSAL_APPROVED', 'TASK_COMPLETED', 'REVENUE_IMPACT').
            event_details (Dict[str, Any]): A dictionary containing details of the event.
            recorded_at (Optional[datetime]): The timestamp when the event was recorded.
            related_transaction_id (Optional[str]): An ID linking to a financial transaction.
        """
        self.entry_id = entry_id
        self.proposal_id = proposal_id
        self.event_type = event_type
        self.event_details = event_details
        self.recorded_at = recorded_at or datetime.utcnow()
        self.related_transaction_id = related_transaction_id

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the ledger entry to a dictionary."""
        return {
            "entry_id": self.entry_id,
            "proposal_id": self.proposal_id,
            "event_type": self.event_type,
            "event_details": self.event_details,
            "recorded_at": self.recorded_at.isoformat(),
            "related_transaction_id": self.related_transaction_id,
        }

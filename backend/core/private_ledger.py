# backend/core/private_ledger.py

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class PrivateLedger:
    """
    Provides a secure, append-only ledger for critical system events.

    This core service is designed to create a tamper-resistant audit trail.
    Each entry is cryptographically hashed and linked to the previous entry,
    forming a blockchain-like structure. It is the foundation for domain-specific
    ledgers like the InnovationLedger.
    """

    def __init__(self, db_connection: Any):
        """
        Initializes the PrivateLedger.

        Args:
            db_connection: A database connection to a collection/table for ledger entries.
        """
        self.db_connection = db_connection
        self.collection = self.db_connection.ledger
        if self.collection.count_documents({}) == 0:
            self._create_genesis_block()

    def _create_genesis_block(self):
        """Creates the very first block in the chain."""
        genesis_block = self._create_block(
            domain="system",
            event_type="LEDGER_INITIALIZED",
            details={"message": "Ledger created"},
            previous_hash="0"
        )
        self.collection.insert_one(genesis_block)

    def _hash_block(self, block: Dict[str, Any]) -> str:
        """Hashes a block to create a unique fingerprint."""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def _get_last_hash(self) -> str:
        """Returns the hash of the most recent block in the chain."""
        last_entry = self.collection.find_one(sort=[("timestamp", -1)])
        if not last_entry:
            return "0"
        return last_entry["hash"]

    def _create_block(
        self,
        domain: str,
        event_type: str,
        details: Dict[str, Any],
        previous_hash: str
    ) -> Dict[str, Any]:
        """Creates a new block for the ledger."""
        block = {
            "timestamp": datetime.utcnow().isoformat(),
            "domain": domain,
            "event_type": event_type,
            "details": details,
            "previous_hash": previous_hash,
        }
        block["hash"] = self._hash_block(block)
        return block

    def add_entry(
        self,
        domain: str,
        event_type: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adds a new, verified entry to the ledger.

        Args:
            domain: The domain originating the event (e.g., 'innovation', 'finance').
            event_type: The specific type of event.
            details: A dictionary containing event data.

        Returns:
            The newly created block.
        """
        previous_hash = self._get_last_hash()
        new_block = self._create_block(domain, event_type, details, previous_hash)

        self.collection.insert_one(new_block)

        print(f"Added new block to ledger: {new_block['hash']} (Domain: {domain})")
        return new_block

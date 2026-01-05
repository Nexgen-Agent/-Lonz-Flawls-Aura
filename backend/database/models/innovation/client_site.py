# backend/database/models/innovation/client_site.py

from datetime import datetime
from typing import Optional, Dict, Any

class ClientSite:
    """
    Represents a client website or application endpoint.

    This model stores information about the platforms where innovations
    can be deployed, tested, or monitored. It is managed by the SiteRegistryService.
    """
    def __init__(
        self,
        url: str,
        name: str,
        site_id: Optional[str] = None,
        description: Optional[str] = None,
        is_active: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Initializes a ClientSite instance.

        Args:
            site_id (Optional[str]): The unique identifier for the site.
            url (str): The primary URL of the client site or platform.
            name (str): A human-readable name for the site.
            description (Optional[str]): A brief description of the site's purpose.
            is_active (bool): Whether the site is currently active for deployments.
            metadata (Optional[Dict[str, Any]]): A dictionary for storing extra info.
            created_at (Optional[datetime]): Timestamp of creation.
            updated_at (Optional[datetime]): Timestamp of last update.
        """
        self.site_id = site_id
        self.url = url
        self.name = name
        self.description = description
        self.is_active = is_active
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the client site object to a dictionary."""
        return {
            "site_id": self.site_id,
            "url": self.url,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

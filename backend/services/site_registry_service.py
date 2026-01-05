# backend/services/site_registry_service.py

from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.database.models.innovation import ClientSite

import uuid

class SiteRegistryService:
    """
    Manages the registration and lifecycle of client sites for innovation deployment.

    This service provides a centralized way to track and manage the websites,
    applications, and platforms where innovations can be tested and deployed.
    """

    def __init__(self, db_connection: Any):
        """
        Initializes the SiteRegistryService.

        Args:
            db_connection (Any): A database connection object.
        """
        self.db_connection = db_connection
        self.collection = self.db_connection.sites

    def register_site(self, name: str, url: str, description: Optional[str] = None) -> str:
        """
        Registers a new client site in the system.

        Args:
            name (str): A human-readable name for the site.
            url (str): The primary URL of the site.
            description (Optional[str]): A brief description of the site.

        Returns:
            str: The ID of the newly registered site.
        """
        site_id = str(uuid.uuid4())
        new_site = ClientSite(
            site_id=site_id,
            name=name,
            url=url,
            description=description,
            is_active=True
        )
        self.collection.insert_one(new_site.to_dict())
        print(f"Registered new site: {name} ({url}) with ID {site_id}")
        return site_id

    def get_site_details(self, site_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the details of a specific registered site.

        Args:
            site_id (str): The ID of the site to retrieve.

        Returns:
            Optional[Dict[str, Any]]: The details of the site, or None if not found.
        """
        site_data = self.collection.find_one({"site_id": site_id})
        return site_data

    def update_site_status(self, site_id: str, is_active: bool) -> bool:
        """
        Updates the active status of a site.

        Args:
            site_id (str): The ID of the site to update.
            is_active (bool): The new active status.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        result = self.collection.update_one(
            {"site_id": site_id},
            {"$set": {"is_active": is_active, "updated_at": datetime.utcnow().isoformat()}}
        )
        if result.modified_count == 1:
            print(f"Updated status for site {site_id} to is_active={is_active}")
            return True
        return False

    def list_active_sites(self) -> List[Dict[str, Any]]:
        """
        Lists all currently active sites.

        Returns:
            List[Dict[str, Any]]: A list of active client sites.
        """
        return list(self.collection.find({"is_active": True}))

import os
import requests

class JulesAPIClient:
    """
    Client for interacting with the Jules API.
    """

    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.jules_api_key = os.getenv("JULES_API_KEY")

    def dispatch(self, task_data):
        """
        Dispatches a task. Falls back to GitHub if direct API is not configured.
        """
        if os.getenv("JULES_API_KEY"):
            return self.dispatch_direct(task_data)
        return self.dispatch_github(task_data)

    def dispatch_direct(self, task_data):
        """
        Posts the task directly to Jules API.
        """
        api_key = os.getenv("JULES_API_KEY")
        if not api_key:
            return self.dispatch_github(task_data)

        url = "https://jules.google.com/api/v1/tasks"
        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            response = requests.post(url, json=task_data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Direct dispatch failed: {e}. Falling back to GitHub.")
            return self.dispatch_github(task_data)

    def dispatch_github(self, task_data):
        """
        Dispatches a task via GitHub issues.
        """
        print(f"Dispatching task via GitHub: {task_data}")
        # In a real app, this would use the GitHub API
        return {"status": "success", "method": "github"}

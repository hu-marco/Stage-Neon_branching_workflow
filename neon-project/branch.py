import requests
import os
from dotenv import load_dotenv
import time
import subprocess

load_dotenv()
BASE_URL = "https://console.neon.tech/api/v2"
database_name = os.environ["DATABASE_NAME"]
role_name = os.environ["DATABASE_ROLE"]

class NeonClient:
    def __init__(self, api_key: str, project_id: str):
        self.project_id = project_id

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def create_branch(
        self,
        name: str,
        parent_id: str | None = None,
    ) -> dict:
        url = f"{BASE_URL}/projects/{self.project_id}/branches"

        branch = {
            "name": name,
        }

        if parent_id:
            branch["parent_id"] = parent_id

        payload = {
            "branch": branch,
            "endpoints": [
                {
                    "type": "read_write",
                }
            ],
        }

        response = self.session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        operation_id = next(
            op["id"]
            for op in data["operations"]
            if op["action"] == "create_branch"
        )
        self.wait_for_operation(operation_id)
        
        return data

    def get_connection_uri(
        self,
        branch_id: str,
        database_name: str,
        role_name: str,
        pooled: bool = False,
    ) -> str:
        url = (
            f"{BASE_URL}/projects/"
            f"{self.project_id}/connection_uri"
        )

        params = {
            "branch_id": branch_id,
            "database_name": database_name,
            "role_name": role_name,
            "pooled": str(pooled).lower(),
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()

        return response.json()["uri"]

    def wait_for_operation(
        self,
        operation_id: str,
        timeout: int = 120,
        ):
        url = (
            f"{BASE_URL}"
            f"/projects/{self.project_id}"
            f"/operations/{operation_id}"
        )

        start = time.time()

        while True:
            response = self.session.get(url)
            response.raise_for_status()

            operation = response.json()["operation"]

            status = operation["status"]

            if status == "finished":
                return operation

            if status == "failed":
                raise RuntimeError(
                    f"Neon operation failed: {operation}"
                )

            if time.time() - start > timeout:
                raise TimeoutError(
                    "Timeout waiting for Neon operation"
                )

            time.sleep(2)
            
    def delete_branch(
        self,
        branch_id: str,
        hard_delete: bool = False,
        ):
        url = (
            f"{BASE_URL}"
            f"/projects/{self.project_id}"
            f"/branches/{branch_id}"
        )

        params = {
            "hard_delete": str(hard_delete).lower()
        }

        response = self.session.delete(
            url,
            params=params,
        )

        response.raise_for_status()
        
    def run_migrations(self, revision:str ,database_url: str):
        env = os.environ.copy()
        env["DATABASE_URL"] = database_url
        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        
        
        subprocess.run(
        ["alembic", "upgrade", revision],
        env=env,
        cwd=project_dir,
        check=True,
        )
   
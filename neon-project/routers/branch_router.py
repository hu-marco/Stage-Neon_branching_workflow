from fastapi import APIRouter, Depends
from dotenv import load_dotenv
import os

from branch import NeonClient

router = APIRouter()

load_dotenv()

NEON_API_KEY = os.environ["NEON_API_KEY"]
NEON_PROJECT_ID = os.environ["NEON_PROJECT_ID"]

@router.post("/create_branch")
def create_branch():
    client = NeonClient(
    api_key=NEON_API_KEY,
    project_id=NEON_PROJECT_ID,
    )

    result = client.create_branch(
        name="preview-pr-123"
    )
    branch = result["branch"]

    print("Branch:", branch["name"])
    print("Branch ID:", branch["id"])
   
    print(result)
    return branch


@router.post("/delete_branch")
def delete_branch():
    client = NeonClient(
    api_key=NEON_API_KEY,
    project_id=NEON_PROJECT_ID,
    )

    client.delete_branch(
        branch_id="br-weathered-water-abit6t59"
    )
    return {"Status":" complete" }


import os

from branch import NeonClient

def get_client() -> NeonClient:
    return NeonClient(
        api_key=os.environ["NEON_API_KEY"],
        project_id=os.environ["NEON_PROJECT_ID"],
    )


def create_database() -> str:
    client = get_client()

    pr_number = os.environ["PR_NUMBER"]

    branch = client.create_branch(
        name=f"preview-pr-{pr_number}",
    )
    branch_id = branch["branch"]["id"]

    database_url = client.get_connection_uri(
        branch_id=branch_id,
        database_name=os.environ["DATABASE_NAME"],
        role_name=os.environ["DATABASE_ROLE"],
        pooled=False,
    )

    github_env = os.environ.get("GITHUB_ENV")

    if not github_env:
        raise RuntimeError("GITHUB_ENV is not available")

    with open(github_env, "a") as f:
        f.write(f"NEON_BRANCH_ID={branch_id}\n")
        f.write(f"DATABASE_URL={database_url}\n")

    return branch_id
    
def run_migrations(revision):
    client = get_client()

    client.run_migrations(
        revision=revision,
        database_url=os.environ["DATABASE_URL"],
    )


def cleanup_database():
    branch_id = os.environ.get("NEON_BRANCH_ID")

    if not branch_id:
        return

    client = get_client()

    client.delete_branch(
        branch_id=branch_id,
    )
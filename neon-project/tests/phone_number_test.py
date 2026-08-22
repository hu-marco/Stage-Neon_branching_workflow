from fastapi.testclient import TestClient
from sqlalchemy import inspect
import sqlalchemy as sa
from dotenv import load_dotenv
from models import Order
import os
from decimal import Decimal


from main import app
from branch import NeonClient
import database as db


client = TestClient(app)


load_dotenv()
database_name = os.environ["DATABASE_NAME"]
role_name = os.environ["DATABASE_ROLE"]
NEON_API_KEY = os.environ["NEON_API_KEY"]
NEON_PROJECT_ID = os.environ["NEON_PROJECT_ID"]

def test_phone_number_present():
    test_session = db.create_session(os.environ["DATABASE_URL"])
    
    def override_get_db(test_session):
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db.get_db] = override_get_db
    session = test_session()
    try:
        inspector = inspect(session.bind)
        columns = inspector.get_columns("users")
        column_names = [column["name"] for column in columns]
        assert "phone_number" in column_names
    finally:
        app.dependency_overrides.clear()


def test_product_review_not_present():
    test_session = db.create_session(os.environ["DATABASE_URL"])
    
    def override_get_db(test_session):
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db.get_db] = override_get_db
    session = test_session()
    try:
        inspector = inspect(session.bind)
        columns = inspector.get_columns("products")
        column_names = [column["name"] for column in columns]
        assert "product_review" not in column_names
    finally:
        app.dependency_overrides.clear() 
"""
def test_simulation():
    neon_client = NeonClient(
    api_key=NEON_API_KEY,
    project_id=NEON_PROJECT_ID,
    )

    branch = neon_client.create_branch(
        name="preview-pr-123",
    )

    branch_id = branch["branch"]["id"]

    database_url = neon_client.get_connection_uri(
        branch_id=branch_id,
        database_name=database_name,
        role_name=role_name,
    )

    neon_client.run_migrations("f82eff2b844f", database_url)
    
    test_session = db.create_session(database_url)

    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db.get_db] = override_get_db
    session = test_session()
    
    try:
        
    finally:
        app.dependency_overrides.clear()
        neon_client.delete_branch(branch_id)
"""
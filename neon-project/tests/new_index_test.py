from fastapi.testclient import TestClient
from sqlalchemy import inspect, text , select
from dotenv import load_dotenv
import os

from main import app
from branch import NeonClient
import database as db

load_dotenv()

client = TestClient(app)

database_name = os.environ["DATABASE_NAME"]
role_name = os.environ["DATABASE_ROLE"]
NEON_API_KEY = os.environ["NEON_API_KEY"]
NEON_PROJECT_ID = os.environ["NEON_PROJECT_ID"]

def test_orders_created_index():
    test_session = db.create_session(os.environ["DATABASE_URL"])
    
    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[db.get_db] = override_get_db
    session = test_session()
    try:
        inspector = inspect(session.bind)

        indexes = inspector.get_indexes("orders")

        assert any(
            index["name"] == "idx_orders_created"
            for index in indexes
        )
    finally:
        app.dependency_overrides.clear()
        
def test_orders_created_uses_index():
    test_session = db.create_session(os.environ["DATABASE_URL"])
    
    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[db.get_db] = override_get_db
    session = test_session()
    try:
        
        result = session.execute(
            text("""
                EXPLAIN
                SELECT *
                FROM orders
                WHERE created_at >= '2026-01-01'
            """)
        )

        plan = "\n".join(row[0] for row in result)

        assert "idx_orders_created" in plan
    finally:
        app.dependency_overrides.clear()    


# Test the API, need to write the router
def test_get_orders_by_date():
    test_session = db.create_session(os.environ["DATABASE_URL"])
    
    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[db.get_db] = override_get_db
    try:
        response = client.get(
            "/orders/get_orders_by_date?created_at_from=2026-01-01"
        )
        assert response.status_code == 200

        data = response.json()

        assert all(
            order["created_at"] >= "2026-01-01"
            for order in data
        )
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

    neon_client.run_migrations("2f133e768707", database_url)
    
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
        response = client.get(
            "/get_orders_by_date?created_at_from=2026-01-01"
        )
        assert response.status_code == 200

        data = response.json()

        assert all(
            order["created_at"] >= "2026-01-01"
            for order in data
        )
    
        inspector = inspect(session.bind)
        indexes = inspector.get_indexes("orders")

        assert any(
            index["name"] == "idx_orders_created"
            for index in indexes
        )
        result = session.execute(
            text(
                EXPLAIN
                SELECT *
                FROM orders
                WHERE created_at >= '2026-01-01'
            )
        )

        plan = "\n".join(row[0] for row in result)

        assert "idx_orders_created" in plan
        
    finally:
        app.dependency_overrides.clear()
        neon_client.delete_branch(branch_id)
        """
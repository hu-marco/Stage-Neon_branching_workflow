from fastapi.testclient import TestClient
from sqlalchemy import inspect, text
from dotenv import load_dotenv
import os

from main import app
from branch import NeonClient
import database as db

load_dotenv()

client = TestClient(app)

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
        
        result = db.execute(
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
            "/get_orders_by_date?created_at_from=2026-01-01"
        )
        assert response.status_code == 200

        data = response.json()

        assert all(
            order["created_at"] >= "2026-01-01"
            for order in data
        )
    finally:
        app.dependency_overrides.clear()    
        
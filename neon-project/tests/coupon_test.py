from fastapi.testclient import TestClient
from sqlalchemy import inspect
from dotenv import load_dotenv
from models import Order
import os


from main import app
from branch import NeonClient
import database as db


client = TestClient(app)


load_dotenv()
database_name = os.environ["DATABASE_NAME"]
role_name = os.environ["DATABASE_ROLE"]
NEON_API_KEY = os.environ["NEON_API_KEY"]
NEON_PROJECT_ID = os.environ["NEON_PROJECT_ID"]

def test_create_coupon():
    test_session = db.create_session(os.environ["DATABASE_URL"])
    
    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[db.get_db] = override_get_db
    
    try:
        response = client.post(
            "/create_coupon",
            json={
                "code": "WELCOME10",
                "discount": 10
            }
        )

        assert response.status_code == 200

    finally:
        app.dependency_overrides.clear()


def test_coupon_code_present():
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
        columns = inspector.get_columns("orders")
        column_names = [column["name"] for column in columns]
        assert "coupon_id" in column_names
    finally:
        app.dependency_overrides.clear()


def test_coupon_code_populated():

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
        order = (
            session.query(Order)
            .filter(Order.id < 100)
            .first()
        )
        assert order is not None
        assert order.coupon_id == "1"
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

    neon_client.run_migrations("head", database_url)
    
    test_session = db.create_session(database_url)

    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db.get_db] = override_get_db
    session = test_session()
    
    client = TestClient(app)
    try:
        response = client.post(
            "/create_coupon",
            json={
                "code": "WELCOME10",
                "discount": 10
            }
        )
        
        assert response.status_code == 200
    
        inspector = inspect(session.bind)
        columns = inspector.get_columns("orders")
        column_names = [column["name"] for column in columns]
        assert "coupon_id" in column_names
        
        order = (
            session.query(Order)
            .filter(Order.total > 100)
            .first()
        )
        assert order is not None
        assert order.coupon_id == "1"

    finally:
        app.dependency_overrides.clear()
        neon_client.delete_branch(branch_id)
"""
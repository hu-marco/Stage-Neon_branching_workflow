from fastapi.testclient import TestClient
from sqlalchemy import inspect
import sqlalchemy as sa
from dotenv import load_dotenv
import os
from datetime import date


from main import app
from branch import NeonClient
import database as db
from models import Order

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
            "/coupons/create_coupon",
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
        columns = inspector.get_columns("orders")
        column_names = [column["name"] for column in columns]
        assert "coupon_id" in column_names
    finally:
        app.dependency_overrides.clear()


def test_coupon_code_populated():

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
            sa.text("""
                SELECT id, coupon_id
                FROM orders
                WHERE id < 100
                LIMIT 1
            """)
        ).first()
        assert result is not None
        assert result.coupon_id == 1
    finally:
        app.dependency_overrides.clear()    
        
def test_integration():
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
        # Login control
        response = client.get(
            "/users/login?email_address=erica51@example.net"
        )

        
        assert response.status_code == 200

        user = response.json()
        print(user)
        assert user['id']==13
        # End Login control
        
        #create products
        response= client.post(
            "/products/create_product",
            json={
                "name": "product1",
                "price": 12,
                "stock": 100
            }
        )
        assert response.status_code == 200
        product_1 = response.json()
        
        response= client.post(
            "/products/create_product",
            json={
                "name": "product2",
                "price": 19,
                "stock": 200
            }
        )
        assert response.status_code == 200
        product_2 = response.json()
        
        
        response= client.post(
            "/products/create_product",
            json={
                "name": "product3",
                "price": 43,
                "stock": 50
            }
        )
        assert response.status_code == 200
        product_3 = response.json()
        
        # create order
        response= client.post(
            "/orders/create_order",
            json={
                "user_id": user['id'],
                "created_at": date.today().isoformat()
            }
        )
        
        assert response.status_code == 200
        order = response.json()
        
        # add products to order
        response= client.post(
            "/order_item/create_order_item",
            json={
                "order_id": order['id'],
                "product_id": product_1['id'],
                "quantity": 5
            }
        )
        assert response.status_code == 200
        order_item_1 = response.json()
        
        response= client.post(
            "/order_item/create_order_item",
            json={
                "order_id": order['id'],
                "product_id": product_2['id'],
                "quantity": 9
            }
        )
        assert response.status_code == 200
        order_item_2 = response.json()
        
        response= client.post(
            "/order_item/create_order_item",
            json={
                "order_id": order['id'],
                "product_id": product_3['id'],
                "quantity": 7
            }
        )
        assert response.status_code == 200
        order_item_3 = response.json()
        
        response = client.post(
            "/coupons/create_coupon",
            json={
                "code": "ANNIVERSARY",
                "discount": 10
            }
        )

        assert response.status_code == 200
        
        coupon=response.json()

        response = client.patch(
            f"/orders/set_coupon?order_id={order['id']}&coupon_id={coupon['id']}"
        )
        assert response.status_code == 200
        
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

    neon_client.run_migrations("1b6df6316c0e", database_url)
    
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
    
        # Login control
        response = client.get(
            "/login?email_address=erica51@example.net"
        )
        assert response.status_code == 200

        user = response.json()
        print(user)
        assert user['id']==13
        # End Login control
        
        #create products
        response= client.post(
            "/create_product",
            json={
                "name": "product1",
                "price": 12,
                "stock": 100
            }
        )
        assert response.status_code == 200
        product_1 = response.json()
        
        response= client.post(
            "/create_product",
            json={
                "name": "product2",
                "price": 19,
                "stock": 200
            }
        )
        assert response.status_code == 200
        product_2 = response.json()
        
        
        response= client.post(
            "/create_product",
            json={
                "name": "product3",
                "price": 43,
                "stock": 50
            }
        )
        assert response.status_code == 200
        product_3 = response.json()
        
        # create order
        response= client.post(
            "/create_order",
            json={
                "user_id": user['id'],
                "created_at": date.today().isoformat()
            }
        )
        
        assert response.status_code == 200
        order = response.json()
        
        # add products to order
        response= client.post(
            "/create_order_item",
            json={
                "order_id": order['id'],
                "product_id": product_1['id'],
                "quantity": 5
            }
        )
        assert response.status_code == 200
        order_item_1 = response.json()
        
        response= client.post(
            "/create_order_item",
            json={
                "order_id": order['id'],
                "product_id": product_2['id'],
                "quantity": 9
            }
        )
        assert response.status_code == 200
        order_item_2 = response.json()
        
        response= client.post(
            "/create_order_item",
            json={
                "order_id": order['id'],
                "product_id": product_3['id'],
                "quantity": 7
            }
        )
        assert response.status_code == 200
        order_item_3 = response.json()
        
        response = client.post(
            "/create_coupon",
            json={
                "code": "ANNIVERSARY",
                "discount": 10
            }
        )

        assert response.status_code == 200
        
        coupon=response.json()

        response = client.post(
            f"/set_coupon?order_id={order['id']}&coupon_id={coupon['id']}"
        )
        assert response.status_code == 200
        
        
    finally:
        app.dependency_overrides.clear()
        neon_client.delete_branch(branch_id)
"""
from fastapi.testclient import TestClient
from sqlalchemy import inspect
import sqlalchemy as sa
from dotenv import load_dotenv
import os
from decimal import Decimal
from datetime import date
import subprocess
import time
import requests
from playwright.sync_api import expect



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

def test_total_price_present():
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
        assert "total_price" in column_names
    finally:
        app.dependency_overrides.clear()


def test_total_price_corrected():

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
                SELECT id, coupon_id, total_price
                FROM orders
                WHERE id =1
            """)
        ).first()
        assert result is not None
        assert result.total_price == Decimal("178855.86")
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
            "/order_items/create_order_item",
            json={
                "order_id": order['id'],
                "product_id": product_1['id'],
                "quantity": 5
            }
        )
        assert response.status_code == 200
        order_item_1 = response.json()
        
        response= client.post(
            "/order_items/create_order_item",
            json={
                "order_id": order['id'],
                "product_id": product_2['id'],
                "quantity": 9
            }
        )
        assert response.status_code == 200
        order_item_2 = response.json()
        
        response= client.post(
            "/order_items/create_order_item",
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
        
        response = client.patch(
            f"/orders/calculate_total?order_id={order['id']}"
        )
        
        
        assert response.status_code == 200
        
        response = client.get(
            f"/orders/get_total_price?order_id={order['id']}"
        )
        
        total_price= response.json()
        assert response.status_code == 200
        assert total_price['total_price']==532
        
        response = client.patch(
            f"/orders/apply_discount?order_id={order['id']}"
        )
        
        assert response.status_code == 200
        
        response = client.get(
            f"/orders/get_total_price?order_id={order['id']}"
        )
        
        new_total= response.json()
        assert response.status_code == 200
        assert new_total['total_price']==478.8

    finally:
        app.dependency_overrides.clear()





def wait_for_server(url, timeout=30):
    start = time.time()

    while time.time() - start < timeout:
        try:
            response = requests.get(url)
            if response.status_code < 500:
                return
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(0.5)

    raise RuntimeError("Uvicorn non è partito entro il timeout")

def test_end_to_end(page):
    test_session = db.create_session(os.environ["DATABASE_URL"])
    
    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db.get_db] = override_get_db
    try:
        env = os.environ.copy()
        env["DATABASE_URL"] = os.environ["DATABASE_URL"]
        server = subprocess.Popen(
            [
                "uvicorn",
                "main:app",
                "--host", "127.0.0.1",
                "--port", "8000",
            ],
            env=env,
        )
        wait_for_server("http://127.0.0.1:8000/login_site")
        
        
        page.goto("http://127.0.0.1:8000/login_site")

        page.locator("#email").fill("erica51@example.net")
        page.locator("#login_button").click()

        page.wait_for_function(
        "() => localStorage.getItem('user_id') !== null"
        )
        user_id = page.evaluate(
        "() => localStorage.getItem('user_id')"
        )
        
        assert user_id is not None
        assert user_id == "13"
        
        page.goto("http://127.0.0.1:8000/product_site")
        
        page.locator("#create-order-button").click()
        
        page.wait_for_function(
        "() => localStorage.getItem('order_id') !== null"
        )
        order_id = page.evaluate(
        "() => localStorage.getItem('order_id')"
        )
        
        assert order_id is not None
        assert order_id == "10002"
        
        page.locator("#button-1").click()
        page.locator("#button-2").click()
        page.locator("#button-3").click()
        
        page.goto("http://127.0.0.1:8000/order_site")
        
        page.locator("#button-10002").click()
        
        page.wait_for_function(
        "() => localStorage.getItem('viewed_order_id') !== null"
        )
        viewed_order_id = page.evaluate( 
        "() => localStorage.getItem('viewed_order_id')"
        )
        
        assert viewed_order_id == "10002"
        
        page.goto("http://127.0.0.1:8000/order_item_site")
        
        with page.expect_response(
            lambda response:
                "/orders/calculate_total" in response.url
                and response.status == 200
        ):
            page.locator("#calculate-total-button").click()

        with page.expect_response(
            lambda response:
                "/orders/get_total_price" in response.url
                and response.status == 200
        ):
            page.locator("#get-total-button").click()
            
                
        text = page.locator("#total")
        expect(text).to_have_text("€2998.49")
        total = text.inner_text()
        assert total == "€2998.49"
        
        page.locator("#coupon_id").fill("1")
        with page.expect_response(
            lambda response:
            "/orders/apply_discount" in response.url
            and response.status == 200
        ):
            page.locator("#apply-coupon-button").click()
        
        with page.expect_response(
            lambda response:
            "/orders/get_total_price" in response.url
            and response.status == 200
        ):
            page.locator("#get-total-button").click()
        
        new_text = page.locator("#total")
        expect(new_text).to_have_text("€2698.64")
        new_total = new_text.inner_text()
        assert new_total == "€2698.64"
        
        
    finally:
        server.terminate()
        server.wait()
        app.dependency_overrides.clear()
 
"""    
def test_all(page):
    neon_client = NeonClient(
    api_key=NEON_API_KEY,
    project_id=NEON_PROJECT_ID,
    )

    
    try:
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
        
        response = client.post(
            "/coupons/create_coupon",
            json={
                "code": "WELCOME10",
                "discount": 10
            }
        )
        assert response.status_code == 200
        
        env = os.environ.copy()
        env["DATABASE_URL"] = database_url

        server = subprocess.Popen(
            [
                "uvicorn",
                "main:app",
                "--host", "127.0.0.1",
                "--port", "8000",
            ],
            env=env,
        )
        wait_for_server("http://127.0.0.1:8000/login_site")
        
        
        page.goto("http://127.0.0.1:8000/login_site")

        page.locator("#email").fill("erica51@example.net")
        page.locator("#login_button").click()

        page.wait_for_function(
        "() => localStorage.getItem('user_id') !== null"
        )
        user_id = page.evaluate(
        "() => localStorage.getItem('user_id')"
        )
        
        assert user_id is not None
        assert user_id == "13"
        
        page.goto("http://127.0.0.1:8000/product_site")
        
        page.locator("#create-order-button").click()
        
        page.wait_for_function(
        "() => localStorage.getItem('order_id') !== null"
        )
        order_id = page.evaluate(
        "() => localStorage.getItem('order_id')"
        )
        
        assert order_id is not None
        assert order_id == "10001"
        
        page.locator("#button-1").click()
        page.locator("#button-2").click()
        page.locator("#button-3").click()
        
        page.goto("http://127.0.0.1:8000/order_site")
        
        page.locator("#button-10001").click()
        
        page.wait_for_function(
        "() => localStorage.getItem('viewed_order_id') !== null"
        )
        viewed_order_id = page.evaluate( 
        "() => localStorage.getItem('viewed_order_id')"
        )
        
        assert viewed_order_id == "10001"
        
        page.goto("http://127.0.0.1:8000/order_item_site")
        
        page.locator("#calculate-total-button").click()
        page.locator("#get-total-button").click()
        
                
        text = page.locator("#total")
        expect(text).to_have_text("€2998.49")
        total = text.inner_text()
        assert total == "€2998.49"
        
        page.locator("#coupon_id").fill("1")
        with page.expect_response(
            lambda response:
            "/orders/apply_discount" in response.url
            and response.status == 200
        ):
            page.locator("#apply-coupon-button").click()
        
        with page.expect_response(
            lambda response:
            "/orders/get_total_price" in response.url
            and response.status == 200
        ):
            page.locator("#get-total-button").click()
        
        new_text = page.locator("#total")
        expect(new_text).to_have_text("€2698.64")
        new_total = new_text.inner_text()
        assert new_total == "€2698.64"
        
    finally:
        server.terminate()
        server.wait()
        app.dependency_overrides.clear()
        neon_client.delete_branch(branch_id)
        
"""
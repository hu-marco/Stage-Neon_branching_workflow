from faker import Faker
import random
import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decimal import *

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set or loaded")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

def create_session(database_url: str):
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    return SessionLocal

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close

#create_table
def create_all_table():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            print("Connection established")
            with conn.cursor() as cur:
            
                # users table
                cur.execute("""
                    CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(20),
                        email VARCHAR(20)
                    );
                """)
                print("Finished creating table users.")

                # categories table
                cur.execute("""
                    CREATE TABLE categories (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(25) NOT NULL
                    );
                """)
                print("Finished creating table categories.")

                # addresses table
                cur.execute("""
                    CREATE TABLE addresses (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        city VARCHAR(20),
                        street VARCHAR(20)
                    );
                """)
                print("Finished creating table addresses.")

                # products table
                cur.execute("""
                    CREATE TABLE products (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(15),
                        price FLOAT,
                        stock INTEGER,
                        category_id INTEGER,
                        foreign key(category_id)
                        references categories(id)
                    );
                """)
                print("Finished creating table products.")

                # orders table
                cur.execute("""
                    CREATE TABLE orders (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        created_at DATE,
                        foreign key(user_id)
                        references users(id)
                    );
                """)
                print("Finished creating table orders.")
                
                # order_items table
                cur.execute("""
                    CREATE TABLE order_items (
                        id SERIAL PRIMARY KEY,
                        order_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        foreign key(order_id)
                        references orders(id),
                        foreign key(product_id)
                        references products(id)
                    );
                """)
                print("Finished creating table order_items.")
                
                print("All the tables are created")
                conn.commit()
                return True
    except Exception as e:
        print("Connection failed.")
        print(e)
        return False
    

#insert the initial data
def insert_initial_data():
    fake = Faker('en_US')
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            print("Connection established")
            with conn.cursor() as cur:

                # users table
                for _ in range(500):
                    name = fake.first_name()[:20]
                    email = fake.email()[:20]
                    cur.execute(
                        """INSERT INTO users (name, email)
                        VALUES (%s, %s);
                        """,
                        (name, email)
                    )
                print("users data added")
                
                # categories table
                cur.execute(
                """
                INSERT INTO categories (name) VALUES
                    ('Electronics'),
                    ('Home & Garden'),
                    ('Health & Beauty'),
                    ('Food & Beverage'),
                    ('Sports & Outdoors'),
                    ('Hobbie & Toys'),
                    ('Fashion & Apparel'),
                    ('Game');
                    """
                )
                print("categories data added")
                
                # products table 
                
                products = [
                "Smartphone",
                "Keyboard",
                "Mouse",
                "Motherboard",
                "Chair",
                "Table",
                "Vase",
                "Garder Gnome",
                "Cologne",
                "Perfume",
                "Syrup",
                "Face cream",
                "Soda",
                "Fries",
                "Hamburger",
                "Water",
                "Ball",
                "Tent",
                "Sunglasses",
                "Watch",
                "Book",
                "Sewing kit",
                "Cards",
                "Multi-tool",
                "Shirt",
                "Shoes",
                "Bag",
                "Makeup",
                "Videogame",
                "Board games",
                "Computer",
                "Card set"
                ]
                
                batch_size = 500

                for _ in range(0,2000, batch_size):
                    products_data = []
                    
                    for _ in range(batch_size):
                        products_data.append((
                            random.choice(products), #product name
                            Decimal(str(round(random.uniform(1.5, 1999.99), 2))), # product price
                            random.randint(1, 100000) # products stock
                    ))    
                    execute_values(
                        cur,
                        """INSERT INTO products (name, price, stock)
                        VALUES %s;
                        """,
                        products_data
                    )
                print("products data added")
                
                # addresses table
                for x in range(1, 501):
                    city = fake.city()[:20]
                    street = fake.street_name()[:20]
                    cur.execute(
                        """INSERT INTO addresses 
                        (user_id, city, street)
                        VALUES (%s, %s, %s)""",
                        (x, city, street)
                    )
                print("addresses data added")
                
                # orders table
                for _ in range(0,10000, batch_size):
                    orders_data = []
                    for _ in range(batch_size):
                        orders_data.append((
                            random.randint(1, 500), #user_id
                            fake.date(end_datetime="+1w") #created_at
                        ))                
                    execute_values(
                        cur,
                    """INSERT INTO orders (user_id, created_at)
                    VALUES  %s;
                    """,
                    orders_data
                    )
                print("orders data added")
                
                # order_items
                for _ in range(0, 30000, batch_size):
                    orders_items_data = []
                    for _ in range(batch_size):
                        orders_items_data.append((
                            random.randint(1, 10000), #order_id
                            random.randint(1, 2000), #product_id
                            random.randint(1, 100)#quantity
                        ))
                    execute_values(
                    cur,
                    """INSERT INTO order_items
                    (order_id, product_id, quantity)
                    VALUES %s;
                    """,
                    orders_items_data
                    )
                print("order_items data added")
                conn.commit()
                return True
    except Exception as e:
        print("Connection failed.")
        print(e)
        return False


#delete all the table
def delete_all_table():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            print("Connection established")
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS order_items;")
                cur.execute("DROP TABLE IF EXISTS orders ;")
                cur.execute("DROP TABLE IF EXISTS products;")
                cur.execute("DROP TABLE IF EXISTS categories;")
                cur.execute("DROP TABLE IF EXISTS addresses;")
                cur.execute("DROP TABLE IF EXISTS users;")
                conn.commit()
                print("All the tables are deleted")
                return True
    except Exception as e:
        print("Connection failed.")
        print(e)
        return False
      
def delete_all_data():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            print("Connection established")
            
            with conn.cursor() as cur:
                cur.execute("""
                TRUNCATE TABLE 
                order_items, orders, categories, addresses, products, users
                RESTART IDENTITY CASCADE;
                 """)
                
                conn.commit()
                print("All the data are deleted")
                return True
    except Exception as e:
        print("Connection failed.")
        print(e)
        return False
        

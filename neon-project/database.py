from faker import Faker
import random
import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()



#create_table
def create_all_table():
    load_dotenv()
    conn_string = os.getenv("DATABASE_URL")
    
    try:
        with psycopg2.connect(conn_string) as conn:
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
                        price DOUBLE,
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
                        total DOUBLE,
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
    except Exception as e:
        print("Connection failed.")
        print(e)
    

#insert the initial data
def insert_initial_data():
    load_dotenv()
    conn_string = os.getenv("DATABASE_URL")
    
    fake = Faker('en_US')
    
    try:
        with psycopg2.connect(conn_string) as conn:
            print("Connection established")
            with conn.cursor() as cur:

                # users table
                for _ in range(500):
                    name = fake.first_name()
                    email = fake.email()
                    cur.execute(
                        """INSERT INTO users (name, email)
                        VALUES (%s, %s)""",
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
                    ('Game'),
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

                for _ in range(0, 2000, batch_size):
                    product_data = []
                    
                    for _ in range(batch_size):
                        product_data.append((
                            random.choice(products),
                            random.uniform(1.5, 1999.99),
                            random.randint(1, 100000)
                        ))
                
                cur.execute(
                """INSERT INTO products (name, pric, stock)
                    VALUES %s;
                """,
                product_data
                )
                print("products data added")
                
                # addresses table
                for x in range(500):
                    city = fake.city()[:20]
                    street = fake.street_name()[:20],
                    cur.execute(
                        """INSERT INTO addresses 
                        (user_id, city, street )
                        VALUES (%s, %s, %s)""",
                        (x, city, street)
                    )
                print("addresses data added")
                
                # orders table
                batch_size = 500

                for _ in range(0, 10000, batch_size):
                    order_data = []
                    
                    for _ in range(batch_size):
                        order_data.append((
                            random.randint(1, 500), #user_id
                            fake.date(end_datetime="+1w"), #created_at
                            random.uniform(1.5, 1999.99) #total
                        ))
                
                cur.execute(
                """INSERT INTO orders (user_id, created_at, total)
                    VALUES %s;
                """,
                order_data
                )
                print("orders data added")
                
                # order_items
                for _ in range(0, 30000, batch_size):
                    order_item_data = []
                    
                    for _ in range(batch_size):
                        order_item_data.append((
                            random.randint(1, 10000), #order_id
                            random.randint(1, 2000), #product_at
                            random.randint(1, 100) #quantity
                        ))
                
                cur.execute(
                """INSERT INTO order_items
                (order_id, product_id, quantity)
                    VALUES %s;
                """,
                order_item_data
                )
                print("order_items data added")
                
                
                conn.commit()
    except Exception as e:
        print("Connection failed.")
        print(e)


#delete all the table
def delete_all_table():
    load_dotenv()
    conn_string = os.getenv("DATABASE_URL")
    try:
        with psycopg2.connect(conn_string) as conn:
            print("Connection established")
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS order_items;")
                cur.execute("DROP TABLE IF EXISTS orders ;")
                cur.execute("DROP TABLE IF EXISTS categories;")
                cur.execute("DROP TABLE IF EXISTS address;")
                cur.execute("DROP TABLE IF EXISTS products;")
                cur.execute("DROP TABLE IF EXISTS users;")
                conn.commit()
                print("All the tables are deleted")
    except Exception as e:
        print("Connection failed.")
        print(e)
      
def delete_all_data():
    load_dotenv()
    conn_string = os.getenv("DATABASE_URL")
    try:
        with psycopg2.connect(conn_string) as conn:
            print("Connection established")
            
            with conn.cursor() as cur:
                cur.execute("""
                TRUNCATE TABLE 
                order_items, orders, categories, addresses, products, users
                RESTART IDENTITY CASCADE;
                 """)
                
                conn.commit()
                print("All the data are deleted")
    except Exception as e:
        print("Connection failed.")
        print(e)

        

from fastapi import APIRouter, Depends
import database as db


router = APIRouter()

@router.post("/create_tables")
def create_all_tables():
    success=db.create_all_table()
    if success:
        return {"status": "tables created"}
    else:
        return {"status": "table creation failed"}

@router.post("/add_data")
def insert_initial_data():
    success= db.insert_initial_data()
    if success:
        return {"status": "data added"}
    else:
        return {"status": "data addition failed"}

@router.post("/delete_table")
def delete_all_table():
    success=db.delete_all_table()
    if success:
        return {"status": "tables deleted"}
    else:
        return {"status": "tables removal failed"}

@router.post("/delete_data")
def delete_all_data():
    success=db.delete_all_data()
    if success:
        return {"status": "data deleted"}
    else:
        return {"status": "data removal failed"}
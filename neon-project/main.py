from fastapi import FastAPI
from routers import (
    database_router,
    branch_router,
    coupons_router,
    orders_router,
    products_router,
    order_items_router,
    users_router
)

app = FastAPI(
    title="E-commerce"
)

@app.get("/")
def root():
    return {"Hello":"World"}

app.include_router(database_router.router)
app.include_router(branch_router.router)
app.include_router(coupons_router.router)
app.include_router(orders_router.router)
app.include_router(order_items_router.router)
app.include_router(products_router.router)
app.include_router(users_router.router)
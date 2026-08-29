from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


app.include_router(database_router.router)
app.include_router(branch_router.router)
app.include_router(coupons_router.router)
app.include_router(orders_router.router)
app.include_router(order_items_router.router)
app.include_router(products_router.router)
app.include_router(users_router.router)


@app.get("/", include_in_schema=False)
def home(request: Request ):
    return templates.TemplateResponse(request, "home.html", {"title": "Home"})

@app.get("/product_site", include_in_schema=False)
def home(request: Request ):
    return templates.TemplateResponse(request, "product.html", {"title": "Product"})

@app.get("/login_site", include_in_schema=False)
def home(request: Request ):
    return templates.TemplateResponse(request, "login.html", {"title": "Login"})

@app.get("/order_site", include_in_schema=False)
def home(request: Request ):
    return templates.TemplateResponse(request, "order.html", {"title": "Order"})
    
@app.get("/order_item_site", include_in_schema=False)
def home(request: Request ):
    return templates.TemplateResponse(request, "order_item.html", {"title": "Order Items"})

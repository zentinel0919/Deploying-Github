from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId for working with MongoDB ObjectIDs

# Replace "your_actual_password" with your MongoDB Atlas password
atlas_password = 'natividad'

# MongoDB Atlas connection string
atlas_connection_string = f"mongodb+srv://harvey:natividad@cluster0.xcod1uv.mongodb.net/"

# Connect to MongoDB Atlas
client = MongoClient(atlas_connection_string)
db = client["simple_ecommerce"]

products_collection = db["products"]
sales_collection = db["sales"]

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (CSS and JS)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_home():
    return FileResponse("static/index.html")


@app.post("/buy")
async def buy_product(product_name: str):
    # Retrieve the product details from the products_collection
    product = products_collection.find_one({"name": product_name})

    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_name} not found")

    # Add logic to process the purchase and insert into MongoDB sales_collection
    sale_data = {
        "product_id": str(product["_id"]),  # Convert ObjectId to string
        "product_name": product["name"],
        "quantity": 1,  # For simplicity, assume quantity is 1 for each purchase
        "total_price": product.get("price", 0),  # Adjust this field based on your product schema
    }

    # Insert the sale_data into the sales_collection
    sales_collection.insert_one(sale_data)

    print(f"Product {product_name} purchased and recorded in MongoDB")
    return {"message": f"Product {product_name} purchased and recorded in MongoDB"}


@app.get("/report")
async def get_report(secret_key: str = Header(..., convert_underscores=False, alias="X-Secret-Key")):
    # Add proper authentication logic here, for now, check if secret_key is correct
    if secret_key != "groupings":  # Replace "groupings" with your actual secret key
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Add logic to fetch sales report from MongoDB
    # For simplicity, you can return a dummy report for now
    report = {"total_sales": 100, "products_sold": {"Product 1": 50, "Product 2": 50}}
    return report

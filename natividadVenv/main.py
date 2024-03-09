from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

# Replace "your_actual_password" with your MongoDB Atlas password
atlas_password = 'natividad'

# MongoDB Atlas connection string
atlas_connection_string = f"mongodb+srv://harvey:natividad@cluster0.xcod1uv.mongodb.net/"

# Connect to MongoDB Atlas
client = MongoClient(atlas_connection_string)
db = client["simple_ecommerce"]

products_collection = db["products"]  # Replace "products" with the actual name of your products collection
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

# Define the route for the home page
@app.get("/", response_class=HTMLResponse)
async def read_home():
    return FileResponse("static/index.html")

# Define the route to handle product purchases
@app.post("/buy/{product_id}")
async def buy_product(product_id: int):
    # Add logic to process the purchase and insert into MongoDB
    # For simplicity, you can just print a message for now
    print(f"Product {product_id} purchased!")
    return {"message": f"Product {product_id} purchased!"}

# Define the route to generate the sales report
@app.get("/report")
async def get_report(secret_key: str = Header(..., convert_underscores=False, alias="X-Secret-Key")):
    # Add proper authentication logic here, for now, check if secret_key is correct
    if secret_key != "groupings":  # Replace "groupings" with your actual secret key
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Add logic to fetch sales report from MongoDB
    # For simplicity, you can return a dummy report for now
    report = {"total_sales": 100, "products_sold": {"Product 1": 50, "Product 2": 50}}
    return report

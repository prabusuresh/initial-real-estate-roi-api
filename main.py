# main.py

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

templates = Jinja2Templates(directory="templates")


from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# Define your data model
class PropertyInput(BaseModel):
    location: str
    property_type: str
    property_price: float
    holding_years: int
    loan_amount: float
    expected_rent: float = None  # Optional

# Simulated rental estimate
def get_rental_estimate(location):
    location = location.lower()
    location_rent_mapping = {
        "bangalore": 18000,
        "mumbai": 25000,
        "chennai": 15000,
        "hyderabad": 16000,
        "delhi": 22000,
        "pune": 19000,
        "coimbatore": 12000,
    }
    return location_rent_mapping.get(location)

# ROI calculator
def calculate_roi(property_price, expected_rent, holding_years, appreciation_rate=0.06):
    total_rent_income = expected_rent * 12 * holding_years
    final_property_value = property_price * ((1 + appreciation_rate) ** holding_years)
    roi = (total_rent_income + (final_property_value - property_price)) / property_price * 100
    return roi, total_rent_income, final_property_value

# API Endpoint
@app.post("/analyze")
def analyze_property(data: PropertyInput):
    rent = data.expected_rent or get_rental_estimate(data.location) or 15000

    roi, total_rent_income, final_property_value = calculate_roi(
        data.property_price, rent, data.holding_years
    )

    result = {
        "Location": data.location,
        "Property Type": data.property_type,
        "Purchase Price": data.property_price,
        "Expected Monthly Rent": rent,
        "Holding Period (Years)": data.holding_years,
        "Loan Amount": data.loan_amount,
        "Estimated Total Rental Income": total_rent_income,
        "Estimated Final Property Value": final_property_value,
        "Overall ROI (%)": roi
    }
    return result

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# main.py

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Format number into Indian Rupees
def format_inr(amount):
    return f"₹{amount:,.2f}"

# Simulated market data
def fetch_market_data(location):
    print(f"Fetching market data for {location}... (mocked)")
    average_price_growth_rate = np.random.uniform(0.04, 0.07)
    average_rental_yield = 0.035
    return average_price_growth_rate, average_rental_yield

# Simulated risk analysis
def analyze_risk(location, property_type):
    risk_score = np.random.choice(["Low", "Medium", "High"])
    reason = "Based on general location saturation and demand trends (mocked)"
    return risk_score, reason

# ROI calculation
def calculate_roi(property_price, expected_rent, holding_years, appreciation_rate=0.06):
    total_rent_income = expected_rent * 12 * holding_years
    final_property_value = property_price * ((1 + appreciation_rate) ** holding_years)
    roi = (total_rent_income + (final_property_value - property_price)) / property_price * 100
    return roi, total_rent_income, final_property_value

# Fallback rent
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

# Pydantic model for API users
class PropertyInput(BaseModel):
    location: str
    property_type: str
    property_price: float
    holding_years: int
    loan_amount: float
    expected_rent: float = None

# API Endpoint
@app.post("/analyze")
def analyze_property(data: PropertyInput):
    rent = data.expected_rent or get_rental_estimate(data.location) or 15000
    roi, total_rent_income, final_property_value = calculate_roi(
        data.property_price, rent, data.holding_years
    )
    return {
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

# Web Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/analyze-form", response_class=HTMLResponse)
async def analyze_form(request: Request,
                       location: str = Form(...),
                       property_type: str = Form(...),
                       property_price: float = Form(...),
                       expected_rent: float = Form(...),
                       holding_years: int = Form(...),
                       loan_amount: float = Form(...)):

    appreciation_rate, rental_yield = fetch_market_data(location)
    roi, total_rent_income, final_property_value = calculate_roi(
        property_price, expected_rent, holding_years, appreciation_rate
    )
    risk_score, reason = analyze_risk(location, property_type)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "location": location,
        "property_type": property_type,
        "purchase_price": format_inr(property_price),
        "expected_rent": format_inr(expected_rent),
        "holding_years": holding_years,
        "loan_amount": format_inr(loan_amount),
        "total_rent_income": format_inr(total_rent_income),
        "final_property_value": format_inr(final_property_value),
        "roi": f"{roi:.2f}%",
        "risk_score": risk_score,
        "reason": reason
    })

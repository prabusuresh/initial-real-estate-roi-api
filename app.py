# app.py

import pandas as pd
import numpy as np
import requests 

# Fetch Rental Estimate
def get_rental_estimate(location):
    try:
        # Very basic simulation of rental fetching (later real APIs)
        url = f"https://www.nobroker.in/api/v1/multilocation/search?searchString={location}"
        response = requests.get(url)
        if response.status_code == 200:
            rental_estimate = 15000 + np.random.randint(-3000, 3000)  # ₹12k - ₹18k dummy range
            return rental_estimate
        else:
            print("⚠️ Rental API not reachable, falling back to manual input.")
            return None
    except Exception as e:
        print(f"⚠️ Error fetching rental data: {e}")
        return None


# 1. Take User Input
# 1. Take User Input
def get_user_input():
    print("🏠 Enter Property Investment Details")
    location = input("Location (City/Area): ")
    property_type = input("Property Type (Apartment/Villa/Plot/Commercial): ")
    property_price = float(input("Purchase Price (₹): "))

    # Rental fetching attempt
    auto_rent = get_rental_estimate(location)
    if auto_rent:
        print(f"Auto-fetched approximate monthly rent for {location}: ₹{auto_rent}")
        use_auto_rent = input("Do you want to use this rent? (yes/no): ").strip().lower()
        if use_auto_rent == "yes":
            expected_rent = auto_rent
        else:
            expected_rent = float(input("Enter your expected Monthly Rent (₹): "))
    else:
        expected_rent = float(input("Expected Monthly Rent (₹): "))

    holding_years = int(input("Planned Holding Period (Years): "))
    loan_amount = float(input("Loan Amount (₹) [Enter 0 if no loan]: "))
    return location, property_type, property_price, expected_rent, holding_years, loan_amount


# 2. Fetch Market Data (Dummy for Now)
def fetch_market_data(location):
    print(f"Fetching market data for {location}... (using dummy data)")
    # Normally you will call an API here
    average_price_growth_rate = np.random.uniform(0.04, 0.07)  # 4%-7% appreciation randomly
    average_rental_yield = 0.035       # 3.5% rental yield
    return average_price_growth_rate, average_rental_yield

# 3. Calculate ROI
def calculate_roi(property_price, expected_rent, holding_years, appreciation_rate):
    total_rent_income = expected_rent * 12 * holding_years
    final_property_value = property_price * ((1 + appreciation_rate) ** holding_years)
    roi = (total_rent_income + (final_property_value - property_price)) / property_price * 100
    return roi, total_rent_income, final_property_value

# 4. Risk Analysis (Dummy)
def analyze_risk(location, property_type):
    # Very simple risk logic
    risk_score = np.random.choice(["Low", "Medium", "High"])
    reason = "Based on general location saturation and demand trends (mocked)"
    return risk_score, reason

# 5. Generate Report
def generate_report(location, property_type, property_price, expected_rent, holding_years, loan_amount,
                     roi, total_rent_income, final_property_value, risk_score, reason):
    print("\n📋 INVESTMENT ANALYSIS REPORT")
    print(f"Location: {location}")
    print(f"Property Type: {property_type}")
    print(f"Purchase Price: ₹{property_price:,.0f}")
    print(f"Expected Monthly Rent: ₹{expected_rent:,.0f}")
    print(f"Holding Period: {holding_years} years")
    print(f"Loan Amount: ₹{loan_amount:,.0f}")
    
    if loan_amount > 0:
        emi = calculate_emi(loan_amount)
        print(f"Estimated Monthly EMI: ₹{emi:,.0f}")
        total_emi_paid = emi * 12 * holding_years
        print(f"Total EMI Paid Over {holding_years} years: ₹{total_emi_paid:,.0f}")
    else:
        emi = 0
        total_emi_paid = 0

    print("-" * 50)
    print(f"Estimated Total Rental Income: ₹{total_rent_income:,.0f}")
    print(f"Estimated Property Value After {holding_years} years: ₹{final_property_value:,.0f}")
    print(f"Overall Estimated ROI: {roi:.2f}%")
    print("-" * 50)
    print(f"Risk Level: {risk_score}")
    print(f"Risk Reason: {reason}")

# EMI Calculator
def calculate_emi(loan_amount, annual_interest_rate=0.085, loan_tenure_years=20):
    monthly_interest_rate = annual_interest_rate / 12
    num_payments = loan_tenure_years * 12
    emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** num_payments) / (((1 + monthly_interest_rate) ** num_payments) - 1)
    return emi

# Main
if __name__ == "__main__":
    location, property_type, property_price, expected_rent, holding_years, loan_amount = get_user_input()
    appreciation_rate, rental_yield = fetch_market_data(location)
    roi, total_rent_income, final_property_value = calculate_roi(property_price, expected_rent, holding_years, appreciation_rate)
    risk_score, reason = analyze_risk(location, property_type)
    generate_report(location, property_type, property_price, expected_rent, holding_years, loan_amount,
                    roi, total_rent_income, final_property_value, risk_score, reason)


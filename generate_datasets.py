"""
Data Analyst Mastery Suite - Dataset Generator
Generates realistic datasets with intentional data quality issues for training.
"""
import csv
import random
import os
from datetime import datetime, timedelta
import math

random.seed(42)
os.makedirs("datasets", exist_ok=True)

# ============================================================
# DATASET 1: E-Commerce Transactions (~5000 rows)
# ============================================================
print("Generating E-Commerce dataset...")

categories = {
    "Electronics": {"products": ["Laptop", "Smartphone", "Headphones", "Tablet", "Smart Watch", "Camera", "Speaker", "Monitor"], "price_range": (49.99, 1299.99)},
    "Clothing": {"products": ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers", "Hoodie", "Shorts", "Scarf"], "price_range": (14.99, 199.99)},
    "Home & Kitchen": {"products": ["Blender", "Coffee Maker", "Cookware Set", "Air Fryer", "Vacuum", "Toaster", "Lamp", "Rug"], "price_range": (19.99, 349.99)},
    "Books": {"products": ["Fiction Novel", "Textbook", "Cookbook", "Biography", "Self-Help Book", "Comic Book"], "price_range": (7.99, 49.99)},
    "Sports": {"products": ["Yoga Mat", "Dumbbells", "Running Shoes", "Bicycle", "Tennis Racket", "Basketball", "Jump Rope"], "price_range": (9.99, 499.99)},
}

countries = ["United States", "United Kingdom", "Germany", "Canada", "Australia", "France", "Japan", "Brazil", "India", "Egypt"]
payment_methods = ["Credit Card", "Debit Card", "PayPal", "Apple Pay", "Google Pay", "Bank Transfer"]

# Generate 500 customer IDs
customer_ids = [f"CUST-{str(i).zfill(4)}" for i in range(1, 501)]

# Some customers buy more frequently (power law)
frequent_customers = random.sample(customer_ids, 80)

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)

ecommerce_rows = []
order_id = 1000

for i in range(5200):
    # Pick customer - frequent customers appear more
    if random.random() < 0.4:
        customer = random.choice(frequent_customers)
    else:
        customer = random.choice(customer_ids)
    
    # Pick category and product
    cat = random.choice(list(categories.keys()))
    product = random.choice(categories[cat]["products"])
    low, high = categories[cat]["price_range"]
    price = round(random.uniform(low, high), 2)
    quantity = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0]
    
    # Random date with seasonal patterns (more sales in Nov-Dec)
    days_range = (end_date - start_date).days
    day_offset = random.randint(0, days_range)
    order_date = start_date + timedelta(days=day_offset)
    
    # Boost Q4 sales
    if order_date.month in [11, 12]:
        if random.random() < 0.3:
            continue  # We'll add extra Q4 rows later
    
    country = random.choices(countries, weights=[30, 15, 12, 10, 8, 7, 6, 5, 4, 3])[0]
    payment = random.choice(payment_methods)
    
    # Intentional data issues:
    # 1. Some missing values
    if random.random() < 0.03:
        country = ""
    if random.random() < 0.02:
        payment = ""
    
    # 2. Some negative quantities (returns)
    if random.random() < 0.04:
        quantity = -quantity
    
    # 3. Date format inconsistencies
    if random.random() < 0.05:
        date_str = order_date.strftime("%d/%m/%Y")
    elif random.random() < 0.05:
        date_str = order_date.strftime("%m-%d-%Y")
    else:
        date_str = order_date.strftime("%Y-%m-%d")
    
    # 4. Some duplicates
    if random.random() < 0.02:
        ecommerce_rows.append(ecommerce_rows[-1] if ecommerce_rows else None)
    
    total = round(price * abs(quantity), 2)
    if quantity < 0:
        total = -total
    
    row = {
        "order_id": f"ORD-{order_id}",
        "customer_id": customer,
        "order_date": date_str,
        "product_name": product,
        "category": cat,
        "unit_price": price,
        "quantity": quantity,
        "total_amount": total,
        "country": country,
        "payment_method": payment
    }
    ecommerce_rows.append(row)
    order_id += 1

# Remove None entries from duplicate injection
ecommerce_rows = [r for r in ecommerce_rows if r is not None]

# Add extra Q4 sales
for _ in range(800):
    month = random.choice([11, 12])
    year = random.choice([2022, 2023, 2024])
    day = random.randint(1, 28)
    order_date = datetime(year, month, day)
    cat = random.choices(list(categories.keys()), weights=[35, 20, 20, 10, 15])[0]
    product = random.choice(categories[cat]["products"])
    low, high = categories[cat]["price_range"]
    price = round(random.uniform(low, high), 2)
    quantity = random.choices([1, 2, 3, 4, 5], weights=[40, 25, 20, 10, 5])[0]
    customer = random.choice(customer_ids)
    country = random.choices(countries, weights=[30, 15, 12, 10, 8, 7, 6, 5, 4, 3])[0]
    payment = random.choice(payment_methods)
    total = round(price * quantity, 2)
    
    row = {
        "order_id": f"ORD-{order_id}",
        "customer_id": customer,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "product_name": product,
        "category": cat,
        "unit_price": price,
        "quantity": quantity,
        "total_amount": total,
        "country": country,
        "payment_method": payment
    }
    ecommerce_rows.append(row)
    order_id += 1

random.shuffle(ecommerce_rows)

with open("datasets/ecommerce_transactions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["order_id", "customer_id", "order_date", "product_name", "category", "unit_price", "quantity", "total_amount", "country", "payment_method"])
    writer.writeheader()
    writer.writerows(ecommerce_rows)

print(f"  -> ecommerce_transactions.csv: {len(ecommerce_rows)} rows")

# ============================================================
# DATASET 2: Health Risk Data (~2000 rows)
# ============================================================
print("Generating Health Risk dataset...")

health_rows = []

for i in range(2000):
    patient_id = f"PAT-{str(i+1).zfill(4)}"
    age = random.randint(18, 85)
    gender = random.choice(["Male", "Female"])
    
    # BMI correlated with age slightly
    bmi_base = random.gauss(26, 5)
    bmi = round(max(15, min(50, bmi_base + (age - 40) * 0.05)), 1)
    
    # Blood pressure correlated with age and BMI
    systolic_base = 110 + (age - 30) * 0.5 + (bmi - 25) * 1.2
    systolic = round(max(85, min(200, random.gauss(systolic_base, 12))))
    diastolic = round(max(55, min(130, systolic * 0.6 + random.gauss(0, 8))))
    
    # Cholesterol correlated with age and BMI
    cholesterol = round(max(120, min(350, random.gauss(200 + (age - 30) * 0.8 + (bmi - 25) * 2, 30))))
    
    # Blood sugar
    blood_sugar = round(max(60, min(250, random.gauss(100 + (bmi - 25) * 1.5, 20))))
    
    # Smoking
    smoking = random.choices(["Never", "Former", "Current"], weights=[50, 25, 25])[0]
    
    # Exercise hours per week
    exercise_hours = round(max(0, random.gauss(3.5, 2.5)), 1)
    
    # Family history
    family_history = random.choices(["Yes", "No"], weights=[30, 70])[0]
    
    # Calculate risk score (0-100) based on factors
    risk = 0
    risk += max(0, (age - 40)) * 0.5
    risk += max(0, (bmi - 25)) * 2
    risk += max(0, (systolic - 120)) * 0.3
    risk += max(0, (cholesterol - 200)) * 0.15
    risk += max(0, (blood_sugar - 100)) * 0.2
    if smoking == "Current":
        risk += 15
    elif smoking == "Former":
        risk += 5
    risk -= exercise_hours * 2
    if family_history == "Yes":
        risk += 10
    risk = max(0, min(100, risk + random.gauss(0, 5)))
    risk_score = round(risk, 1)
    
    # Heart disease outcome (binary) based on risk
    heart_disease_prob = 1 / (1 + math.exp(-(risk_score - 45) / 12))
    heart_disease = 1 if random.random() < heart_disease_prob else 0
    
    # Intentional data issues:
    # 1. Missing values
    row_bmi = bmi if random.random() > 0.04 else ""
    row_chol = cholesterol if random.random() > 0.03 else ""
    row_exercise = exercise_hours if random.random() > 0.05 else ""
    row_blood_sugar = blood_sugar if random.random() > 0.03 else ""
    
    # 2. Some outliers
    if random.random() < 0.01:
        row_bmi = round(random.uniform(55, 70), 1)
    
    # 3. Gender inconsistency
    if random.random() < 0.02:
        gender = random.choice(["M", "F", "male", "female"])
    
    # 4. Smoking inconsistency
    if random.random() < 0.02:
        smoking = random.choice(["Yes", "No", "current", "never"])
    
    row = {
        "patient_id": patient_id,
        "age": age,
        "gender": gender,
        "bmi": row_bmi,
        "systolic_bp": systolic,
        "diastolic_bp": diastolic,
        "cholesterol": row_chol,
        "blood_sugar": row_blood_sugar,
        "smoking_status": smoking,
        "exercise_hours_per_week": row_exercise,
        "family_history": family_history,
        "risk_score": risk_score,
        "heart_disease": heart_disease
    }
    health_rows.append(row)

with open("datasets/health_risk_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["patient_id", "age", "gender", "bmi", "systolic_bp", "diastolic_bp", "cholesterol", "blood_sugar", "smoking_status", "exercise_hours_per_week", "family_history", "risk_score", "heart_disease"])
    writer.writeheader()
    writer.writerows(health_rows)

print(f"  -> health_risk_data.csv: {len(health_rows)} rows")

# ============================================================
# DATASET 3: Stock Market Data (Simulated realistic prices)
# ============================================================
print("Generating Stock Market dataset...")

stocks = {
    "AAPL": {"start_price": 130, "volatility": 0.018, "drift": 0.0003},
    "GOOGL": {"start_price": 95, "volatility": 0.020, "drift": 0.0002},
    "MSFT": {"start_price": 250, "volatility": 0.016, "drift": 0.0004},
    "AMZN": {"start_price": 105, "volatility": 0.022, "drift": 0.0002},
    "TSLA": {"start_price": 120, "volatility": 0.035, "drift": 0.0001},
}

stock_start = datetime(2020, 1, 2)
stock_end = datetime(2024, 12, 31)
stock_rows = []

for ticker, params in stocks.items():
    price = params["start_price"]
    current_date = stock_start
    
    while current_date <= stock_end:
        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue
        
        # Geometric Brownian Motion for realistic price movement
        daily_return = random.gauss(params["drift"], params["volatility"])
        price *= (1 + daily_return)
        price = max(price, 5)  # Floor price
        
        open_price = round(price * (1 + random.gauss(0, 0.005)), 2)
        high_price = round(max(price, open_price) * (1 + abs(random.gauss(0, 0.008))), 2)
        low_price = round(min(price, open_price) * (1 - abs(random.gauss(0, 0.008))), 2)
        close_price = round(price, 2)
        
        # Volume with some randomness
        base_volume = random.randint(20_000_000, 80_000_000)
        # Higher volume on big price moves
        volume = int(base_volume * (1 + abs(daily_return) * 10))
        
        row = {
            "date": current_date.strftime("%Y-%m-%d"),
            "ticker": ticker,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume
        }
        stock_rows.append(row)
        current_date += timedelta(days=1)

# Sort by date then ticker
stock_rows.sort(key=lambda x: (x["date"], x["ticker"]))

with open("datasets/stock_market_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "ticker", "open", "high", "low", "close", "volume"])
    writer.writeheader()
    writer.writerows(stock_rows)

print(f"  -> stock_market_data.csv: {len(stock_rows)} rows")

# ============================================================
# DATASET 4: Excel Sales Data (for Excel Mastery project)
# ============================================================
print("Generating Excel Sales dataset...")

regions = ["North", "South", "East", "West", "Central"]
sales_reps = {
    "North": ["Ahmed Hassan", "Sara Ali", "Omar Khaled"],
    "South": ["Mona Ibrahim", "Youssef Nabil", "Layla Farid"],
    "East": ["Karim Mostafa", "Nour El-Din", "Hana Samir"],
    "West": ["Tarek Mansour", "Dina Reda", "Amr Salah"],
    "Central": ["Fatma Gamal", "Mahmoud Adel", "Rania Sayed"]
}

product_catalog = {
    "Software": {"items": ["CRM License", "ERP Module", "Analytics Suite", "Security Package", "Cloud Storage Plan"], "price_range": (500, 15000)},
    "Hardware": {"items": ["Server Rack", "Workstation", "Network Switch", "Printer", "UPS System"], "price_range": (200, 8000)},
    "Services": {"items": ["Consulting Hour", "Training Session", "Support Contract", "Installation", "Data Migration"], "price_range": (100, 5000)},
    "Accessories": {"items": ["Keyboard", "Mouse", "Monitor Stand", "USB Hub", "Webcam"], "price_range": (15, 250)},
}

excel_rows = []
for i in range(3000):
    sale_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    region = random.choices(regions, weights=[25, 20, 22, 18, 15])[0]
    rep = random.choice(sales_reps[region])
    cat = random.choices(list(product_catalog.keys()), weights=[35, 25, 25, 15])[0]
    product = random.choice(product_catalog[cat]["items"])
    low, high = product_catalog[cat]["price_range"]
    unit_price = round(random.uniform(low, high), 2)
    qty = random.choices([1, 2, 3, 5, 10], weights=[40, 25, 15, 12, 8])[0]
    discount_pct = random.choices([0, 0.05, 0.1, 0.15, 0.2], weights=[40, 20, 20, 12, 8])[0]
    revenue = round(unit_price * qty * (1 - discount_pct), 2)
    cost = round(revenue * random.uniform(0.4, 0.7), 2)
    profit = round(revenue - cost, 2)
    
    # Marketing spend for regression analysis
    marketing_spend = round(random.uniform(100, 5000) + revenue * random.uniform(0.01, 0.05), 2)
    
    row = {
        "sale_id": f"SALE-{str(i+1).zfill(5)}",
        "date": sale_date.strftime("%Y-%m-%d"),
        "region": region,
        "sales_rep": rep,
        "category": cat,
        "product": product,
        "unit_price": unit_price,
        "quantity": qty,
        "discount_pct": discount_pct,
        "revenue": revenue,
        "cost": cost,
        "profit": profit,
        "marketing_spend": marketing_spend
    }
    excel_rows.append(row)

excel_rows.sort(key=lambda x: x["date"])

with open("datasets/excel_sales_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["sale_id", "date", "region", "sales_rep", "category", "product", "unit_price", "quantity", "discount_pct", "revenue", "cost", "profit", "marketing_spend"])
    writer.writeheader()
    writer.writerows(excel_rows)

print(f"  -> excel_sales_data.csv: {len(excel_rows)} rows")

# Create solutions directory
os.makedirs("solutions", exist_ok=True)

print("\n✅ All datasets generated successfully!")
print(f"Total files: 4 CSV files in datasets/ directory")

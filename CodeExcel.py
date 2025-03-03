import openpyxl

# Charger le fichier Excel
file_path = "investment_results.xlsx"
wb = openpyxl.load_workbook(file_path)
sheet = wb["Sheet1"]

# Exemple : Écrire des valeurs de test
sheet["A1"] = "Country"
sheet["B1"] = "City"
sheet["C1"] = "Property Price"

# 🔍 Vérification avant sauvegarde
print("Données à écrire :", sheet["A1"].value, sheet["B1"].value, sheet["C1"].value)

# Sauvegarde
wb.save(file_path)
print("Fichier bien sauvegardé !")

# Hardcoded database for interest rates and appreciation rates
interest_rates = {
    "France": 0.04,
    "USA": 0.05,
    "UK": 0.045,
    "Mexico": 0.07,
    "Panama": 0.06,
    "Scotland": 0.043,
    "Wales": 0.042,
    "Northern Ireland": 0.044
}

appreciation_rates = {
    "Paris": 0.03,
    "Marseille": 0.025,
    "Lyon": 0.027,
    "New York": 0.025,
    "Seattle": 0.022,
    "Miami": 0.028,
    "London": 0.027,
    "Mexico City": 0.02,
    "Guadalajara": 0.018,
    "Monterrey": 0.021,
    "Panama City": -0.05  # Negative appreciation for simulation
}


def calculate_loan(property_price, available_capital):
    """Calculates the loan amount required."""
    return property_price - available_capital


def compute_mortgage_payment(loan_amount, interest_rate, years):
    """Computes monthly mortgage payment (simple interest model)."""
    total_payment = loan_amount * (1 + interest_rate * years)
    monthly_payment = total_payment / (years * 12)
    return monthly_payment, total_payment


def estimate_future_value(property_price, appreciation_rate, years=10):
    """Estimates the future property value."""
    return property_price * ((1 + appreciation_rate) ** years)


def investment_analysis(country, city, property_price, available_capital, years, row):
    """Performs full investment analysis and writes results to Excel."""
    if country not in interest_rates or city not in appreciation_rates:
        print(f"Data for {country} or {city} is not available.")
        return

    loan_amount = calculate_loan(property_price, available_capital)
    interest_rate = interest_rates[country]
    appreciation_rate = appreciation_rates[city]

    monthly_payment, total_mortgage_cost = compute_mortgage_payment(loan_amount, interest_rate, years)
    future_value = estimate_future_value(property_price, appreciation_rate)

    total_cost = total_mortgage_cost + available_capital
    profit_or_loss = future_value - total_cost

    # Write results back to Excel
    sheet[f"G{row}"] = loan_amount
    sheet[f"H{row}"] = monthly_payment
    sheet[f"I{row}"] = total_mortgage_cost
    sheet[f"J{row}"] = future_value
    sheet[f"K{row}"] = total_cost
    sheet[f"L{row}"] = profit_or_loss
    sheet[f"M{row}"] = "Profitable ✅" if profit_or_loss > 0 else "Loss ❌"


# Read data from Excel and perform investment analysis
for row in range(2, sheet.max_row + 1):  # Assuming headers are in row 1
    country = sheet[f"A{row}"].value
    city = sheet[f"B{row}"].value
    property_price = sheet[f"C{row}"].value
    available_capital = sheet[f"D{row}"].value
    years = sheet[f"E{row}"].value

    # Perform investment analysis for each row
    investment_analysis(country, city, property_price, available_capital, years, row)

# Save the updated Excel file
wb.save("investment_results.xlsx")
print("Investment analysis completed and saved to Excel.")

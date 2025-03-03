import openpyxl
import matplotlib.pyplot as plt
import numpy as np

# Load the Excel file
file_path = "investment_data.xlsx"
wb = openpyxl.load_workbook(file_path)
sheet = wb["Sheet1"]  # Ensure the sheet is named "Sheet1"

# Database of interest rates and appreciation rates
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
    "Panama City": -0.05
}

# Retrieve user inputs from Excel
country = sheet["A2"].value
city = sheet["B2"].value
property_price = sheet["C2"].value
capital = sheet["D2"].value
loan_duration = sheet["E2"].value

# Check if data exists
if country not in interest_rates or city not in appreciation_rates:
    sheet["F2"].value = "Sorry, we are working on collecting more data."
else:
    interest_rate = interest_rates[country]
    appreciation_rate = appreciation_rates[city]

    # Loan calculation
    loan_amount = property_price - capital
    monthly_payment = (loan_amount * (1 + interest_rate * loan_duration)) / (loan_duration * 12)

    # Future value calculation
    future_value = property_price * ((1 + appreciation_rate) ** loan_duration)

    # Profitability analysis
    total_cost = monthly_payment * loan_duration * 12 + capital
    profit_or_loss = future_value - total_cost
    result = "Profitable" if profit_or_loss > 0 else "Not profitable"

    # Write results in Excel
    sheet["F2"].value = result

    # Generate graph
    years = np.arange(1, loan_duration + 1)
    annual_value = [property_price * ((1 + appreciation_rate) ** i) for i in years]

    plt.figure(figsize=(8, 5))
    plt.plot(years, annual_value, marker='o', linestyle='-', color='b', label='Property Value Evolution')
    plt.axhline(y=total_cost, color='r', linestyle='--', label='Total Investment Cost')
    plt.xlabel("Years")
    plt.ylabel("Value (€)")
    plt.title("Investment Evolution")
    plt.legend()
    plt.grid()

    # Save the graph
    graph_path = "investment_graph.png"
    plt.savefig(graph_path)
    plt.close()

    # Add the graph to Excel
    from openpyxl.drawing.image import Image

    img = Image(graph_path)
    sheet.add_image(img, "H2")

# Save the Excel file
wb.save(file_path)
print("Investment analysis completed and saved to Excel.")

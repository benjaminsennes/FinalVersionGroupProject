import xlwings as xw
import matplotlib.pyplot as plt
import numpy as np
import time
import os

# Open the Excel file dynamically
file_path = "investment_data.xlsx"
wb = xw.Book(file_path)  # Opens the file live
sheet = wb.sheets["Sheet1"]  # Selects the correct sheet

# Database for interest and appreciation rates
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

# Function to analyze the investment
def investment_analysis():
    # Read user input from Excel
    country = sheet["A2"].value
    city = sheet["B2"].value
    property_price = sheet["C2"].value
    personal_funding = sheet["D2"].value
    loan_duration = sheet["E2"].value

    # If data is missing, display a message
    if country not in interest_rates and city not in appreciation_rates:
        sheet["F2"].value = "Sorry, we are working on collecting more data."
        return

    # Retrieve interest and appreciation rates
    interest_rate = interest_rates[country]
    appreciation_rate = appreciation_rates[city]

    # Loan calculation
    loan_amount = property_price - personal_funding
    monthly_payment = (loan_amount * (1 + interest_rate * loan_duration)) / (loan_duration * 12)

    # Define a longer horizon (e.g., 30 years)
    max_years = 30  # Maximum period to visualize investment growth

    # Future property value calculation over a longer period
    years = np.arange(1, max_years + 1)
    annual_values = [property_price * ((1 + appreciation_rate) ** i) for i in years]

    # Profitability analysis
    total_cost = (monthly_payment * loan_duration * 12) + personal_funding
    profit_or_loss = [value - total_cost for value in annual_values]

    # Find the break-even point (first year where profit is positive)
    break_even_year = next((i for i, p in enumerate(profit_or_loss, 1) if p > 0), None)

    # Update the result message in Excel
    if break_even_year:
        sheet["F2"].value = f"Profitable from year {break_even_year} ✅"
    else:
        sheet["F2"].value = "Not Profitable within 30 years ❌"

    # Generate the graph
    plt.figure(figsize=(8, 5))
    plt.plot(years, annual_values, marker='o', linestyle='-', color='b', label='Property Value Over Time')
    plt.axhline(y=total_cost, color='r', linestyle='--', label='Total Investment Cost')

    # Highlight the break-even point
    if break_even_year:
        plt.scatter(break_even_year, annual_values[break_even_year - 1], color='g', s=100, zorder=3, label="Break-Even Point")

    plt.xlabel("Years")
    plt.ylabel("Value (€)")
    plt.title("Investment Evolution (Long-Term View)")
    plt.legend()
    plt.grid()

    # Save the graph
    graph_path = "investment_graph.png"
    plt.savefig(graph_path)
    plt.close()

    # Insert the graph into Excel
    img_path = os.path.abspath(graph_path)
    sheet.pictures.add(img_path, name="InvestmentGraph", update=True, left=400, top=50)

    print("Investment analysis updated!")

# **Live update loop**
while True:
    investment_analysis()
    time.sleep(10)  # Updates every 10 seconds
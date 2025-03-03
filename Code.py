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


def display_supported_options():
    """Displays the list of supported countries and cities."""
    print("\nSupported countries:")
    for country, rate in interest_rates.items():
        print(f"- {country}")
    print("\nSupported cities:")
    for city, rate in appreciation_rates.items():
        print(f"- {city}")


def calculate_loan(property_price, available_capital):
    """Calculates the loan amount required."""
    return property_price - available_capital


def compute_mortgage_payment(loan_amount, interest_rate, years):
    """Computes monthly mortgage payment (simple interest model)."""
    total_payment = loan_amount * (1 + interest_rate*years)
    monthly_payment = total_payment / (years * 12)
    return monthly_payment, total_payment


def estimate_future_value(property_price, appreciation_rate, years=10):
    """Estimates the future property value in 10 years."""
    return property_price * ((1 + appreciation_rate) ** years)


def investment_analysis(country, city, property_price, available_capital, years):
    """Performs full investment analysis."""
    if country not in interest_rates or city not in appreciation_rates:
        print("Data for the selected country or city is not available.")
        return

    loan_amount = calculate_loan(property_price, available_capital)
    interest_rate = interest_rates[country]
    appreciation_rate = appreciation_rates[city]

    monthly_payment, total_mortgage_cost = compute_mortgage_payment(loan_amount, interest_rate, years)
    future_value = estimate_future_value(property_price, appreciation_rate)

    total_cost = total_mortgage_cost + available_capital
    profit_or_loss = future_value - total_cost

    print("\nInvestment Breakdown:")
    print(f"Loan Amount: €{loan_amount}")
    print(f"Monthly Mortgage Payment: €{monthly_payment:.2f}")
    print(f"Total Mortgage Payment over {years} years: €{total_mortgage_cost:.2f}")
    print(f"Expected Property Value in 10 years: €{future_value:.2f}")
    print(f"Total Cost Paid: €{total_cost:.2f}")
    print(f"Projected Profit/Loss: €{profit_or_loss:.2f}")

    if profit_or_loss > 0:
        print("✅ This investment is likely to be profitable!")
    else:
        print("❌ This investment may result in a loss. Consider alternatives.")


# Display supported countries and cities at the beginning
display_supported_options()

# User Input
country = input("Enter the country: ")
city = input("Enter the city: ")
property_price = float(input("Enter the property price (€): "))
available_capital = float(input("Enter your available capital (€): "))

# Choose repayment period
years = 0
while years not in [10, 15, 20]:
    try:
        years = int(input("Choose your loan repayment period (10, 15, or 20 years): "))
        if years not in [10, 15, 20]:
            print("Invalid choice. Please select 10, 15, or 20 years.")
    except ValueError:
        print("Please enter a valid number (10, 15, or 20).")

# Perform Investment Analysis
investment_analysis(country, city, property_price, available_capital, years)
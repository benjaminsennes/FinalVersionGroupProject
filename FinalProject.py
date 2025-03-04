import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

# Data for cities, appreciation rates, and multipliers
city_data = {
    "Madrid": {1000000: 0.04, 2500000: 0.05, 5000000: 0.06},

    "Barcelona": {1000000: 0.03, 2500000: 0.04, 5000000: 0.05},

    "Seville": {1000000: 0.035, 2500000: 0.045, 5000000: 0.055},

    "San Sebastian": {1000000: 0.045, 2500000: 0.055, 5000000: 0.065},

    "Marbella": {1000000: 0.06, 2500000: 0.07, 5000000: 0.08},
             }

location_multiplier = {"Center": 1.09, "Suburb": 1.08}

property_multiplier = {
    "Apartment": {"Center": 1.09, "Suburb": 0.96},
    "House": {"Center": 0.96, "Suburb": 1.08},
                        }
construction_multiplier = {"Bogdan Constructors": 1.1, "Steffen Constructors": 0.95}

worker_multiplier = {2: 0.95, 4: 1.03, 6: 1.09, 8: 1.00}

material_multiplier = {
    "Apartment": {"Modern": 1.03, "Vintage": 1.00, "Countryside": 1.09},

    "House": {"Stone": 1.07, "Wood": 1.04, "Concrete": 1.00},
                        }
bank_interest = {"BBVA": 0.03, "Santander": 0.05}

investment_options = [1000000, 2500000, 5000000]

REQUIRED_ROI = 50  # Minimum required ROI to be hired

def calculate_roi():
    city = city_var.get()
    location = location_var.get()
    property_type = property_type_var.get()
    company = company_var.get()
    workers = int(workers_var.get())
    bank = bank_var.get()
    investment = int(investment_var.get())
    material = material_var.get()

    appreciation_rate = city_data[city][investment] * location_multiplier[location] * \
                        property_multiplier[property_type][location] * construction_multiplier[company] * \
                        worker_multiplier[workers] * material_multiplier[property_type][material]

    interest_rate = bank_interest[bank]
    down_payment = investment * 0.2
    total_loan = investment * 0.8

    total_cost = down_payment + (total_loan * (1 + interest_rate * 4))
    final_value = investment * (1 + appreciation_rate) ** 4
    roi = ((final_value - total_cost) / down_payment) * 100

    # Plot results
    plt.figure(figsize=(7, 5))
    plt.bar(["Your Investment"], [roi], color="blue", label="Your Investment")
    plt.axhline(y=REQUIRED_ROI, color="black", linestyle="--", label="Required ROI")  # Keep only the line

    plt.xlabel("Investment")
    plt.ylabel("ROI (%)")
    plt.title("Investment Return")
    plt.legend()
    plt.grid()
    plt.show()


# GUI Setup
root = tk.Tk()
root.title("Real Estate Investment Simulator")

city_var = tk.StringVar(value="Barcelona")
location_var = tk.StringVar(value="Center")
property_type_var = tk.StringVar(value="Apartment")
company_var = tk.StringVar(value="Bogdan Constructors")
workers_var = tk.StringVar(value="4")
bank_var = tk.StringVar(value="BBVA")
investment_var = tk.StringVar(value="2500000")
material_var = tk.StringVar(value="Modern")

options = [
    ("Choose a city:", city_var, list(city_data.keys())),
    ("Choose location:", location_var, list(location_multiplier.keys())),
    ("Choose property type:", property_type_var, list(property_multiplier.keys())),
    ("Choose construction company:", company_var, list(construction_multiplier.keys())),
    ("Number of Workers:", workers_var, ["2", "4", "6", "8"]),
    ("Choose a bank:", bank_var, list(bank_interest.keys())),
    ("Choose investment amount:", investment_var, ["1000000", "2500000", "5000000"]),
]

for i, (text, var, choices) in enumerate(options):
    ttk.Label(root, text=text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
    ttk.Combobox(root, textvariable=var, values=choices, state="readonly").grid(row=i, column=1, padx=10, pady=5)

# Material selection updates based on property type
material_options = {
    "Apartment": ["Modern", "Vintage", "Countryside"],
    "House": ["Stone", "Wood", "Concrete"],
}

def update_material_options(*args):
    selected_type = property_type_var.get()
    material_var.set(material_options[selected_type][0])
    material_dropdown["values"] = material_options[selected_type]

property_type_var.trace("w", update_material_options)

ttk.Label(root, text="Choose material:").grid(row=len(options), column=0, padx=10, pady=5, sticky='w')
material_dropdown = ttk.Combobox(root, textvariable=material_var, values=material_options["Apartment"], state="readonly")
material_dropdown.grid(row=len(options), column=1, padx=10, pady=5)

ttk.Button(root, text="Simulate Investment", command=calculate_roi).grid(row=len(options) + 1, columnspan=2, pady=10)

root.mainloop()

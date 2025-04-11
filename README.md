# ✈️ Airlines Manager Route Pricing Automation

This Python script automates the task of updating route prices and retrieving simulation results from the [Airlines Manager](https://www.airlines-manager.com/) web interface using Selenium.

It reads routes and their respective pricing from a CSV file, logs into your Airlines Manager account, navigates through the UI, updates each route's prices, runs a simulation, and exports the results to a new CSV file.

---

## 📂 Project Structure
📁 airlines-manager-automation/

├── airline.csv # Input file with routes and pricing (semicolon-separated)

├── airline_updated.csv # Output file with added simulation results

├── script.py # Main automation script

├── .env # Environment variables (email and password)

├── requirements.txt (packages needed to run the code)

└── README.md # This file

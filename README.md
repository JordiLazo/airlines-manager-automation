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


### 🔍 How It Works — Step by Step

1. **Login to Airlines Manager**
   - Automatically logs in [Airlines Manager](https://www.airlines-manager.com/) using credentials stored securely in the `.env` file.
   - Accepts cookie consent messages if prompted.

2. **Read Routes and Prices from CSV**
   - Loads data from `airline.csv`, which contains routes and their respective prices for Economy, Business, First Class, and Cargo.

3. **Select Route via Dropdown Menu**
   - It selects all routes that are available.
   <img src="/images/all_routes.png" alt="all routes available" width="300" height="300"/>


4. **Update Route Prices**
   - Clicks the "Precios de la ruta" (Route Prices) button to open the price input screen.
   - Clears existing values in input fields (Economy, Business, First Class, Cargo) using `.clear()`.
   - Inserts new values from the CSV using `.send_keys()`.

5. **Run Simulation**
   - Clicks the "Run Simulation" button (`ID: priceSimulation`) to simulate how many passengers/cargo units would book at the new prices.
   - Waits for the simulation results to appear on the page.

6. **Extract Simulation Results**
   - Retrieves the output values for:
     - `paxEcoValue`
     - `paxBusValue`
     - `paxFirstValue`
     - `paxCargoValue`
   - These represent the expected number of passengers or cargo for each class.
   - Adds these values to the in-memory dictionary along with the original prices.

7. **Save Updated Data**
   - Writes everything to a new CSV file `airline_updated.csv`.
   - The output includes:
     - Route name
     - Input prices
     - Simulated demand for each class

8. **Crash-Safe Writing**
   - After each route is processed, the CSV file is updated.
   - If the script crashes or fails mid-run, partial results are still saved.

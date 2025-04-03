from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

def main():
    # Define input and output CSV files
    input_file = "airline.csv"  
    output_file = "airline_updated.csv"  # New file to save updated data

    # Define the dictionary keys
    keys = ["line_priceEco", "line_priceBus", "line_priceFirst", "line_priceCargo"]
    sim_keys = ["paxEcoValue", "paxBusValue", "paxFirstValue", "paxCargoValue"]  # Keys for simulation results

    # Process the CSV and store data in a dictionary
    nested_dict = {}

    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader)  # Read the header
        
        for row in reader:
            if row:  # Skip empty lines
                route = row[0]
                values = row[1:5]  # Extract the prices
                nested_dict[route] = {key: value for key, value in zip(keys, values)}
    
    # Initialize Chrome driver
    driver = webdriver.Chrome()
    try:
        # Open the main page
        driver.get("https://www.airlines-manager.com/network/")
        email = os.getenv("AIRLINE_EMAIL")
        password = os.getenv("AIRLINE_PASSWORD")
        # Accept the cookie banner in French (message: "Compris !")
        try:
            cookie_accept = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'cc-dismiss') and contains(., 'Compris')]"))
            )
            cookie_accept.click()
            print("Cookie message (Compris!) accepted.")
        except Exception as e:
            print("Cookie message not found or already accepted:", e)

        # Login: wait for username and password fields
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys(email)

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        try:
            login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button.click()
        except Exception:
            password_field.send_keys(Keys.RETURN)

        # Accept cookies after login
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Consent')]"))
            )
            consent_button.click()
            print("Cookies accepted with 'Consent' button.")  
        except Exception as e:
            print("Consent button not found:", e)

        # Navigate to "Network Management" menu
        menu_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "picto2"))
        )
        menu_link.click()
        print("'Network Management' menu accessed.")
        
        # Process each route in the dictionary
        for route_index, (selected_route, route_prices) in enumerate(nested_dict.items()):
            print(f"\n[{route_index + 1}/{len(nested_dict)}] Processing route: {selected_route}")
            
            try:
                # Navigate to network page if not on first iteration (return to route selection)
                if route_index > 0:
                    # Navigate back to the network page
                    network_menu = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/network/')]"))
                    )
                    network_menu.click()
                    print("Returned to network management page.")
                    time.sleep(2)  # Wait for page to load
                
                # Select the route from dropdown
                select_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.linePicker"))
                )
                select_obj = Select(select_element)
                select_obj.select_by_visible_text(selected_route)
                print(f"Option '{selected_route}' selected.")

                # Wait for the selection to process and the redirect
                time.sleep(3)

                # Click on the "Route Prices" button
                pricing_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'gradientButtonPurple') and contains(., 'Precios de la ruta')]"))
                )
                pricing_button.click()
                print("'Route Prices' button clicked.")
                
                # Wait for the pricing page to load and locate fare inputs
                price_eco = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "line_priceEco"))
                )
                price_bus = driver.find_element(By.ID, "line_priceBus")
                price_first = driver.find_element(By.ID, "line_priceFirst")
                price_cargo = driver.find_element(By.ID, "line_priceCargo")

                # Clear existing values and set new values from dictionary
                price_eco.clear()
                price_eco.send_keys(route_prices["line_priceEco"])
                
                price_bus.clear()
                price_bus.send_keys(route_prices["line_priceBus"])
                
                price_first.clear()
                price_first.send_keys(route_prices["line_priceFirst"])
                
                price_cargo.clear()
                price_cargo.send_keys(route_prices["line_priceCargo"])
                
                print(f"Values for route {selected_route} updated:")
                print("line_priceEco:", route_prices["line_priceEco"])
                print("line_priceBus:", route_prices["line_priceBus"])
                print("line_priceFirst:", route_prices["line_priceFirst"])
                print("line_priceCargo:", route_prices["line_priceCargo"])
                
                # Click on the "Run simulation" button instead of saving
                try:
                    simulation_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "priceSimulation"))
                    )
                    simulation_button.click()
                    print("'Run simulation' button clicked.")
                    
                    # Wait for simulation results to appear
                    time.sleep(3)
                    
                    # Extract the simulated passenger values
                    pax_eco = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "paxEcoValue"))
                    ).text
                    pax_bus = driver.find_element(By.ID, "paxBusValue").text
                    pax_first = driver.find_element(By.ID, "paxFirstValue").text
                    pax_cargo = driver.find_element(By.ID, "paxCargoValue").text
                    
                    # Store the simulated values in the dictionary
                    nested_dict[selected_route]["paxEcoValue"] = pax_eco
                    nested_dict[selected_route]["paxBusValue"] = pax_bus
                    nested_dict[selected_route]["paxFirstValue"] = pax_first
                    nested_dict[selected_route]["paxCargoValue"] = pax_cargo
                    
                    print(f"Simulation values for route {selected_route} obtained:")
                    print("paxEcoValue:", pax_eco)
                    print("paxBusValue:", pax_bus)
                    print("paxFirstValue:", pax_first)
                    print("paxCargoValue:", pax_cargo)
                    
                    # Write the current data to CSV after each route (in case of crash)
                    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        
                        # Write header
                        header = ['route'] + keys + sim_keys
                        writer.writerow(header)
                        
                        # Write data
                        for route, values in nested_dict.items():
                            row = [route]
                            for key in keys + sim_keys:
                                row.append(values.get(key, ''))  # Use empty string if key doesn't exist
                            writer.writerow(row)
                        
                        print(f"Updated data saved to {output_file} after processing route {selected_route}")
                    
                except Exception as e:
                    print(f"Error running simulation for route {selected_route}:", e)
                    
            except Exception as e:
                print(f"Error processing route {selected_route}:", e)
                continue  # Continue with the next route even if this one fails
        
        print("\nAll routes processed successfully.")

    except Exception as e:
        print("Error during execution:", e)
    finally:
        # Uncomment the line below to close the browser when finished
        # driver.quit()
        print("Script execution completed. Browser left open for verification.")

if __name__ == "__main__":
    main()

import datetime
import csv
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

def get_gold_price():
    gold_price = float(input("Enter the current gold price in IRR per gram: "))
    return gold_price

def get_dollar_price():
    dollar_price = float(input("Enter the current dollar price in IRR: "))
    return dollar_price

def save_to_csv(gold_price, dollar_price, current_time):
    # Save data to a CSV file in append mode
    with open('prices.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, gold_price, dollar_price])
    print("Prices saved to prices.csv")

def display_prices():
    gold_price = get_gold_price()
    dollar_price = get_dollar_price()
    current_time = datetime.datetime.now()

    print(f"At {current_time}, the gold price is {gold_price} IRR per gram and the dollar price is {dollar_price} IRR.")
    save_to_csv(gold_price, dollar_price, current_time)

def view_historical_data():
    try:
        data = pd.read_csv('prices.csv', header=None, names=['Timestamp', 'Gold Price (IRR)', 'Dollar Price (IRR)'])
        print(data)
    except FileNotFoundError:
        print("No historical data found. Please add some data first.")

def predict_prices():
    try:
        # Read the CSV file and check if it has enough data
        data = pd.read_csv('prices.csv', header=None, names=['Timestamp', 'Gold Price (IRR)', 'Dollar Price (IRR)'])
        
        # Convert the 'Timestamp' column to datetime, and set it as the index
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], errors='coerce')
        data.set_index('Timestamp', inplace=True)

        # Print the data to debug the issue
        print("Loaded Data:\n", data)

        # Remove rows where any values are missing or invalid
        data.dropna(inplace=True)

        # Ensure the data has enough valid rows
        if len(data) < 5:
            print("Not enough data to make a prediction. Please add more data points.")
            return

        # Use a simple moving average to predict the next 5 hours
        gold_moving_avg = data['Gold Price (IRR)'].rolling(window=3).mean().iloc[-1]
        dollar_moving_avg = data['Dollar Price (IRR)'].rolling(window=3).mean().iloc[-1]

        print(f"Predicted Gold Price for the next 5 hours: {gold_moving_avg}")
        print(f"Predicted Dollar Price for the next 5 hours: {dollar_moving_avg}")

    except FileNotFoundError:
        print("No historical data found. Please add some data first.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    choice = input("Enter '1' to add new prices, '2' to view historical data, or '3' to predict future prices: ")

    if choice == '1':
        display_prices()
    elif choice == '2':
        view_historical_data()
    elif choice == '3':
        predict_prices()
    else:
        print("Invalid choice.")

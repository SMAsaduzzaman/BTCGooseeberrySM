import time
import threading
from datetime import datetime, timedelta
import telebot
import MetaTrader5 as mt5
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from model import create_and_train_model
from place_buy_order import place_buy_order
from place_sell_order import place_sell_order
from collect_data import collect_data

# Replace 'YOUR_API_TOKEN' with the API token you received from the BotFather
API_TOKEN = "**********************"
CHAT_ID = '-***********'  # Your actual channel ID

bot = telebot.TeleBot(API_TOKEN)

# Flags to control message sending and thread stopping
send_messages = True  # Changed to True to start sending messages immediately
stop_thread = threading.Event()

# Function to send a Telegram message with retry mechanism
def send_telegram_message(actual_price, predicted_price, execution_time, trading_time):
    message = (f"Actual price: {actual_price}\n"
               f"Predicted price in 5 minutes: {predicted_price}\n"
               f"Model training execution time: {execution_time:.2f} seconds\n"
               f"Trading execution time: {trading_time:.2f} seconds")
    print(f"Sending message: {message}")
    success = False
    attempts = 0
    while not success and attempts < 5:  # Retry up to 5 times
        try:
            bot.send_message(chat_id=CHAT_ID, text=message)
            success = True
        except Exception as e:
            print(f"Failed to send message (attempt {attempts + 1}): {e}")
            attempts += 1
            time.sleep(5)  # Wait for 5 seconds before retrying

# Initialize MetaTrader 5 connection
print("Initializing MetaTrader 5...")
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

print("MetaTrader 5 initialized successfully.")

# Account details
account_details = {
    "login": 51840831,
    "password": "Cs&7m&XBPt8dDe",
    "server": "ICMarketsSC-Demo",
}

# Login to the account
print("Logging into MetaTrader 5 account...")
if not mt5.login(login=account_details["login"], password=account_details["password"], server=account_details["server"]):
    print(f"Failed to login to account {account_details['login']}: {mt5.last_error()}")
    mt5.shutdown()
    quit()

print("Logged into MetaTrader 5 account successfully.")

# Load scaler
scaler = MinMaxScaler(feature_range=(0, 1))

# Define symbol and timeframe
symbol = "BTCUSD"
timeframe = mt5.TIMEFRAME_M5  # 5-minute intervals

def calculate_sleep_time_until_next_divisible_by_5():
    now = datetime.now()
    # Calculate the number of minutes to add to reach the next minute divisible by 5
    minutes_to_add = (5 - now.minute % 5)
    next_run = now + timedelta(minutes=minutes_to_add)
    next_run = next_run.replace(second=0, microsecond=0)

    # Calculate sleep time
    sleep_time = (next_run - now).total_seconds()
    print(f"Sleep time until the next minute divisible by 5: {sleep_time} seconds")
    return sleep_time

def predict_and_trade():
    global send_messages, stop_thread
    print("Started predict_and_trade function")
    while not stop_thread.is_set():
        if send_messages:
            print("Predicting and trading")
            data = collect_data(symbol, timeframe, 5000)  # Collect 5000 records
            if data is None:
                time.sleep(600)  # Sleep for 10 minutes if there's an error
                continue

            # Scale data
            data['close'] = scaler.fit_transform(data['close'].values.reshape(-1, 1))

            # Train the model
            model, execution_time = create_and_train_model(data)

            # Create input for prediction
            X_input = data['close'].values[-10:].reshape(1, -1, 1)  # Last 10 data points

            # Predict closing price
            predicted_price_scaled = model.predict(X_input)
            predicted_price = float(scaler.inverse_transform(predicted_price_scaled)[0][0])
            print(type(predicted_price))

            # Calculate sleep time until the next 5-minute mark
            sleep_time = calculate_sleep_time_until_next_divisible_by_5()
            time.sleep(sleep_time)

            # Collect actual data to compare with prediction
            latest_data = collect_data(symbol, timeframe, 1)  # Collect the latest 1 record
            actual_next_price = float(latest_data['close'][0])

            # Determine order type based on prediction
            start_trading_time = time.time()
            if predicted_price > actual_next_price:
                result = place_buy_order(predicted_price)
            else:
                result = place_sell_order(predicted_price)
            trading_execution_time = time.time() - start_trading_time

            if result:
                print(result.comment)
                print(f"Order placed successfully: {result}")
            else:
                print("Order placement failed")

            # Send Telegram message
            send_telegram_message(actual_next_price, predicted_price, execution_time, trading_execution_time)
        else:
            print("Messages are currently stopped")
            while not send_messages and not stop_thread.is_set():
                time.sleep(1)  # Wait for the start_sending command or stop_thread to become True

# Function to start the bot and schedule tasks
def start_bot():
    thread = threading.Thread(target=predict_and_trade)
    thread.daemon = True  # Ensure thread will close when main program exits
    thread.start()
    print("Background thread started")

# Start the bot
start_bot()

# Start polling for bot commands
bot.polling(none_stop=True, interval=0, timeout=20)

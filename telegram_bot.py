import telebot

# Replace 'YOUR_API_TOKEN' with the API token you received from the BotFather
API_TOKEN = "6769941954:AAHulChi9Wbjo9yhO0gTrLX3ZJ9ftS_eJQc"
CHAT_ID = '1093879901'  # Your actual chat ID

bot = telebot.TeleBot(API_TOKEN)

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print("Received /start or /help command")
    bot.reply_to(message, "Welcome to YourBot! Type /info to get more information. Use /start_sending to start and /stop_sending to stop messages.")

@bot.message_handler(commands=['info'])
def send_info(message):
    print("Received /info command")
    bot.reply_to(message, "This is a simple Telegram bot implemented in Python.")

# Command to start sending messages
@bot.message_handler(commands=['start_sending'])
def start_sending(message):
    global send_messages
    send_messages = True
    print("Started sending messages")
    bot.reply_to(message, "Started sending messages.")

# Command to stop sending messages
@bot.message_handler(commands=['stop_sending'])
def stop_sending(message):
    global send_messages
    send_messages = False
    print("Stopped sending messages")
    bot.reply_to(message, "Stopped sending messages.")

# Command to stop the system
@bot.message_handler(commands=['stop_sys'])
def stop_system(message):
    global stop_thread
    stop_thread.set()
    print("Stopped the system")
    bot.reply_to(message, "Stopped sending messages.")
    mt5.shutdown()
    sys.exit()

# Define a message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"Echoing message: {message.text}")
    bot.reply_to(message, message.text)

def send_telegram_message(actual_price, predicted_price, execution_time):
    message = f"Actual price: {actual_price}\nPredicted price in 5 minutes: {predicted_price}\nModel training execution time: {execution_time:.2f} seconds"
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

# BTCUSD Prediction with LSTM and MetaTrader 5 Integration

This repository contains a project to predict BTCUSD prices using an LSTM model and automate trading decisions using MetaTrader 5. The LSTM model is trained on historical BTCUSD data, and trading actions are executed based on the model's predictions.

## Project Structure

- `main.py`: The main script that integrates data collection, prediction, and trading.
- `collect_data.py`: Script to collect historical BTCUSD data from MetaTrader 5.
- `place_buy_order.py`: Script to place a buy order on MetaTrader 5.
- `place_sell_order.py`: Script to place a sell order on MetaTrader 5.
- `model.py`: Script for building, training, and hyperparameter tuning of the LSTM model.
- `btc_usd_data.csv`: The historical BTCUSD data file. That will be updated regularly with real-time data

## Requirements

- Python 3.8+
- TensorFlow 2.4+
- MetaTrader 5
- pandas
- numpy
- scikit-learn
- keras-tuner
- pyTelegramBotAPI

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/btcusd-prediction.git
    cd btcusd-prediction
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **MetaTrader 5 Setup**:
    - Ensure MetaTrader 5 is installed and configured.
    - Update `account_details` in `main.py` with your MetaTrader 5 account details.

4. **Telegram Bot Setup**:
    - Create a new bot using BotFather on Telegram and get the API token.
    - Update `API_TOKEN` and `CHAT_ID` in `main.py` with your Telegram bot token and chat ID.

5. **Prepare Data**:
    - Place your BTCUSD historical data file (`btc_usd_data.csv`) in the project directory.

## Usage

1. **Run the main script**:
    ```sh
    python main.py
    ```

2. **Telegram Commands**:
    - `/start` or `/help`: Get information about the bot.
    - `/start_sending`: Start sending messages.
    - `/stop_sending`: Stop sending messages.
    - `/stop_sys`: Stop the system and shutdown MetaTrader 5.

## Hyperparameter Tuning

The `model.py` script includes hyperparameter tuning using `keras-tuner`. The optimal hyperparameters are found and the best model is saved as `best_lstm_btcusd_model.h5`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MetaTrader 5](https://www.metatrader5.com/)
- [TensorFlow](https://www.tensorflow.org/)
- [Keras Tuner](https://keras.io/keras_tuner/)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

## Contact

For any questions or suggestions, feel free to open an issue or contact me at [smasaduzzaman95@gmail.com](mailto:smasaduzzaman95@gmail.com).

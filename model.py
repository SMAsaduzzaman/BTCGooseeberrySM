import time
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import numpy as np

def create_and_train_model(data, seq_length=10, batch_size=2, epochs=10):
    def create_sequences(data, seq_length):
        sequences = []
        for i in range(len(data) - seq_length):
            sequence = data[i:i + seq_length]
            label = data[i + seq_length]
            sequences.append((sequence, label))
        return sequences

    sequences = create_sequences(data['close'].values, seq_length)

    train_size = int(len(sequences) * 0.8)
    train_sequences = sequences[:train_size]
    test_sequences = sequences[train_size:]

    X_train, y_train = zip(*train_sequences)
    X_test, y_test = zip(*test_sequences)

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)

    print("Data preprocessed")

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Build LSTM model
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dense(80))
    model.add(Dense(80))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    start_time = time.time()
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Model training execution time: {execution_time:.2f} seconds")

    # model.save('lstm_btcusd_model.h5')
    # print("Model trained and saved")

    return model, execution_time
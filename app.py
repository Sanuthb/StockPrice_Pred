from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('keras_model.h5')

# MinMaxScaler for scaling input data
scaler = MinMaxScaler(feature_range=(0, 1))

# Function to load data from Yahoo Finance
def load_data(ticker, start="2010-01-01", end=None):
    try:
        # Fetch the data using yfinance
        data = yf.download(ticker, start=start, end=end)
        
        # Check if data is empty
        if data.empty:
            raise ValueError(f"No data found for ticker: {ticker}. Please check the ticker or date range.")
        
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Function to prepare data for prediction
def prepare_data(data, look_back=100):
    data_scaled = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
    x_test = []
    for i in range(look_back, len(data_scaled)):
        x_test.append(data_scaled[i-look_back:i])
    return np.array(x_test), scaler

# Function to predict stock prices
def predict_stock(data, model, look_back=100):
    x_test, scaler = prepare_data(data, look_back)
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    return predictions

# Function to evaluate stock recommendation
def evaluate_stock(data, predictions):
    # Get the last actual and predicted prices
    last_actual_price = data['Close'].values[-1]
    last_predicted_price = predictions[-1][0]
    
    # Define a threshold for decision making (e.g., 5% difference)
    threshold = 0.05 * last_actual_price  # 5% of the last actual price
    
    if last_predicted_price > last_actual_price + threshold:
        return "Buy"
    elif last_predicted_price < last_actual_price - threshold:
        return "Sell"
    else:
        return "Hold"

# Home route for serving the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Route to predict stock prices
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get stock ticker and date range from request
        req_data = request.get_json()
        ticker = req_data.get('ticker', 'TCS.NS')
        start_date = req_data.get('start', '2010-01-01')
        end_date = req_data.get('end', None)

        # Load stock data
        data = load_data(ticker, start_date, end_date)
        
        if data.empty:
            return jsonify({"error": f"No data found for ticker {ticker}. Please check the ticker and date range."})

        # Predict stock prices
        predictions = predict_stock(data, model)

        # Prepare response
        response = {
            "ticker": ticker,
            "predicted_prices": predictions[-10:].flatten().tolist(),  # Last 10 predicted prices
            "original_prices": data['Close'].values[-10:].tolist()  # Last 10 actual prices
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to recommend buy/sell/hold
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get stock ticker and date range from request
        req_data = request.get_json()
        ticker = req_data.get('ticker', 'TCS.NS')
        start_date = req_data.get('start', '2010-01-01')
        end_date = req_data.get('end', None)

        # Load stock data
        data = load_data(ticker, start_date, end_date)
        
        if data.empty:
            return jsonify({"error": f"No data found for ticker {ticker}. Please check the ticker and date range."})

        # Predict stock prices
        predictions = predict_stock(data, model)

        # Calculate recommendation based on last price
        last_actual_price = data['Close'].values[-1]
        last_predicted_price = predictions[-1][0]  # Use the last predicted price
        recommendation = (
            "Buy" if last_predicted_price > last_actual_price else
            "Sell" if last_predicted_price < last_actual_price else
            "Hold"
        )

        # Prepare response
        response = {
            "ticker": ticker,
            "recommendation": recommendation,
            "last_actual_price": float(last_actual_price),  # Convert to float for JSON
            "last_predicted_price": float(last_predicted_price)  # Convert to float for JSON
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to fetch stock details for a fixed list of stocks
@app.route('/fetch_stocks', methods=['GET'])
def fetch_stocks():
    try:
        # List of fixed popular stocks
        popular_stocks = [
            "AAPL", "GOOGL", "AMZN", "MSFT", "TSLA",
            "NFLX", "META", "NVDA", "BABA", "V",
            "JPM", "DIS", "INTC", "PYPL", "PEP",
            "CSCO", "KO", "NKE", "MCD", "ADBE"
        ]

        # Initialize an empty list for stock data
        stock_data = []

        # Fetch actual and predicted prices for each stock
        for ticker in popular_stocks:
            # Load stock data
            data = load_data(ticker, start="2023-01-01")
            
            if data.empty:
                continue

            # Predict stock prices
            predictions = predict_stock(data, model)

            # Get the last 10 actual and predicted prices
            actual_prices = data['Close'].values[-10:]
            predicted_prices = predictions[-10:].flatten()
            dates = data['Date'].dt.strftime('%Y-%m-%d').values[-10:]

            # Append stock details to the list
            stock_data.append({
                "ticker": ticker,
                "details": [
                    {
                        "Date": dates[i], 
                        "Actual Price": float(actual_prices[i]),  # Convert numpy value to float
                        "Predicted Price": float(predicted_prices[i])  # Convert numpy value to float
                    }
                    for i in range(len(dates))
                ]
            })

        # Return JSON response
        return jsonify({"stocks": stock_data})
    except Exception as e:
        return jsonify({"error": str(e)})


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)

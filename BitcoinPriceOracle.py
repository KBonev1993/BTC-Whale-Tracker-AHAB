import requests
import pandas as pd
import logging
from textblob import TextBlob

def get_transactions(limit):
    """Get the latest transactions from the blockchain explorer API."""
    try:
        url = f"https://blockchain.info/unconfirmed-transactions?format=json&limit={limit}"
        response = requests.get(url)
        transactions = response.json()["txs"]
        return transactions
    except Exception as e:
        logging.error(f"Error while retrieving transactions: {e}")
        # Try a different API or raise an error to stop the processing
        raise e

def filter_whale_transactions(transactions, threshold):
    """Filter transactions based on their size to identify whale activity."""
    whale_transactions = [tx for tx in transactions if tx["size"] >= threshold]
    return whale_transactions

def analyze_transactions(whale_transactions):
    """Analyze the filtered transactions to identify patterns and correlations."""
    addresses = [tx["inputs"][0]["prev_out"]["addr"] for tx in whale_transactions]
    # Additional analysis can be performed here, such as frequency analysis and market simulation
    address_series = pd.Series(addresses, dtype=str)
    frequent_addresses = address_series[address_series.duplicated()].tolist()
    return frequent_addresses

def predict_market_movements(addresses):
    """Predict future market movements based on the analyzed transactions."""
    sentiment = 0
    for address in addresses:
        analysis = TextBlob(address)
        sentiment += analysis.sentiment[0]

    if sentiment >= 0:
        prediction = "Positive"
    else:
        prediction = "Negative"

    return prediction

def track_whale_activity(limit, threshold):
    """Main function to track crypto whale activity."""
    if limit <= 0:
        raise ValueError("Limit must be a positive integer")
    if threshold <= 0:
        raise ValueError("Threshold must be a positive integer")

    transactions = get_transactions(limit)
    whale_transactions = filter_whale_transactions(transactions, threshold)
    addresses = analyze_transactions(whale_transactions)
    prediction = predict_market_movements(addresses)
    return prediction

# Example usage
try:
    result = track_whale_activity(1000000, 10000000)
    print(result)
except Exception as e:
    logging.error(f"Error while tracking whale activity: {e}")

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def fetch_coin_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {'vs_currency': 'usd', 'days': days}
    response = requests.get(url, params=params)
    return response.json()

def fetch_coin_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    try:
        coin_data = response.json()
        if isinstance(coin_data, list) and 'id' in coin_data[0] and 'name' in coin_data[0]:
            return {coin['id']: coin['name'] for coin in coin_data}
        else:
            st.error("Unexpected data format received from CoinGecko API. Please check the API or try later.")
            return {}
    except ValueError:
        st.error("Failed to decode JSON from response. Check the URL and try again.")
        return {}
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return {}


def plot_comparison_data(data1, data2, coin1, coin2):
    df1 = pd.DataFrame(data1['prices'], columns=['date', 'price'])
    df1['date'] = pd.to_datetime(df1['date'], unit='ms')
    df1.set_index('date', inplace=True)
    
    df2 = pd.DataFrame(data2['prices'], columns=['date', 'price'])
    df2['date'] = pd.to_datetime(df2['date'], unit='ms')
    df2.set_index('date', inplace=True)
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df1.index, df1['price'], label=f'{coin1} Price')
    plt.plot(df2.index, df2['price'], label=f'{coin2} Price')
    plt.title('Price Comparison Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return plt

# Streamlit user interface for comparison
st.title('Cryptocurrency Price Comparison Tracker')

# Load coin data
coins = fetch_coin_list()
coin1 = st.selectbox('Select the first cryptocurrency', options=list(coins.values()))
coin2 = st.selectbox('Select the second cryptocurrency', options=list(coins.values()), index=1)
time_frame = st.selectbox('Select the time frame', options=['7', '30', '365', '1825'], format_func=lambda x: {'7': '1 week', '30': '1 month', '365': '1 year', '1825': '5 years'}[x])

if coin1 and coin2:
    coin_id1 = [key for key, value in coins.items() if value == coin1][0]
    coin_id2 = [key for key, value in coins.items() if value == coin2][0]
    data1 = fetch_coin_data(coin_id1, time_frame)
    data2 = fetch_coin_data(coin_id2, time_frame)
    fig = plot_comparison_data(data1, data2, coin1, coin2)
    st.pyplot(fig)

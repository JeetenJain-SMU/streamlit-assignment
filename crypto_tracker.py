import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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

def fetch_coin_data(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {'vs_currency': 'usd', 'days': days}
    response = requests.get(url, params=params)
    return response.json()

def plot_price_data(data):
    df = pd.DataFrame(data['prices'], columns=['date', 'price'])
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True)
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['price'], label='Price')
    plt.title('Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return plt, df

# Streamlit user interface
st.title('Cryptocurrency Price Tracker')

# Load coin data
coins = fetch_coin_list()
if coins:
    coin_name = st.selectbox('Select a cryptocurrency', options=list(coins.values()))

    if coin_name:
        coin_id = [key for key, value in coins.items() if value == coin_name][0]
        data = fetch_coin_data(coin_id)
        fig, df = plot_price_data(data)
        st.pyplot(fig)
        
        # Displaying max and min price details
        max_price = df['price'].max()
        min_price = df['price'].min()
        max_date = df[df['price'] == max_price].index[0].strftime('%Y-%m-%d')
        min_date = df[df['price'] == min_price].index[0].strftime('%Y-%m-%d')
        
        st.write(f"Maximum price of {max_price} USD on {max_date}")
        st.write(f"Minimum price of {min_price} USD on {min_date}")

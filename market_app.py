import streamlit as st
import yfinance as yf
import requests
import time

st.set_page_config(page_title="Market Sentiment Tracker", page_icon="📈")

def get_vix_data():
    try:
        vix = yf.Ticker("^VIX")
        # Getting latest price
        val = vix.history(period="1d")['Close'].iloc[-1]
        return round(val, 2)
    except:
        return 0.0

def get_fear_greed():
    """"Fetches Fear & Greed index from an alternative public API cuz CNN sucks and I cant be fucked to scrape from their site directly lol"""
    # Below is on Dataviz but its connected to CNN so should be okay to use indefinitely.
    # For the exact CNN Stock index, we use the production endpoint with headers
    try:
        cnn_url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        res = requests.get(cnn_url, headers=headers, timeout=5)
        return round(res.json()['fear_and_greed']['score'], 1)
    except:
        return None

# --- UI Header ---
st.title("📊 Market Sentiment at a glance")
st.markdown("This app monitors the **VIX** and **CNN Fear & Greed** to find extreme panic. When the VIX shoots above 25 and the F&G Index dips below 25, it tends to indicate the bottom of a bear run, meaning potential for buy opportunities")

vix_val = get_vix_data()
fng_val = get_fear_greed()

col1, col2 = st.columns(2)

with col1:
    st.metric(label="VIX (Volatility Index)", value=vix_val)
    if vix_val > 25:
        st.warning("⚠️ High Volatility Detected")

with col2:
    if fng_val is not None:
        st.metric(label="Fear & Greed Index", value=fng_val)
        if fng_val < 25:
            st.error("😨 Extreme Fear Detected")
    else:
        st.error("Could not fetch CNN data. (The site may be blocking the request).")

st.divider()

# --- SIGNAL LOGIC ---
st.header("🎯 Trading Signal")

if fng_val is not None:
    if vix_val > 25 and fng_val < 25:
        st.success("🔥 **BUY Signal: CAPITULATION**")
        st.write("Both indicators are at extreme levels. Historically, this is a reversal signal.")
        st.balloons() # Added some flair for the buy signal lol
    else:
        st.info("No extreme signal detected. Current status: 'Wait and See'")
else:
    st.info("Waiting for sentiment data...")

st.caption("Data provided by Yahoo Finance and CNN Business.")

# --- REFRESH ---
# This tells the user the site is waiting
st.write("---")
st.caption("Data refreshes every 10 minutes")

# Wait for 600 seconds, then rerun the app
time.sleep(600)
st.rerun()


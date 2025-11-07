"""
Test script for live stock price fetching
Run this to verify yfinance is working before launching Streamlit
"""

import yfinance as yf
from datetime import datetime

def test_live_price_feed():
    """Test if we can fetch UHS stock price"""
    print("=" * 60)
    print("TESTING LIVE STOCK PRICE FEED")
    print("=" * 60)

    try:
        print("\n📡 Fetching UHS stock price from Yahoo Finance...")
        stock = yf.Ticker("UHS")
        data = stock.history(period="1d")

        if not data.empty:
            current_price = round(data['Close'].iloc[-1], 2)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\n✅ SUCCESS!")
            print(f"🏥 UHS Current Price: ${current_price:.2f}")
            print(f"⏰ Fetched at: {timestamp}")
            print(f"📊 Volume: {data['Volume'].iloc[-1]:,.0f}")
            print(f"📈 Day High: ${data['High'].iloc[-1]:.2f}")
            print(f"📉 Day Low: ${data['Low'].iloc[-1]:.2f}")

            # Calculate upside
            fair_value = 410  # Updated weighted average
            upside = ((fair_value - current_price) / current_price) * 100
            print(f"\n💰 VALUATION SUMMARY:")
            print(f"   Current Price: ${current_price:.2f}")
            print(f"   Fair Value: ${fair_value:.2f}")
            print(f"   Upside: +{upside:.1f}%")

            return True
        else:
            print("\n❌ ERROR: No data returned from Yahoo Finance")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n⚠️  If yfinance is not installed, run:")
        print("   pip install yfinance")
        return False

if __name__ == "__main__":
    test_live_price_feed()
    print("\n" + "=" * 60)
    print("If successful, your Streamlit app will fetch live prices!")
    print("=" * 60)

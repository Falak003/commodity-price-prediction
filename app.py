import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import finnhub
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import base64
from streamlit import cache_data
# from dotenv import load_dotenv  # Commented out to avoid dotenv error if not installed

# Load environment variables from .env file
load_dotenv()

# Uncomment the next line if you have python-dotenv installed and want to use .env
# load_dotenv()

# Set page config
st.set_page_config(
    page_title="Commodity Price Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for two-tone green theme and gold text
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background: linear-gradient(135deg, #123524 0%, #1C352D 100%) !important;
        color: #f5d76e !important;
    }
    .main {
        background: linear-gradient(135deg, #123524 0%, #1C352D 100%) !important;
        color: #f5d76e !important;
        padding: 2rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #1C352D !important;
        color: #f5d76e !important;
    }
    .stButton>button {
        background-color: #f5d76e;
        color: #123524;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        width: 100%;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(245,215,110,0.15);
    }
    .stButton>button:hover {
        background-color: #fff2b2;
        color: #123524;
        transform: translateY(-2px);
    }
    .welcome-popup {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(18,53,36,0.95);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .welcome-popup-content {
        background: #1C352D;
        color: #f5d76e;
        padding: 2.5rem 3rem;
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #f5d76e;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .header-sub {
        font-size: 1.1rem;
        color: #f5d76e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .commodity-emojis {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 1.5rem;
        color: #f5d76e;
    }
    .signup-container {
        background: #1C352D;
        border-radius: 18px;
        padding: 2rem 2.5rem 2.5rem 2.5rem;
        margin: 2rem auto 0 auto;
        max-width: 420px;
        box-shadow: 0 4px 24px rgba(18,53,36,0.15);
        color: #f5d76e;
    }
    .signup-btn {
        background: #f54e4e;
        color: #fff;
        border: none;
        border-radius: 2rem;
        width: 100%;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.8rem 0;
        margin: 1.2rem 0 1rem 0;
        cursor: pointer;
        transition: background 0.2s;
    }
    .signup-btn:hover {
        background: #ff7b7b;
    }
    .signup-divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #f5d76e;
        margin: 1.5rem 0 1rem 0;
    }
    .signup-divider::before, .signup-divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #f5d76e;
    }
    .signup-divider:not(:empty)::before {
        margin-right: .75em;
    }
    .signup-divider:not(:empty)::after {
        margin-left: .75em;
    }
    .social-btn {
        display: flex;
        align-items: center;
        background: #fff;
        color: #222;
        border-radius: 2rem;
        padding: 0.7rem 1rem;
        margin-bottom: 0.7rem;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        width: 100%;
        cursor: pointer;
        transition: background 0.2s;
        text-decoration: none;
    }
    .social-btn img {
        height: 1.5rem;
        margin-right: 1rem;
    }
    .social-btn:hover {
        background: #f5d76e;
        color: #123524;
    }
    .stAlert, .stInfo, .stWarning, .stSuccess, .stError {
        color: #f5d76e !important;
    }
    .commodity-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.7rem;
    }
    .commodity-img {
        width: 38px;
        height: 38px;
        border-radius: 8px;
        margin-right: 14px;
        transition: transform 0.2s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        object-fit: cover;
    }
    .commodity-img:hover {
        transform: scale(1.35);
        z-index: 2;
    }
    .about-heading {
        color: #f5d76e;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1.2rem;
    }
    .hover-img {
        transition: transform 0.2s;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        width: 38px;
        height: 38px;
        object-fit: cover;
        margin-right: 14px;
        vertical-align: middle;
    }
    .hover-img:hover {
        transform: scale(1.35);
        z-index: 2;
    }
    </style>
    """, unsafe_allow_html=True)

# Add custom CSS to style st.info and st.success messages with gold text
st.markdown('''
<style>
.stAlert, .stInfo, .stSuccess, .stWarning, .stError {
    color: #f5d76e !important;
    font-size: 1.1rem !important;
}
</style>
''', unsafe_allow_html=True)

# Add custom CSS for golden border and remove spread
st.markdown('''
<style>
.commodity-cards {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: flex-start;
    gap: 1.2rem;
    margin: 2rem 0;
    width: 100%;
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 1.5rem;
}
.commodity-card {
    background: linear-gradient(135deg, #123524 0%, #1C352D 100%);
    border-radius: 24px;
    box-shadow: 0 2px 12px 0 rgba(44,62,80,0.10);
    border: 3px solid #f5d76e;
    width: 250px;
    min-width: 220px;
    max-width: 270px;
    height: 170px;
    min-height: 150px;
    max-height: 200px;
    padding: 1.1rem 1.1rem 0.7rem 1.1rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
    box-sizing: border-box;
    margin: 0;
    flex-shrink: 0;
    position: relative;
    transition: box-shadow 0.2s, transform 0.2s;
}
.commodity-card:hover {
    box-shadow: 0 8px 32px 0 rgba(245,215,110,0.18);
    transform: scale(1.045);
    z-index: 2;
}
.commodity-header {
    display: flex;
    align-items: center;
    margin-bottom: 0.7rem;
    font-size: 1.1rem;
    font-weight: 500;
}
.commodity-title {
    color: #f5d76e;
    font-size: 1.1rem;
    font-weight: 500;
    margin-left: 0.4rem;
}
.commodity-flag {
    font-size: 1.1rem;
    margin-left: 0.2rem;
}
.commodity-icon {
    font-size: 1.5rem;
}
.trend-row {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-bottom: 0.4rem;
    margin-top: -0.7rem;
    width: 100%;
}
.trend-icon {
    width: 22px;
    height: 14px;
    margin-right: 0.2rem;
    vertical-align: middle;
    display: inline-block;
}
.trend-positive {
    color: #00b86b;
    font-weight: 500;
    font-size: 1.05rem;
}
.trend-negative {
    color: #ff4444;
    font-weight: 500;
    font-size: 1.05rem;
}
.commodity-metrics {
    display: flex;
    justify-content: space-between;
    margin: 0.7rem 0 0.1rem 0;
    width: 100%;
}
.metric-label {
    color: #b0b0b0;
    font-size: 0.95rem;
    font-weight: 400;
}
.metric-value {
    color: #00b86b;
    font-size: 1.25rem;
    font-weight: 500;
    margin-top: 0.1rem;
}
</style>
''', unsafe_allow_html=True)

# Streamlit-native welcome popup
if 'welcome_shown' not in st.session_state:
    st.session_state['welcome_shown'] = False

if not st.session_state['welcome_shown']:
    st.markdown('<div style="display:flex;justify-content:center;align-items:center;height:80vh;">'
                '<div style="background:#1C352D;padding:3rem 4rem;border-radius:2rem;box-shadow:0 8px 32px rgba(0,0,0,0.25);text-align:center;">'
                '<span style="font-size:2.2rem;font-weight:bold;color:#f5d76e;">Welcome to Commodity Trading</span><br><br>', unsafe_allow_html=True)
    if st.button("Continue", key="welcome_btn", help="Click to continue"):
        st.session_state['welcome_shown'] = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# Header
st.markdown('<div class="header-title" style="color:#f5d76e;">Commodity Price Prediction</div>', unsafe_allow_html=True)

# Commodity Emojis
st.markdown('<div class="commodity-emojis" style="color:#f5d76e;">'
    '🛢️ Crude Oil &nbsp; '
    '🔥 Natural Gas &nbsp; '
    '🌾 Wheat &nbsp; '
    '🏆 Gold &nbsp; '
    '🥈 Silver &nbsp; '
    '🟫 Copper'
    '</div>', unsafe_allow_html=True)

# Subheader
st.markdown('<div class="header-sub" style="color:#f5d76e;">Learn how to trade gold, oil, and other essential commodities with expert insights and strategies</div>', unsafe_allow_html=True)

# Dummy values for Bid, Ask, Spread, and dummy graph data
DUMMY_METRICS = {
    'Silver': {'bid': 3239.18, 'ask': 3239.66, 'spread': 0.00005, 'change': 0.06},
    'Gold': {'bid': 947.46, 'ask': 961.54, 'spread': 0.00005, 'change': 0.77},
    'Copper': {'bid': 1.075, 'ask': 1.07, 'spread': 0.00005, 'change': 0.11},
}

# Dummy SVGs for up and down trend
UP_TREND_SVG = '''<svg class="trend-icon" viewBox="0 0 32 20" fill="none" xmlns="http://www.w3.org/2000/svg"><polyline points="2,18 10,8 18,14 30,2" stroke="#00b86b" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
DOWN_TREND_SVG = '''<svg class="trend-icon" viewBox="0 0 32 20" fill="none" xmlns="http://www.w3.org/2000/svg"><polyline points="2,2 10,10 18,4 30,18" stroke="#ff4444" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

# Commodity data and icons (add US flag)
commodities = [
    {"name": "Silver", "symbol": "SI=F", "icon": "🥈", "flag": "🇺🇸"},
    {"name": "Gold", "symbol": "GC=F", "icon": "🥇", "flag": "🇺🇸"},
    {"name": "Copper", "symbol": "HG=F", "icon": "🥉", "flag": "🇺🇸"},
    {"name": "Crude Oil", "symbol": "CL=F", "icon": "🛢️", "flag": "🇺🇸"},
    {"name": "Natural Gas", "symbol": "NG=F", "icon": "🔥", "flag": "🇺🇸"},
    {"name": "Wheat", "symbol": "ZW=F", "icon": "🌾", "flag": "🇺🇸"},
]

@st.cache_data(ttl=300, show_spinner=False)
def get_commodity_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        bid = info.get('bid')
        ask = info.get('ask')
        # Fallback to close price if bid/ask not available
        data = yf.download(symbol, period="1d", interval="1m")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            prev_price = data['Open'].iloc[0]
            change = ((current_price - prev_price) / prev_price) * 100
        else:
            current_price = prev_price = change = None
        # Calculate spread if possible
        if bid is not None and ask is not None:
            spread = abs(ask - bid)
        else:
            spread = None
        return {
            'price': current_price,
            'change': change,
            'bid': bid,
            'ask': ask,
            'spread': spread
        }
    except Exception as e:
        return None

# Update card layout to match screenshot
st.markdown('<div class="commodity-cards">', unsafe_allow_html=True)
for idx, commodity in enumerate(commodities[:3]):
    metrics = DUMMY_METRICS[commodity['name']]
    is_positive = metrics['change'] >= 0
    trend_svg = UP_TREND_SVG if is_positive else DOWN_TREND_SVG
    trend_class = "trend-positive" if is_positive else "trend-negative"
    change_symbol = "+" if is_positive else ""
    st.markdown(f'''
    <div class="commodity-card">
        <div class="trend-row">
            {trend_svg}
            <span class="{trend_class}">{change_symbol}{metrics['change']:.2f}%</span>
        </div>
        <div class="commodity-header">
            <span class="commodity-icon">{commodity['icon']}</span>
            <span class="commodity-flag">{commodity['flag']}</span>
            <span class="commodity-title">{commodity['name']}/USD</span>
        </div>
        <div class="commodity-metrics">
            <div>
                <div class="metric-label">Bid</div>
                <div class="metric-value">{metrics['bid']}</div>
            </div>
            <div>
                <div class="metric-label">Ask</div>
                <div class="metric-value">{metrics['ask']}</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sign Up Section
st.markdown('''
<div class="signup-container">
    <form>
        <label for="email">Email</label><br>
        <input type="email" id="email" name="email" style="width:100%;padding:0.7rem 1rem;margin:0.5rem 0 1rem 0;border-radius:1rem;border:none;font-size:1.1rem;">
        <div style="font-size:0.9rem;margin-bottom:1.2rem;">By creating an account, you agree to our <a href="#" style="color:#f5d76e;text-decoration:underline;">Terms and conditions</a> and acknowledge that we may send you updates and marketing materials (see our <a href="#" style="color:#f5d76e;text-decoration:underline;">Security and privacy policy</a>). Unsubscribe anytime in your account settings.</div>
        <button class="signup-btn" type="button">Sign up</button>
    </form>
    <div class="signup-divider">Or</div>
    <a class="social-btn" href="https://accounts.google.com/signup" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_2013_Google.png">Sign up with Google</a>
    <a class="social-btn" href="https://www.facebook.com/r.php" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg">Sign up with Facebook</a>
    <a class="social-btn" href="https://appleid.apple.com/account" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg">Sign up with Apple</a>
</div>
''', unsafe_allow_html=True)

# Commodity mapping for yfinance and finnhub
COMMODITY_OPTIONS = {
    "Gold": {"yfinance": "GC=F", "finnhub": "OANDA:XAU_USD"},
    "Silver": {"yfinance": "SI=F", "finnhub": "OANDA:XAG_USD"},
    "Wheat": {"yfinance": "ZW=F", "finnhub": "OANDA:XW1_USD"},
    "Crude Oil": {"yfinance": "CL=F", "finnhub": "OANDA:XWT_USD"},
    "Natural Gas": {"yfinance": "NG=F", "finnhub": "OANDA:XNG_USD"},
    "Copper": {"yfinance": "HG=F", "finnhub": "OANDA:XCU_USD"}
}

# Sidebar navigation with custom-styled buttons
st.sidebar.markdown('<h2 style="color:#f5d76e;">Navigation</h2>', unsafe_allow_html=True)
nav_pages = ["About", "Commodity Trading", "How it works?"]
nav_styles = {
    "active": "background-color:#f5d76e;color:#123524;font-weight:bold;border-radius:1.5rem;padding:0.5rem 0.5rem;margin-bottom:0.5rem;width:100%;border:none;font-size:1.1rem;",
    "inactive": "background:transparent;color:#f5d76e;border:2px solid #f5d76e;border-radius:1.5rem;padding:0.5rem 0.5rem;margin-bottom:0.5rem;width:100%;font-size:1.1rem;"
}
if 'page' not in st.session_state:
    st.session_state['page'] = None
for page_name in nav_pages:
    if st.sidebar.button(page_name, key=f"nav_{page_name}", help=f"Go to {page_name}",
                        args=(), kwargs={},
                        use_container_width=True):
        st.session_state['page'] = page_name
    # Custom style for the button
    st.sidebar.markdown(f"""
        <style>
        div[data-testid=\"stSidebar\"] button[kind=\"secondary\"]#{'nav_' + page_name} {{
            {nav_styles['active' if st.session_state.get('page') == page_name else 'inactive']}
        }}
        </style>
    """, unsafe_allow_html=True)

# Show About content only if About button was clicked
if st.session_state['page'] == 'About':
    st.markdown('<div class="about-heading" style="color:#f5d76e;font-size:2rem;font-weight:bold;margin-bottom:1.2rem;">What are commodities?</div>', unsafe_allow_html=True)
    st.write("Commodities are basic goods or raw materials that are interchangeable with other goods of the same type. They are used in commerce and are often the building blocks of more complex goods and services.")
    st.write('🔑 **Two Main Types of Commodities:**')

    st.markdown('**1. Hard Commodities**  ')
    st.write('These are natural resources that are mined or extracted.')
    st.markdown('**Examples:**')
    hard_commodities = [
        ("Gold", "static/gold.JPG"),
        ("Silver", "static/silver.JPG"),
        ("Crude Oil", "static/crude_oil.JPG"),
        ("Natural Gas", "static/natural_gas.JPG"),
        ("Copper", "static/copper.JPG"),
    ]
    for name, img_path in hard_commodities:
        cols = st.columns([1, 6])
        with cols[0]:
            st.image(img_path, width=80)
        with cols[1]:
            st.markdown(f"<span style='color:#f5d76e;font-size:1.1rem;'>{name}</span>", unsafe_allow_html=True)

    st.markdown('**2. Soft Commodities**  ')
    st.write('These are agricultural products or livestock.')
    st.markdown('**Examples:**')
    soft_commodities = [
        ("Wheat", "static/wheat.JPG"),
        ("Corn", "static/corn.JPG"),
        ("Sugar", "static/sugar.JPG"),
        ("Cotton", "static/cotton.JPG"),
        ("Coffee", "static/coffee.JPG"),
    ]
    for name, img_path in soft_commodities:
        cols = st.columns([1, 6])
        with cols[0]:
            st.image(img_path, width=80)
        with cols[1]:
            st.markdown(f"<span style='color:#f5d76e;font-size:1.1rem;'>{name}</span>", unsafe_allow_html=True)

    st.markdown('''
    <br>
    <b>📈 Why Commodities Matter in Finance</b><br>
    <ul>
      <li>Traded on exchanges like the Chicago Mercantile Exchange (CME) or New York Mercantile Exchange (NYMEX)</li>
      <li>Prices fluctuate due to supply and demand, geopolitical events, weather, inflation, etc.</li>
      <li>Investors use them for hedging and speculation</li>
    </ul>
    ''', unsafe_allow_html=True)

# Show Commodity Trading content only if Commodity Trading button was clicked
if st.session_state['page'] == 'Commodity Trading':
    st.markdown('<div class="about-heading" style="color:#f5d76e;font-size:2rem;font-weight:bold;margin-bottom:1.2rem;">What is Commodity Trading?</div>', unsafe_allow_html=True)
    st.write("Commodity trading is the buying and selling of raw materials or primary products like gold, oil, wheat, or natural gas. Traders try to profit from changes in commodity prices—just like stock trading, but with goods instead of companies.")
    st.markdown('''
    <b>⚙️ How Commodity Trading Works</b><br>
    <ul>
      <li>Commodities are traded on exchanges (like NYMEX, CME, or MCX).</li>
      <li>Prices are set based on global supply and demand, weather, politics, war, inflation, etc.</li>
      <li>You can trade commodities in two main ways:
        <ul>
          <li><b>Spot Market:</b> Buy/sell actual physical goods (used more by producers and buyers)</li>
          <li><b>Futures Market:</b> Buy/sell contracts to deliver commodities in the future (most common for traders and investors).</li>
        </ul>
      </li>
    </ul>
    ''', unsafe_allow_html=True)
    st.video('https://www.youtube.com/watch?v=EtqVmE2U4Xo')
    st.markdown('<div style="color:#f5d76e;font-size:1.3rem;font-weight:bold;margin-top:2rem;">🌟 Benefits of Commodity Trading</div>', unsafe_allow_html=True)
    st.markdown('''
    <style>
    .gold-table td, .gold-table th {
        color: #f5d76e !important;
        border: 1px solid #f5d76e;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
    }
    .gold-table {
        border-collapse: collapse;
        margin-top: 1rem;
        margin-bottom: 2rem;
        width: 100%;
    }
    </style>
    <table class="gold-table">
        <tr>
            <th>Benefit</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>Diversification</td>
            <td>Helps spread investment risk beyond stocks and bonds.</td>
        </tr>
        <tr>
            <td>Hedging Against Inflation</td>
            <td>Commodities often rise in price when inflation increases.</td>
        </tr>
        <tr>
            <td>High Liquidity</td>
            <td>Many commodities are traded in huge volumes daily.</td>
        </tr>
        <tr>
            <td>Profit Opportunities</td>
            <td>Volatility in prices = chances to profit from price swings.</td>
        </tr>
    </table>
    ''', unsafe_allow_html=True)
elif st.session_state['page'] == 'How it works?':
    st.markdown('<div class="about-heading" style="color:#f5d76e;font-size:2rem;font-weight:bold;margin-bottom:1.2rem;">How it works?</div>', unsafe_allow_html=True)
    st.markdown('**Upload Kragle CSV**', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your Kaggle dataset", type=['csv', 'xlsx'])
    data = None
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

    st.markdown('**Select Commodity**', unsafe_allow_html=True)
    COMMODITY_OPTIONS = {
        "Gold": {"yfinance": "GC=F", "finnhub": "OANDA:XAU_USD"},
        "Silver": {"yfinance": "SI=F", "finnhub": "OANDA:XAG_USD"},
        "Wheat": {"yfinance": "ZW=F", "finnhub": "OANDA:XW1_USD"},
        "Crude Oil": {"yfinance": "CL=F", "finnhub": "OANDA:XWT_USD"},
        "Natural Gas": {"yfinance": "NG=F", "finnhub": "OANDA:XNG_USD"},
        "Copper": {"yfinance": "HG=F", "finnhub": "OANDA:XCU_USD"}
    }
    commodity = st.selectbox("Choose a commodity:", list(COMMODITY_OPTIONS.keys()))

    if commodity:
        st.markdown(f"**Fetch Real-Time Data for {commodity}**", unsafe_allow_html=True)
        # Fetch with yfinance
        yf_symbol = COMMODITY_OPTIONS[commodity]["yfinance"]
        try:
            yf_data = yf.download(yf_symbol, period="5d")
            if yf_data.empty:
                st.warning("No data found for this commodity. Please try another or check your internet connection.")
            else:
                st.write(f"### {commodity} - Yahoo Finance (last 5 days)")
                st.dataframe(yf_data)
        except Exception as e:
            st.error(f"Failed to fetch data from Yahoo Finance: {e}")
        # Fetch with finnhub
        finnhub_symbol = COMMODITY_OPTIONS[commodity]["finnhub"]
        try:
            import os
            import finnhub
            api_key = os.getenv('FINNHUB_API_KEY')
            if api_key:
                finnhub_client = finnhub.Client(api_key=api_key)
                quote = finnhub_client.quote(finnhub_symbol)
                st.write(f"### {commodity} - Finnhub Real-Time Quote")
                st.json(quote)
            else:
                st.info("Finnhub API key not set. Skipping Finnhub data.")
        except Exception as e:
            st.warning(f"Finnhub data unavailable: {str(e)}")

    # Step 2: Load Data Button
    if data is not None:
        if st.button('Load Data'):
            st.dataframe(data)
            st.success("Data Loaded Successfully")

        # Step 3: Preprocessing Button
        if st.button('Preprocessing'):
            # Show before stats
            st.info(f"Missing values before: {data.isnull().sum().sum()}")
            st.info(f"Rows before: {data.shape[0]}")
            # Handle missing values (drop rows with any missing values)
            data_clean = data.dropna()
            # Handle outliers (remove rows where any numeric value is more than 3 std from mean)
            numeric_cols = data_clean.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                mean = data_clean[col].mean()
                std = data_clean[col].std()
                data_clean = data_clean[(data_clean[col] >= mean - 3*std) & (data_clean[col] <= mean + 3*std)]
            # Show after stats
            st.info(f"Missing values after: {data_clean.isnull().sum().sum()}")
            st.info(f"Rows after: {data_clean.shape[0]}")
            st.success("Preprocessing complete!")
            st.dataframe(data_clean)

        # Step 4: Feature Engineering Button
        if st.button('Feature Engineering'):
            df = data.copy()
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            # Only allow numeric columns and their engineered features for modeling
            feature_options = list(numeric_cols)
            # Add engineered features for numeric columns
            for col in numeric_cols:
                df[f'{col}_ma5'] = df[col].rolling(window=5).mean()
                df[f'{col}_lag1'] = df[col].shift(1)
                feature_options.append(f'{col}_ma5')
                feature_options.append(f'{col}_lag1')
            selected_features = st.multiselect('Select features for modeling:', feature_options, default=feature_options)
            st.info(f'Selected features: {selected_features}')
            st.dataframe(df[selected_features].head(10))
            st.success('Feature engineering complete!')

        # Step 5: Model Training Button
        if st.button('Model Training'):
            df = data.copy()
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            feature_options = list(numeric_cols)
            for col in numeric_cols:
                df[f'{col}_ma5'] = df[col].rolling(window=5).mean()
                df[f'{col}_lag1'] = df[col].shift(1)
                feature_options.append(f'{col}_ma5')
                feature_options.append(f'{col}_lag1')
            selected_features = st.multiselect('Select features for modeling:', feature_options, default=feature_options, key='model_features')
            df_model = df[selected_features].dropna()
            if len(selected_features) < 2:
                st.warning('Please select at least one feature and a target.')
            else:
                X = df_model.iloc[:, :-1]
                y = df_model.iloc[:, -1]
                model = LinearRegression()
                model.fit(X, y)
                st.success('Model Trained!')

        # Step 6: Evaluation Button
        if st.button('Evaluation'):
            df = data.copy()
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            feature_options = list(numeric_cols)
            for col in numeric_cols:
                df[f'{col}_ma5'] = df[col].rolling(window=5).mean()
                df[f'{col}_lag1'] = df[col].shift(1)
                feature_options.append(f'{col}_ma5')
                feature_options.append(f'{col}_lag1')
            selected_features = st.multiselect('Select features for modeling:', feature_options, default=feature_options, key='eval_features')
            df_model = df[selected_features].dropna()
            if len(selected_features) < 2:
                st.warning('Please select at least one feature and a target.')
            else:
                X = df_model.iloc[:, :-1]
                y = df_model.iloc[:, -1]
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                r2 = r2_score(y_test, y_pred)
                mae = np.mean(np.abs(y_test - y_pred))
                mse = np.mean((y_test - y_pred) ** 2)
                st.info(f'R² Score: {r2:.4f}')
                st.info(f'MAE: {mae:.4f}')
                st.info(f'MSE: {mse:.4f}')
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=y_test, mode='lines', name='Actual'))
                fig.add_trace(go.Scatter(y=y_pred, mode='lines', name='Predicted'))
                fig.update_layout(title='Actual vs Predicted', xaxis_title='Index', yaxis_title='Value')
                st.plotly_chart(fig)
                st.success('Evaluation complete!')

        # Step 7: Results Visualization Button
        if st.button('Results Visualization'):
            df = data.copy()
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            feature_options = list(numeric_cols)
            for col in numeric_cols:
                df[f'{col}_ma5'] = df[col].rolling(window=5).mean()
                df[f'{col}_lag1'] = df[col].shift(1)
                feature_options.append(f'{col}_ma5')
                feature_options.append(f'{col}_lag1')
            selected_features = st.multiselect('Select features for modeling:', feature_options, default=feature_options, key='viz_features')
            df_model = df[selected_features].dropna()
            if len(selected_features) < 2:
                st.warning('Please select at least one feature and a target.')
            else:
                X = df_model.iloc[:, :-1]
                y = df_model.iloc[:, -1]
                model = LinearRegression()
                model.fit(X, y)
                n_days = st.number_input('Forecast next n-days:', min_value=1, max_value=30, value=5)
                last_row = X.iloc[[-1]].values
                preds = []
                for _ in range(n_days):
                    pred = model.predict(last_row)[0]
                    preds.append(pred)
                forecast_index = range(len(y), len(y) + n_days)
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=y, mode='lines', name='Actual'))
                fig.add_trace(go.Scatter(x=list(forecast_index), y=preds, mode='lines+markers', name='Forecast'))
                fig.update_layout(title='Future Forecast', xaxis_title='Index', yaxis_title='Value')
                st.plotly_chart(fig)
                forecast_df = pd.DataFrame({'Forecast': preds})
                csv = forecast_df.to_csv(index=False).encode('utf-8')
                st.download_button('Download Forecast CSV', csv, 'forecast.csv', 'text/csv')
                st.success('Results visualization complete!')

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode() 
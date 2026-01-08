"""
Live Quotes Page - Real-time market quotes display

Features:
- Real-time price updates (auto-refresh when market is live)
- Watchlist management
- Bid/Ask spread
- Volume and OI tracking
- % change indicators

Author: Smart Analysis System
"""
import streamlit as st
import pandas as pd
from datetime import datetime, time as dt_time
from libs.smart_data_router import SmartDataRouter
from libs.broker_manager import BrokerManager
import time


def is_market_open() -> bool:
    """Check if market is currently open"""
    now = datetime.now()
    current_time = now.time()
    
    # Market hours: 9:15 AM to 3:30 PM IST, Monday-Friday
    market_start = dt_time(9, 15)
    market_end = dt_time(15, 30)
    
    # Check if weekday (0=Monday, 6=Sunday)
    is_weekday = now.weekday() < 5
    
    # Check if within market hours
    is_trading_hours = market_start <= current_time <= market_end
    
    return is_weekday and is_trading_hours


def display_quote_card(symbol: str, exchange: str, quote: dict):
    """Display a quote card with real-time data"""
    if not quote:
        st.error(f"No data available for {symbol}")
        return
    
    ltp = quote.get('ltp', 0)
    prev_close = quote.get('prev_close', 0)
    change = ltp - prev_close
    change_pct = (change / prev_close * 100) if prev_close else 0
    
    # Color based on change
    color = "green" if change >= 0 else "red"
    arrow = "▲" if change >= 0 else "▼"
    
    with st.container():
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"### {symbol}")
            st.caption(exchange)
        
        with col2:
            st.markdown(f"### ₹{ltp:,.2f}")
            st.markdown(f":{color}[{arrow} {change:+.2f} ({change_pct:+.2f}%)]")
        
        with col3:
            if st.button("📊", key=f"chart_{symbol}"):
                st.session_state['selected_symbol'] = symbol
                st.switch_page("pages/stock_analysis.py")
        
        # Additional details
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Open", f"₹{quote.get('open', 0):,.2f}")
        with col2:
            st.metric("High", f"₹{quote.get('high', 0):,.2f}")
        with col3:
            st.metric("Low", f"₹{quote.get('low', 0):,.2f}")
        with col4:
            st.metric("Volume", f"{quote.get('volume', 0):,}")
        
        # Bid/Ask spread
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"Bid: ₹{quote.get('bid', 0):,.2f}")
        with col2:
            st.caption(f"Ask: ₹{quote.get('ask', 0):,.2f}")
        
        st.divider()


def show_live_quotes():
    """Main live quotes page"""
    st.title("📊 Live Market Quotes")
    
    # Initialize components
    router = SmartDataRouter()
    broker_manager = BrokerManager()
    
    # Check broker status
    active_broker = broker_manager.get_active_broker()
    broker_status = broker_manager.get_broker_status(active_broker) if active_broker else None
    
    if not active_broker or not broker_status or not broker_status.get('is_active'):
        st.warning("⚠️ No active broker configured. Please configure a broker first.")
        if st.button("Go to Broker Configuration"):
            st.switch_page("pages/broker_config.py")
        return
    
    # Market status
    market_open = is_market_open()
    if market_open:
        st.success("🟢 Market is OPEN - Live quotes updating")
    else:
        st.info("🔴 Market is CLOSED - Showing last available quotes")
    
    # Sidebar - Watchlist Management
    with st.sidebar:
        st.header("📋 Watchlist")
        
        # Initialize watchlist in session state
        if 'watchlist' not in st.session_state:
            st.session_state.watchlist = [
                {'symbol': 'SBIN', 'exchange': 'NSE'},
                {'symbol': 'RELIANCE', 'exchange': 'NSE'},
                {'symbol': 'TCS', 'exchange': 'NSE'},
                {'symbol': 'INFY', 'exchange': 'NSE'},
                {'symbol': 'HDFCBANK', 'exchange': 'NSE'}
            ]
        
        # Add new symbol
        with st.expander("➕ Add Symbol"):
            new_symbol = st.text_input("Symbol", key="new_symbol")
            new_exchange = st.selectbox("Exchange", ["NSE", "BSE", "NFO"], key="new_exchange")
            
            if st.button("Add to Watchlist"):
                if new_symbol:
                    st.session_state.watchlist.append({
                        'symbol': new_symbol.upper(),
                        'exchange': new_exchange
                    })
                    st.success(f"Added {new_symbol}")
                    st.rerun()
        
        # Display watchlist
        st.caption(f"{len(st.session_state.watchlist)} symbols")
        
        # Remove symbol option
        if st.session_state.watchlist:
            symbols_to_remove = st.multiselect(
                "Remove symbols",
                [f"{s['symbol']} ({s['exchange']})" for s in st.session_state.watchlist],
                key="remove_symbols"
            )
            if st.button("Remove Selected") and symbols_to_remove:
                for symbol_str in symbols_to_remove:
                    symbol = symbol_str.split(" (")[0]
                    st.session_state.watchlist = [
                        s for s in st.session_state.watchlist 
                        if s['symbol'] != symbol
                    ]
                st.rerun()
    
    # Auto-refresh settings
    col1, col2 = st.columns([3, 1])
    with col1:
        auto_refresh = st.checkbox(
            "Auto-refresh (5 sec)", 
            value=market_open,
            help="Automatically refresh quotes every 5 seconds when market is open"
        )
    with col2:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Display quotes
    if not st.session_state.watchlist:
        st.info("📝 Add symbols to your watchlist to see live quotes")
        return
    
    # Fetch and display quotes
    with st.spinner("Fetching live quotes..."):
        for item in st.session_state.watchlist:
            symbol = item['symbol']
            exchange = item['exchange']
            
            try:
                quote = router.get_quote(symbol, exchange)
                display_quote_card(symbol, exchange, quote)
            except Exception as e:
                st.error(f"Error fetching {symbol}: {str(e)}")
    
    # Auto-refresh logic
    if auto_refresh and market_open:
        time.sleep(5)
        st.rerun()
    
    # Footer
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption(f"Data source: {active_broker.upper()} • Broker: {broker_status.get('name', 'Unknown')}")


if __name__ == "__main__":
    show_live_quotes()

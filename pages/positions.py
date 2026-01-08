"""
Position Monitor - Track open positions and P&L

Features:
- Real-time P&L calculation
- Position-wise breakdown
- Quick exit buttons
- Auto-refresh
- Risk metrics

Author: Smart Analysis System
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from libs.smart_data_router import SmartDataRouter
from libs.broker_manager import BrokerManager
import time


def calculate_pnl(entry_price: float, current_price: float, quantity: int, action: str) -> dict:
    """Calculate P&L for a position"""
    if action == "BUY":
        pnl = (current_price - entry_price) * quantity
    else:  # SELL
        pnl = (entry_price - current_price) * quantity
    
    pnl_pct = (pnl / (entry_price * quantity) * 100) if entry_price * quantity > 0 else 0
    
    return {
        'pnl': pnl,
        'pnl_pct': pnl_pct,
        'current_value': current_price * quantity,
        'invested_value': entry_price * quantity
    }


def display_position_card(position: dict, router: SmartDataRouter):
    """Display a position card with live P&L"""
    symbol = position['symbol']
    exchange = position['exchange']
    entry_price = position['entry_price']
    quantity = position['quantity']
    action = position['action']
    
    # Get current price
    try:
        quote = router.get_quote(symbol, exchange)
        current_price = quote.get('ltp', entry_price) if quote else entry_price
    except:
        current_price = entry_price
    
    # Calculate P&L
    pnl_data = calculate_pnl(entry_price, current_price, quantity, action)
    
    # Color based on P&L
    color = "green" if pnl_data['pnl'] >= 0 else "red"
    
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            st.markdown(f"### {symbol}")
            st.caption(f"{exchange} • {action} {quantity}")
        
        with col2:
            st.metric("Entry", f"₹{entry_price:,.2f}")
            st.metric("Current", f"₹{current_price:,.2f}")
        
        with col3:
            st.metric(
                "P&L", 
                f"₹{pnl_data['pnl']:,.2f}",
                delta=f"{pnl_data['pnl_pct']:.2f}%",
                delta_color="normal" if pnl_data['pnl'] >= 0 else "inverse"
            )
        
        with col4:
            if st.button("❌ Exit", key=f"exit_{symbol}", use_container_width=True):
                st.warning(f"Exit {symbol}? (Integration pending)")
        
        st.divider()


def show_positions():
    """Main position monitor page"""
    st.title("💼 Position Monitor")
    
    # Initialize components
    router = SmartDataRouter()
    broker_manager = BrokerManager()
    
    # Check broker status
    active_broker = broker_manager.get_active_broker()
    broker_status = broker_manager.get_broker_status(active_broker) if active_broker else None
    
    if not active_broker or not broker_status or not broker_status.get('is_active'):
        st.error("❌ No active broker configured")
        if st.button("Configure Broker"):
            st.switch_page("pages/broker_config.py")
        return
    
    st.success(f"✅ Connected to {broker_status.get('name', 'Unknown')}")
    
    # Auto-refresh toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        auto_refresh = st.checkbox("Auto-refresh (10 sec)", value=True)
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Mock positions (TODO: Fetch from broker API)
    if 'mock_positions' not in st.session_state:
        st.session_state.mock_positions = [
            {
                'symbol': 'SBIN',
                'exchange': 'NSE',
                'action': 'BUY',
                'quantity': 10,
                'entry_price': 750.00
            },
            {
                'symbol': 'RELIANCE',
                'exchange': 'NSE',
                'action': 'BUY',
                'quantity': 5,
                'entry_price': 2800.00
            }
        ]
    
    positions = st.session_state.mock_positions
    
    if not positions:
        st.info("📭 No open positions")
        if st.button("Place Order"):
            st.switch_page("pages/order_placement.py")
        return
    
    # Summary metrics
    st.subheader("📊 Portfolio Summary")
    
    total_pnl = 0
    total_invested = 0
    total_current = 0
    
    for pos in positions:
        try:
            quote = router.get_quote(pos['symbol'], pos['exchange'])
            current_price = quote.get('ltp', pos['entry_price']) if quote else pos['entry_price']
        except:
            current_price = pos['entry_price']
        
        pnl_data = calculate_pnl(pos['entry_price'], current_price, pos['quantity'], pos['action'])
        total_pnl += pnl_data['pnl']
        total_invested += pnl_data['invested_value']
        total_current += pnl_data['current_value']
    
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Positions", len(positions))
    with col2:
        st.metric("Invested", f"₹{total_invested:,.2f}")
    with col3:
        st.metric("Current Value", f"₹{total_current:,.2f}")
    with col4:
        st.metric(
            "Total P&L",
            f"₹{total_pnl:,.2f}",
            delta=f"{total_pnl_pct:.2f}%",
            delta_color="normal" if total_pnl >= 0 else "inverse"
        )
    
    st.divider()
    
    # Display positions
    st.subheader("📈 Open Positions")
    
    for position in positions:
        display_position_card(position, router)
    
    # Quick actions
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Place New Order", use_container_width=True):
            st.switch_page("pages/order_placement.py")
    
    with col2:
        if st.button("❌ Exit All Positions", use_container_width=True):
            st.warning("Exit all positions? (Integration pending)")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(10)
        st.rerun()
    
    # Footer
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    show_positions()

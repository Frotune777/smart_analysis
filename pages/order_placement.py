"""
Order Placement Page - Trade execution interface

Features:
- Market/Limit/Stop-Loss orders
- Position sizing calculator
- Risk management checks
- Real-time price display
- Order confirmation

Author: Smart Analysis System
"""
import streamlit as st
from libs.smart_data_router import SmartDataRouter
from libs.broker_manager import BrokerManager
from datetime import datetime


def calculate_position_size(capital: float, risk_pct: float, entry: float, stop_loss: float) -> int:
    """Calculate position size based on risk"""
    if entry <= 0 or stop_loss <= 0:
        return 0
    
    risk_amount = capital * (risk_pct / 100)
    risk_per_share = abs(entry - stop_loss)
    
    if risk_per_share == 0:
        return 0
    
    quantity = int(risk_amount / risk_per_share)
    return max(1, quantity)


def show_order_placement():
    """Main order placement page"""
    st.title("🎯 Order Placement")
    
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
    
    # Order form
    with st.form("order_form"):
        st.subheader("Order Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.text_input("Symbol", value="SBIN", help="Trading symbol")
            exchange = st.selectbox("Exchange", ["NSE", "BSE", "NFO", "BFO", "CDS", "MCX"])
            action = st.radio("Action", ["BUY", "SELL"], horizontal=True)
        
        with col2:
            order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "SL", "SL-M"])
            product = st.selectbox("Product", ["MIS", "CNC", "NRML"])
            quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
        
        # Price fields (conditional)
        col1, col2 = st.columns(2)
        
        with col1:
            if order_type in ["LIMIT", "SL"]:
                price = st.number_input("Price", min_value=0.0, value=0.0, step=0.05)
            else:
                price = 0.0
        
        with col2:
            if order_type in ["SL", "SL-M"]:
                trigger_price = st.number_input("Trigger Price", min_value=0.0, value=0.0, step=0.05)
            else:
                trigger_price = 0.0
        
        st.divider()
        
        # Position sizing calculator
        with st.expander("📐 Position Sizing Calculator"):
            calc_col1, calc_col2 = st.columns(2)
            
            with calc_col1:
                capital = st.number_input("Capital", min_value=0.0, value=100000.0, step=1000.0)
                risk_pct = st.number_input("Risk %", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
            
            with calc_col2:
                entry_price = st.number_input("Entry Price", min_value=0.0, value=0.0, step=0.05)
                stop_loss = st.number_input("Stop Loss", min_value=0.0, value=0.0, step=0.05)
            
            if st.button("Calculate"):
                suggested_qty = calculate_position_size(capital, risk_pct, entry_price, stop_loss)
                st.success(f"Suggested Quantity: {suggested_qty}")
                st.caption(f"Risk Amount: ₹{capital * risk_pct / 100:,.2f}")
        
        st.divider()
        
        # Real-time quote
        if symbol:
            try:
                quote = router.get_quote(symbol, exchange)
                if quote:
                    st.info(f"**LTP**: ₹{quote.get('ltp', 0):,.2f} | "
                           f"**Bid**: ₹{quote.get('bid', 0):,.2f} | "
                           f"**Ask**: ₹{quote.get('ask', 0):,.2f}")
            except:
                pass
        
        # Order summary
        st.subheader("Order Summary")
        
        total_value = quantity * (price if price > 0 else quote.get('ltp', 0) if symbol else 0)
        
        summary_col1, summary_col2 = st.columns(2)
        with summary_col1:
            st.metric("Quantity", quantity)
            st.metric("Order Type", order_type)
        with summary_col2:
            st.metric("Total Value", f"₹{total_value:,.2f}")
            st.metric("Product", product)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit = st.form_submit_button("🚀 Place Order", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            # Validation
            if not symbol:
                st.error("Please enter a symbol")
            elif quantity <= 0:
                st.error("Quantity must be greater than 0")
            elif order_type in ["LIMIT", "SL"] and price <= 0:
                st.error("Please enter a valid price")
            elif order_type in ["SL", "SL-M"] and trigger_price <= 0:
                st.error("Please enter a valid trigger price")
            else:
                # TODO: Integrate with broker API for actual order placement
                st.warning("⚠️ Order placement integration pending")
                st.info(f"Order Details: {action} {quantity} {symbol} @ {order_type}")
                
                # Show confirmation
                with st.expander("Order Confirmation"):
                    st.json({
                        "symbol": symbol,
                        "exchange": exchange,
                        "action": action,
                        "quantity": quantity,
                        "order_type": order_type,
                        "product": product,
                        "price": price,
                        "trigger_price": trigger_price,
                        "timestamp": datetime.now().isoformat()
                    })
        
        if cancel:
            st.info("Order cancelled")
    
    # Order history (placeholder)
    st.divider()
    st.subheader("📜 Recent Orders")
    st.info("Order history will be displayed here")


if __name__ == "__main__":
    show_order_placement()

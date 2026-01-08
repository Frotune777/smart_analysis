"""
Market Depth Component - Order book visualization

Features:
- Top 5 bid/ask levels
- Cumulative quantity display
- Price impact calculator
- Real-time updates
- Visual depth chart

Author: Smart Analysis System
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from libs.smart_data_router import SmartDataRouter


def display_market_depth(symbol: str, exchange: str, router: SmartDataRouter):
    """Display market depth visualization"""
    
    try:
        depth_data = router.get_depth(symbol, exchange)
        
        if not depth_data:
            st.warning("Market depth data not available")
            return
        
        bids = depth_data.get('bids', [])
        asks = depth_data.get('asks', [])
        
        if not bids or not asks:
            st.warning("No bid/ask data available")
            return
        
        # Create depth table
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🟢 Bids (Buy Orders)")
            bid_df = pd.DataFrame(bids[:5])
            bid_df['cumulative'] = bid_df['quantity'].cumsum()
            bid_df = bid_df.rename(columns={'price': 'Price', 'quantity': 'Qty', 'cumulative': 'Cumulative'})
            st.dataframe(bid_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("🔴 Asks (Sell Orders)")
            ask_df = pd.DataFrame(asks[:5])
            ask_df['cumulative'] = ask_df['quantity'].cumsum()
            ask_df = ask_df.rename(columns={'price': 'Price', 'quantity': 'Qty', 'cumulative': 'Cumulative'})
            st.dataframe(ask_df, use_container_width=True, hide_index=True)
        
        # Spread analysis
        best_bid = bids[0]['price'] if bids else 0
        best_ask = asks[0]['price'] if asks else 0
        spread = best_ask - best_bid
        spread_pct = (spread / best_bid * 100) if best_bid else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Best Bid", f"₹{best_bid:,.2f}")
        with col2:
            st.metric("Best Ask", f"₹{best_ask:,.2f}")
        with col3:
            st.metric("Spread", f"₹{spread:.2f} ({spread_pct:.3f}%)")
        
        # Depth chart
        fig = go.Figure()
        
        # Bids
        bid_prices = [b['price'] for b in bids]
        bid_quantities = [b['quantity'] for b in bids]
        bid_cumulative = pd.Series(bid_quantities).cumsum().tolist()
        
        fig.add_trace(go.Bar(
            x=bid_prices,
            y=bid_quantities,
            name='Bids',
            marker_color='green',
            opacity=0.7
        ))
        
        # Asks
        ask_prices = [a['price'] for a in asks]
        ask_quantities = [a['quantity'] for a in asks]
        
        fig.add_trace(go.Bar(
            x=ask_prices,
            y=ask_quantities,
            name='Asks',
            marker_color='red',
            opacity=0.7
        ))
        
        fig.update_layout(
            title="Market Depth",
            xaxis_title="Price",
            yaxis_title="Quantity",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Price impact calculator
        with st.expander("💰 Price Impact Calculator"):
            quantity = st.number_input("Order Quantity", min_value=1, value=100, step=10)
            
            # Calculate impact for buy
            buy_impact = 0
            buy_qty_remaining = quantity
            buy_cost = 0
            
            for ask in asks:
                if buy_qty_remaining <= 0:
                    break
                qty_filled = min(buy_qty_remaining, ask['quantity'])
                buy_cost += qty_filled * ask['price']
                buy_qty_remaining -= qty_filled
            
            avg_buy_price = buy_cost / quantity if quantity > 0 else 0
            buy_impact = ((avg_buy_price - best_ask) / best_ask * 100) if best_ask else 0
            
            # Calculate impact for sell
            sell_impact = 0
            sell_qty_remaining = quantity
            sell_proceeds = 0
            
            for bid in bids:
                if sell_qty_remaining <= 0:
                    break
                qty_filled = min(sell_qty_remaining, bid['quantity'])
                sell_proceeds += qty_filled * bid['price']
                sell_qty_remaining -= qty_filled
            
            avg_sell_price = sell_proceeds / quantity if quantity > 0 else 0
            sell_impact = ((best_bid - avg_sell_price) / best_bid * 100) if best_bid else 0
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Buy Impact",
                    f"{buy_impact:.3f}%",
                    delta=f"Avg Price: ₹{avg_buy_price:,.2f}"
                )
            
            with col2:
                st.metric(
                    "Sell Impact",
                    f"{sell_impact:.3f}%",
                    delta=f"Avg Price: ₹{avg_sell_price:,.2f}"
                )
        
    except Exception as e:
        st.error(f"Error fetching market depth: {str(e)}")


def show_market_depth_page():
    """Standalone market depth page"""
    st.title("📊 Market Depth")
    
    router = SmartDataRouter()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbol = st.text_input("Symbol", value="SBIN")
    
    with col2:
        exchange = st.selectbox("Exchange", ["NSE", "BSE", "NFO"])
    
    if st.button("🔄 Refresh"):
        st.rerun()
    
    if symbol:
        display_market_depth(symbol, exchange, router)


if __name__ == "__main__":
    show_market_depth_page()

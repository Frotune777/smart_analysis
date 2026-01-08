"""
Intraday Charts - Real-time intraday analysis

Features:
- Multiple timeframes (1m, 5m, 15m, 1h)
- Volume profile
- Technical indicators using pandas-ta (130+ indicators)
- Real-time updates
- Interactive charts

Author: Smart Analysis System
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from libs.smart_data_router import SmartDataRouter
from libs.broker_manager import BrokerManager
import pandas_ta as ta


def add_technical_indicators(df: pd.DataFrame, indicators: dict) -> pd.DataFrame:
    """Add technical indicators using pandas-ta"""
    
    # Simple Moving Average
    if indicators.get('sma_20'):
        df.ta.sma(length=20, append=True)
    
    # Exponential Moving Average
    if indicators.get('ema_50'):
        df.ta.ema(length=50, append=True)
    
    # Relative Strength Index
    if indicators.get('rsi'):
        df.ta.rsi(length=14, append=True)
    
    # MACD
    if indicators.get('macd'):
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
    
    return df


def create_candlestick_chart(df: pd.DataFrame, symbol: str, interval: str, indicators: dict):
    """Create interactive candlestick chart with indicators"""
    
    # Determine number of subplots
    subplot_count = 1
    subplot_titles = [f"{symbol} - {interval}"]
    row_heights = [0.7]
    
    if indicators.get('rsi'):
        subplot_count += 1
        subplot_titles.append("RSI")
        row_heights.append(0.15)
    
    if indicators.get('macd'):
        subplot_count += 1
        subplot_titles.append("MACD")
        row_heights.append(0.15)
    
    # Create subplots
    fig = make_subplots(
        rows=subplot_count,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=subplot_titles,
        row_heights=row_heights,
        specs=[[{"secondary_y": True}]] + [[{"secondary_y": False}]] * (subplot_count - 1)
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name="OHLC"
        ),
        row=1, col=1, secondary_y=False
    )
    
    # Volume bars
    colors = ['red' if df['close'].iloc[i] < df['open'].iloc[i] else 'green' 
              for i in range(len(df))]
    
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['volume'],
            name="Volume",
            marker_color=colors,
            opacity=0.3
        ),
        row=1, col=1, secondary_y=True
    )
    
    # Moving Averages
    if indicators.get('sma_20') and 'SMA_20' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['SMA_20'],
                name="SMA 20",
                line=dict(color='orange', width=1)
            ),
            row=1, col=1, secondary_y=False
        )
    
    if indicators.get('ema_50') and 'EMA_50' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['EMA_50'],
                name="EMA 50",
                line=dict(color='blue', width=1)
            ),
            row=1, col=1, secondary_y=False
        )
    
    # RSI
    current_row = 2
    if indicators.get('rsi') and 'RSI_14' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['RSI_14'],
                name="RSI",
                line=dict(color='purple', width=1)
            ),
            row=current_row, col=1
        )
        
        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=current_row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=current_row, col=1)
        
        current_row += 1
    
    # MACD
    if indicators.get('macd') and 'MACD_12_26_9' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACD_12_26_9'],
                name="MACD",
                line=dict(color='blue', width=1)
            ),
            row=current_row, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACDs_12_26_9'],
                name="Signal",
                line=dict(color='orange', width=1)
            ),
            row=current_row, col=1
        )
        
        colors = ['red' if h < 0 else 'green' for h in df['MACDh_12_26_9']]
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['MACDh_12_26_9'],
                name="Histogram",
                marker_color=colors
            ),
            row=current_row, col=1
        )
    
    # Update layout
    fig.update_layout(
        height=600 if subplot_count == 1 else 800,
        xaxis_rangeslider_visible=False,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="Price", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Volume", row=1, col=1, secondary_y=True)
    
    if indicators.get('rsi'):
        fig.update_yaxes(title_text="RSI", row=2, col=1)
    
    if indicators.get('macd'):
        row_idx = 3 if indicators.get('rsi') else 2
        fig.update_yaxes(title_text="MACD", row=row_idx, col=1)
    
    return fig


def show_intraday_charts():
    """Main intraday charts page"""
    st.title("📈 Intraday Charts")
    
    # Initialize components
    router = SmartDataRouter()
    broker_manager = BrokerManager()
    
    # Check broker status
    active_broker = broker_manager.get_active_broker()
    broker_status = broker_manager.get_broker_status(active_broker) if active_broker else None
    
    if not active_broker or not broker_status or not broker_status.get('is_active'):
        st.warning("⚠️ No active broker configured")
        if st.button("Configure Broker"):
            st.switch_page("pages/broker_config.py")
        return
    
    # Settings
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        symbol = st.text_input("Symbol", value="SBIN", help="Enter trading symbol")
    
    with col2:
        exchange = st.selectbox("Exchange", ["NSE", "BSE", "NFO", "BFO"])
    
    with col3:
        interval = st.selectbox(
            "Timeframe",
            ["1m", "5m", "15m", "30m", "1h"],
            index=1,
            help="Select chart timeframe"
        )
    
    # Date range
    col1, col2 = st.columns(2)
    
    with col1:
        days_back = st.slider("Days of history", 1, 30, 5)
    
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Technical indicators
    with st.expander("📊 Technical Indicators"):
        col1, col2 = st.columns(2)
        
        with col1:
            show_sma = st.checkbox("SMA 20", value=True)
            show_rsi = st.checkbox("RSI", value=True)
        
        with col2:
            show_ema = st.checkbox("EMA 50", value=True)
            show_macd = st.checkbox("MACD", value=False)
    
    indicators = {
        'sma_20': show_sma,
        'ema_50': show_ema,
        'rsi': show_rsi,
        'macd': show_macd
    }
    
    # Fetch data
    if symbol:
        with st.spinner(f"Fetching {interval} data for {symbol}..."):
            try:
                df = router.get_history(symbol, interval, days_back, exchange)
                
                if df is not None and not df.empty:
                    # Convert timestamp to datetime
                    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
                    df.set_index('datetime', inplace=True)
                    
                    # Add technical indicators using pandas-ta
                    df = add_technical_indicators(df, indicators)
                    
                    # Display current price
                    current_price = df['close'].iloc[-1]
                    prev_close = df['close'].iloc[0]
                    change = current_price - prev_close
                    change_pct = (change / prev_close * 100) if prev_close else 0
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Current Price", f"₹{current_price:,.2f}", 
                                 delta=f"{change:+.2f} ({change_pct:+.2f}%)")
                    with col2:
                        st.metric("High", f"₹{df['high'].max():,.2f}")
                    with col3:
                        st.metric("Low", f"₹{df['low'].min():,.2f}")
                    with col4:
                        st.metric("Volume", f"{df['volume'].sum():,.0f}")
                    
                    # Create and display chart
                    fig = create_candlestick_chart(df, symbol, interval, indicators)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Data table
                    with st.expander("📋 Raw Data"):
                        st.dataframe(
                            df[['open', 'high', 'low', 'close', 'volume']].tail(50),
                            use_container_width=True
                        )
                    
                else:
                    st.error("No data available for the selected parameters")
                    
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
                st.info("Make sure the broker is authenticated and the symbol is valid")
    
    # Footer
    st.caption(f"Data source: {active_broker.upper()} • Last updated: {datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    show_intraday_charts()

"""
Intraday Scanner - Real-time stock screening

Features:
- Volume breakout detection
- Momentum scanner
- Price action patterns
- Real-time alerts
- Customizable filters

Author: Smart Analysis System
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from libs.smart_data_router import SmartDataRouter
from libs.broker_manager import BrokerManager


def scan_volume_breakout(symbols: list, router: SmartDataRouter, exchange: str = 'NSE', 
                         threshold: float = 2.0) -> list:
    """Scan for volume breakouts"""
    results = []
    
    for symbol in symbols:
        try:
            # Get intraday data
            df = router.get_history(symbol, '5m', 1, exchange)
            
            if df is None or df.empty or len(df) < 20:
                continue
            
            # Calculate average volume
            avg_volume = df['volume'].tail(20).mean()
            current_volume = df['volume'].iloc[-1]
            
            # Check for breakout
            if current_volume > avg_volume * threshold:
                quote = router.get_quote(symbol, exchange)
                if quote:
                    results.append({
                        'symbol': symbol,
                        'ltp': quote.get('ltp', 0),
                        'volume': current_volume,
                        'avg_volume': avg_volume,
                        'volume_ratio': current_volume / avg_volume if avg_volume else 0,
                        'change_pct': ((quote.get('ltp', 0) - quote.get('prev_close', 0)) / 
                                      quote.get('prev_close', 1) * 100)
                    })
        except:
            continue
    
    return results


def scan_momentum(symbols: list, router: SmartDataRouter, exchange: str = 'NSE',
                 min_change: float = 2.0) -> list:
    """Scan for momentum stocks"""
    results = []
    
    for symbol in symbols:
        try:
            quote = router.get_quote(symbol, exchange)
            
            if not quote:
                continue
            
            ltp = quote.get('ltp', 0)
            prev_close = quote.get('prev_close', 0)
            change_pct = ((ltp - prev_close) / prev_close * 100) if prev_close else 0
            
            if abs(change_pct) >= min_change:
                results.append({
                    'symbol': symbol,
                    'ltp': ltp,
                    'prev_close': prev_close,
                    'change': ltp - prev_close,
                    'change_pct': change_pct,
                    'volume': quote.get('volume', 0)
                })
        except:
            continue
    
    return results


def scan_price_action(symbols: list, router: SmartDataRouter, exchange: str = 'NSE') -> list:
    """Scan for price action patterns"""
    results = []
    
    for symbol in symbols:
        try:
            df = router.get_history(symbol, '15m', 1, exchange)
            
            if df is None or df.empty or len(df) < 3:
                continue
            
            # Get last 3 candles
            last_3 = df.tail(3)
            
            # Bullish engulfing
            if (last_3.iloc[-2]['close'] < last_3.iloc[-2]['open'] and  # Previous red
                last_3.iloc[-1]['close'] > last_3.iloc[-1]['open'] and  # Current green
                last_3.iloc[-1]['open'] < last_3.iloc[-2]['close'] and  # Opens below prev close
                last_3.iloc[-1]['close'] > last_3.iloc[-2]['open']):    # Closes above prev open
                
                quote = router.get_quote(symbol, exchange)
                if quote:
                    results.append({
                        'symbol': symbol,
                        'pattern': 'Bullish Engulfing',
                        'ltp': quote.get('ltp', 0),
                        'signal': 'BUY',
                        'strength': 'Strong'
                    })
            
            # Bearish engulfing
            elif (last_3.iloc[-2]['close'] > last_3.iloc[-2]['open'] and  # Previous green
                  last_3.iloc[-1]['close'] < last_3.iloc[-1]['open'] and  # Current red
                  last_3.iloc[-1]['open'] > last_3.iloc[-2]['close'] and  # Opens above prev close
                  last_3.iloc[-1]['close'] < last_3.iloc[-2]['open']):    # Closes below prev open
                
                quote = router.get_quote(symbol, exchange)
                if quote:
                    results.append({
                        'symbol': symbol,
                        'pattern': 'Bearish Engulfing',
                        'ltp': quote.get('ltp', 0),
                        'signal': 'SELL',
                        'strength': 'Strong'
                    })
        except:
            continue
    
    return results


def show_intraday_scanner():
    """Main intraday scanner page"""
    st.title("🔍 Intraday Scanner")
    
    # Initialize components
    router = SmartDataRouter()
    broker_manager = BrokerManager()
    
    # Check broker status
    active_broker = broker_manager.get_active_broker()
    if not active_broker:
        st.warning("⚠️ No active broker configured")
        return
    
    # Scanner selection
    scanner_type = st.selectbox(
        "Scanner Type",
        ["Volume Breakout", "Momentum", "Price Action Patterns"]
    )
    
    # Symbol list
    with st.expander("📋 Symbol List"):
        default_symbols = "SBIN, RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, KOTAKBANK, AXISBANK, BHARTIARTL, ITC"
        symbols_input = st.text_area(
            "Enter symbols (comma-separated)",
            value=default_symbols,
            height=100
        )
        symbols = [s.strip().upper() for s in symbols_input.split(',') if s.strip()]
    
    # Scanner parameters
    col1, col2 = st.columns(2)
    
    with col1:
        exchange = st.selectbox("Exchange", ["NSE", "BSE"])
    
    with col2:
        if scanner_type == "Volume Breakout":
            threshold = st.slider("Volume Threshold (x)", 1.5, 5.0, 2.0, 0.5)
        elif scanner_type == "Momentum":
            min_change = st.slider("Min % Change", 1.0, 10.0, 2.0, 0.5)
    
    # Scan button
    if st.button("🔍 Scan Now", type="primary"):
        with st.spinner(f"Scanning {len(symbols)} symbols..."):
            if scanner_type == "Volume Breakout":
                results = scan_volume_breakout(symbols, router, exchange, threshold)
                
                if results:
                    st.success(f"Found {len(results)} volume breakouts")
                    df = pd.DataFrame(results)
                    df = df.sort_values('volume_ratio', ascending=False)
                    
                    st.dataframe(
                        df.style.format({
                            'ltp': '₹{:.2f}',
                            'volume': '{:,.0f}',
                            'avg_volume': '{:,.0f}',
                            'volume_ratio': '{:.2f}x',
                            'change_pct': '{:+.2f}%'
                        }),
                        use_container_width=True
                    )
                else:
                    st.info("No volume breakouts found")
            
            elif scanner_type == "Momentum":
                results = scan_momentum(symbols, router, exchange, min_change)
                
                if results:
                    st.success(f"Found {len(results)} momentum stocks")
                    df = pd.DataFrame(results)
                    df = df.sort_values('change_pct', ascending=False, key=abs)
                    
                    st.dataframe(
                        df.style.format({
                            'ltp': '₹{:.2f}',
                            'prev_close': '₹{:.2f}',
                            'change': '₹{:+.2f}',
                            'change_pct': '{:+.2f}%',
                            'volume': '{:,.0f}'
                        }).applymap(
                            lambda x: 'color: green' if isinstance(x, (int, float)) and x > 0 else 'color: red' if isinstance(x, (int, float)) and x < 0 else '',
                            subset=['change', 'change_pct']
                        ),
                        use_container_width=True
                    )
                else:
                    st.info("No momentum stocks found")
            
            elif scanner_type == "Price Action Patterns":
                results = scan_price_action(symbols, router, exchange)
                
                if results:
                    st.success(f"Found {len(results)} patterns")
                    df = pd.DataFrame(results)
                    
                    st.dataframe(
                        df.style.format({
                            'ltp': '₹{:.2f}'
                        }).applymap(
                            lambda x: 'color: green' if x == 'BUY' else 'color: red' if x == 'SELL' else '',
                            subset=['signal']
                        ),
                        use_container_width=True
                    )
                else:
                    st.info("No patterns found")
    
    # Footer
    st.caption(f"Last scan: {datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    show_intraday_scanner()

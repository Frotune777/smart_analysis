Broker API Data Capabilities - Comparison Report
Executive Summary
This document compares data capabilities across supported brokers (AngelOne, Dhan, Fyers) and existing data sources (NSE, Screener.in, PKScreener).

Universal Recommendation: Use broker APIs for real-time trading data, keep NSE/Screener.in for fundamentals, and PKScreener for screening.

1. Broker API Capabilities Matrix
Feature	AngelOne	Dhan	Fyers	Cost
Real-Time Quotes	✅ Full	✅ Full	✅ Full	FREE
Intraday OHLC	✅ 1m-1h	✅ 1m-1h	✅ 1m-1h	FREE
Daily Historical	✅ 5.5 years	✅ 10+ years	✅ 10+ years	FREE
Market Depth (L2)	✅ Top 5	✅ Top 5	✅ Top 5	FREE
Open Interest	✅ Real-time	✅ Real-time	✅ Real-time	FREE
WebSocket Feed	✅ 1000 symbols	✅ 1000 symbols	✅ 100 symbols	FREE
Order Execution	✅	✅	✅	FREE
Portfolio/Positions	✅	✅	✅	FREE
Fundamentals	❌	❌	❌	N/A
Corporate Actions	❌	❌	❌	N/A
Bulk/Block Deals	❌	❌	❌	N/A
Key Differences
AngelOne:

✅ Most mature API
✅ Excellent documentation
✅ Wide timeframe support
⚠️ Moderate history (5.5 years daily)
Dhan:

✅ Longer historical data
✅ Modern OAuth flow
✅ Clean API design
⚠️ Newer platform
Fyers:

✅ Good documentation
✅ Reliable service
⚠️ Lower WebSocket limit (100 symbols)
⚠️ OAuth required
2. Data Source Comparison
Data Type	Broker APIs	NSE Direct	Screener.in	Best Choice
Real-Time Quotes	✅ All brokers	❌	❌	Broker API
Intraday Charts	✅ All brokers	❌	❌	Broker API
Daily Historical	✅ Limited years	✅ Full history	✅	NSE (more history)
Market Depth	✅ All brokers	❌	❌	Broker API
Open Interest	✅ All brokers	❌	❌	Broker API
Fundamentals	❌ None	❌	✅ Excellent	Screener.in
FII/DII Data	❌ None	✅	❌	NSE
Bulk Deals	❌ None	✅	❌	NSE
Insider Trading	❌ None	✅	❌	NSE
Corporate Actions	❌ None	✅	✅	NSE
Live Streaming	✅ All brokers	❌	❌	Broker API
3. Use Case Recommendations
3.1 Intraday Trading 📊
Primary: Broker API (any) Secondary: None needed

# Use broker for everything
- Real-time quotes
- 1m/5m/15m candles
- Market depth
- Order execution
3.2 Swing/Positional Trading 📈
Hybrid Approach:

# Broker API: Real-time monitoring
- Live prices
- Entry/exit execution
- Position tracking
# NSE: Market context
- Daily historical data
- FII/DII activity
- Bulk deals
# Screener.in: Stock selection
- Fundamental screening
- Quality metrics
3.3 Long-Term Investing 💼
Primary: Screener.in + NSE Broker: Only for execution

# Screener.in: Analysis
- Fundamental screening
- Financial statements
- Quality scores
# NSE: Market data
- Long-term history
- Institutional activity
# Broker: Execution only
- Place orders
- Track holdings
3.4 Algorithmic Trading 🤖
Primary: Broker API WebSocket Secondary: NSE for backtesting

# Broker WebSocket: Live feed
- Tick-by-tick data
- Real-time execution
- Position monitoring
# NSE: Historical testing
- Backtest strategies
- Validate signals
4. Hybrid Data Strategy
Smart Data Router Pattern
class SmartDataRouter:
    """Route data requests to optimal source"""
    
    def __init__(self):
        self.broker = BrokerAPI()  # Any broker
        self.nse = NSEDataFetcher()
        self.screener = ScreenerAPI()
    
    def get_price(self, symbol, mode='realtime'):
        """Get price from best source"""
        if mode == 'realtime':
            return self.broker.get_ltp(symbol)
        else:
            return self.nse.get_last_close(symbol)
    
    def get_historical(self, symbol, interval, days):
        """Get historical data from best source"""
        if interval in ['1m', '5m', '15m', '1h']:
            # Intraday: Use broker
            return self.broker.get_history(symbol, interval, days)
        else:
            # Daily: Use NSE (more history)
            return self.nse.get_history(symbol, days)
    
    def get_analysis(self, symbol):
        """Get comprehensive analysis"""
        return {
            'price': self.broker.get_quote(symbol),
            'fundamentals': self.screener.get_metrics(symbol),
            'institutional': self.nse.get_bulk_deals(symbol)
        }
5. Implementation Priority
Phase 1: Real-Time Trading (High Priority)
✅ Broker authentication (Done!)
🔄 Real-time quote display
🔄 Order execution interface
🔄 Position tracking
Phase 2: Intraday Analysis (Medium Priority)
🔄 Intraday chart integration
🔄 Market depth display
🔄 Live price updates
Phase 3: Advanced Features (Low Priority)
🔄 WebSocket live feed
🔄 Algorithmic trading support
🔄 Multi-broker support
Phase 4: Keep Existing (No Changes)
✅ NSE daily data
✅ Screener.in fundamentals
✅ PKScreener screening
✅ FII/DII tracking
6. Broker Selection Guide
Choose AngelOne If:
✅ You want mature, well-documented API
✅ You need proven reliability
✅ You prefer simpler authentication
⚠️ 5.5 years daily history is enough
Choose Dhan If:
✅ You want longer historical data
✅ You prefer modern OAuth
✅ You like clean API design
⚠️ You're okay with newer platform
Choose Fyers If:
✅ You need fewer WebSocket symbols (<100)
✅ You prefer their platform
✅ You want good documentation
Current Status: AngelOne configured ✅

7. Cost Analysis
Source	Monthly Cost	Annual Cost	Value
Broker API	₹0	₹0	Real-time data
NSE Direct	₹0	₹0	Official data
Screener.in	₹0	₹0	Fundamentals
PKScreener	₹0	₹0	Screening
Total	₹0	₹0	Everything! 🎉
8. What NOT to Replace
Keep Using NSE For:
Daily historical (>5-10 years)
FII/DII activity
Bulk & Block deals
Insider trading
Corporate actions
Official market statistics
Keep Using Screener.in For:
Fundamental metrics
Financial statements
Shareholding patterns
Quality scores
Stock screening
Keep Using PKScreener For:
Technical screening
Pattern recognition
Bulk analysis
9. Integration Architecture
┌─────────────────────────────────────────────────────────┐
│                   Trading Dashboard                      │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Broker API  │  │  NSE Direct  │  │ Screener.in  │
│              │  │              │  │              │
│ • Real-time  │  │ • Daily OHLC │  │ • PE, ROE    │
│ • Intraday   │  │ • FII/DII    │  │ • Financials │
│ • Orders     │  │ • Bulk Deals │  │ • Quality    │
│ • Positions  │  │ • Insider    │  │ • Screening  │
└──────────────┘  └──────────────┘  └──────────────┘
10. Summary
Best Strategy: Hybrid Approach

✅ Use Broker API for:

Real-time quotes
Intraday charts
Order execution
Live monitoring
WebSocket feed
✅ Keep NSE for:

Long-term history
Market statistics
Institutional data
✅ Keep Screener.in for:

Fundamentals
Stock screening
Quality analysis
✅ Keep PKScreener for:

Technical screening
Pattern detection
You have the perfect setup! Just add broker API for real-time capabilities. 🚀

Appendix: Quick Reference
Broker API Endpoints (Common)
/quote - Real-time quotes
/history - Historical OHLC
/depth - Market depth
/orders - Order management
/positions - Position tracking
/holdings - Portfolio holdings
Data Refresh Rates
Broker API: Real-time (tick-by-tick)
NSE: End of day
Screener.in: Daily updates
PKScreener: On-demand
Rate Limits
AngelOne: Generous (no published limits)
Dhan: Generous (no published limits)
Fyers: Generous (no published limits)
NSE: No limits for historical
Screener.in: Moderate (scraping limits)
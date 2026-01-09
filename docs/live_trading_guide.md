# Live Trading User Guide

## Getting Started with Live Trading

### Prerequisites
1. **Broker Account**: Active account with AngelOne, Dhan, or Fyers
2. **API Credentials**: API key from your broker
3. **System Requirements**: Python 3.8+, Streamlit, TA-Lib

---

## Step 1: Broker Configuration

### Navigate to Broker Configuration
1. Open dashboard
2. Go to **CONFIG** → **Broker Configuration**
3. Select your broker (AngelOne/Dhan/Fyers)

### Enter Credentials
- **AngelOne**: API Key only (Client Code, Password, TOTP requested at login)
- **Dhan**: API Key, API Secret, Client ID
- **Fyers**: API Key, API Secret

### Activate Broker
1. Click **Save Credentials**
2. Click **Activate** to set as active broker
3. Status will show 🟢 when ready

---

## Step 2: Live Quotes

### Access Live Quotes
**Navigation**: TRADING → Live Quotes

### Features
- **Real-time prices**: Auto-refresh every 5 seconds when market is open
- **Watchlist**: Add/remove symbols
- **Bid/Ask spread**: See current market depth
- **Volume tracking**: Monitor trading activity

### Using Watchlist
1. Click **➕ Add Symbol** in sidebar
2. Enter symbol name (e.g., SBIN, RELIANCE)
3. Select exchange (NSE/BSE)
4. Click **Add to Watchlist**

### Remove Symbols
1. Select symbols from dropdown
2. Click **Remove Selected**

---

## Step 3: Order Placement

### Access Order Placement
**Navigation**: TRADING → Order Placement

### Order Types
- **MARKET**: Execute at current market price
- **LIMIT**: Execute at specified price or better
- **SL (Stop Loss)**: Trigger at stop price, execute at limit
- **SL-M (Stop Loss Market)**: Trigger at stop price, execute at market

### Product Types
- **MIS (Intraday)**: Square off before market close
- **CNC (Delivery)**: Hold for delivery
- **NRML (Normal)**: For F&O positions

### Placing an Order

#### Basic Order
1. Enter **Symbol** (e.g., SBIN)
2. Select **Exchange** (NSE/BSE/NFO)
3. Choose **Action** (BUY/SELL)
4. Select **Order Type**
5. Enter **Quantity**
6. Set **Price** (if Limit/SL order)
7. Click **🚀 Place Order**

#### Using Position Sizing Calculator
1. Expand **📐 Position Sizing Calculator**
2. Enter:
   - **Capital**: Total trading capital
   - **Risk %**: Risk per trade (e.g., 1%)
   - **Entry Price**: Planned entry
   - **Stop Loss**: Stop loss price
3. Click **Calculate**
4. Use suggested quantity

**Formula**: 
```
Quantity = (Capital × Risk%) / (Entry - Stop Loss)
```

### Quick Trade from Stock Analysis
1. Go to **Stock Analysis**
2. Select symbol
3. Click **🟢 BUY** or **🔴 SELL**
4. Auto-fills order form with current price

---

## Step 4: Position Monitoring

### Access Positions
**Navigation**: TRADING → Positions

### View Open Positions
- **Live P&L**: Real-time profit/loss
- **Entry Price**: Your entry point
- **Current Price**: Live market price
- **Quantity**: Position size
- **% Change**: Performance

### Portfolio Summary
- **Total Positions**: Number of open trades
- **Invested**: Total capital deployed
- **Current Value**: Live portfolio value
- **Total P&L**: Overall profit/loss

### Exit Position
1. Find position in list
2. Click **❌ Exit** button
3. Confirm exit (integration pending)

### Auto-Refresh
- Toggle **Auto-refresh (10 sec)** for live updates
- Manual refresh with **🔄 Refresh** button

---

## Step 5: Intraday Analysis

### Intraday Charts
**Navigation**: INTRADAY → Intraday Charts

#### Features
- **Timeframes**: 1m, 5m, 15m, 30m, 1h
- **Technical Indicators**: SMA, EMA, RSI, MACD (TA-Lib)
- **Volume Profile**: Color-coded volume bars
- **Interactive Charts**: Zoom, pan, hover details

#### Using Charts
1. Enter **Symbol**
2. Select **Exchange**
3. Choose **Timeframe**
4. Adjust **Days of history** (1-30)
5. Enable indicators in **📊 Technical Indicators**
6. Click **🔄 Refresh Data**

### Market Depth
**Navigation**: INTRADAY → Market Depth

#### Features
- **Top 5 Bids/Asks**: Order book levels
- **Cumulative Quantity**: Total at each level
- **Spread Analysis**: Bid-ask spread %
- **Price Impact Calculator**: Estimate execution price

#### Using Price Impact
1. Enter **Order Quantity**
2. View **Buy Impact** (for market buy)
3. View **Sell Impact** (for market sell)
4. See **Average Price** for execution

### Intraday Scanner
**Navigation**: INTRADAY → Intraday Scanner

#### Scanner Types
1. **Volume Breakout**: Stocks with unusual volume
2. **Momentum**: Stocks with strong % moves
3. **Price Action Patterns**: Bullish/bearish patterns

#### Running a Scan
1. Select **Scanner Type**
2. Enter **Symbol List** (comma-separated)
3. Set **Parameters** (threshold, min change)
4. Click **🔍 Scan Now**
5. View results in sortable table

---

## Market Hours

### Trading Hours (IST)
- **Pre-Open**: 9:00 AM - 9:15 AM
- **Normal**: 9:15 AM - 3:30 PM
- **Post-Close**: 3:30 PM - 4:00 PM

### Auto-Refresh Behavior
- **Market Open**: Auto-refresh enabled by default
- **Market Closed**: Auto-refresh disabled, manual refresh available

---

## Best Practices

### Risk Management
1. **Never risk more than 1-2%** per trade
2. **Always use stop losses**
3. **Position size appropriately**
4. **Diversify across sectors**

### Order Execution
1. **Check live price** before placing orders
2. **Use limit orders** in volatile markets
3. **Monitor market depth** for liquidity
4. **Avoid market orders** in illiquid stocks

### Position Management
1. **Monitor P&L regularly**
2. **Trail stop losses** on winning trades
3. **Cut losses quickly**
4. **Let winners run**

### Intraday Trading
1. **Trade liquid stocks** (high volume)
2. **Avoid first 15 minutes** (volatile)
3. **Square off before 3:15 PM**
4. **Use technical indicators** for entry/exit

---

## Troubleshooting

### No Live Data
- **Check broker status**: CONFIG → Broker Configuration
- **Verify credentials**: Ensure API key is correct
- **Check market hours**: Market must be open for live data

### Order Placement Issues
- **Broker not authenticated**: Complete runtime authentication
- **Invalid symbol**: Verify symbol name and exchange
- **Insufficient margin**: Check available funds

### Position Not Showing
- **Refresh page**: Click 🔄 Refresh
- **Check broker**: Positions from active broker only
- **Mock data**: Using demo positions if no real trades

---

## Keyboard Shortcuts

- **Ctrl + R**: Refresh current page
- **Ctrl + B**: Quick BUY (from stock analysis)
- **Ctrl + S**: Quick SELL (from stock analysis)

---

## Support

For issues or questions:
1. Check **Documentation** in sidebar
2. Review **Broker Setup Guide**
3. Check terminal logs for errors
4. Verify broker API status

---

## Safety Reminders

⚠️ **Important**:
- This is a **live trading system**
- Real money is at risk
- Always test with small positions first
- Never trade more than you can afford to lose
- Keep API credentials secure
- Monitor positions actively

✅ **Good Practices**:
- Start with paper trading
- Use position sizing calculator
- Set stop losses on every trade
- Review trades regularly
- Keep trading journal

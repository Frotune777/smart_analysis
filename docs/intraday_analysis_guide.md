# Intraday Analysis Guide

## Overview

The intraday analysis suite provides professional-grade tools for analyzing intraday price movements, market depth, and scanning for trading opportunities.

---

## Intraday Charts

### Accessing Charts
**Navigation**: INTRADAY → Intraday Charts

### Timeframe Selection

#### Available Timeframes
- **1 minute**: Scalping, very short-term trades
- **5 minutes**: Short-term intraday moves
- **15 minutes**: Medium-term intraday trends
- **30 minutes**: Longer intraday swings
- **1 hour**: Full session analysis

#### Choosing the Right Timeframe
- **Scalping**: Use 1m or 5m
- **Day Trading**: Use 5m or 15m
- **Swing Intraday**: Use 30m or 1h
- **Trend Analysis**: Use 1h

### Technical Indicators (TA-Lib)

#### Simple Moving Average (SMA 20)
- **Purpose**: Identify trend direction
- **Signal**: Price above SMA = Bullish, below = Bearish
- **Use**: Support/resistance levels

#### Exponential Moving Average (EMA 50)
- **Purpose**: Faster trend detection
- **Signal**: Crossovers indicate trend changes
- **Use**: Dynamic support/resistance

#### Relative Strength Index (RSI 14)
- **Range**: 0-100
- **Overbought**: >70 (potential reversal down)
- **Oversold**: <30 (potential reversal up)
- **Use**: Identify momentum and reversals

#### MACD (12, 26, 9)
- **Components**: MACD line, Signal line, Histogram
- **Signal**: MACD crosses above signal = Bullish
- **Use**: Trend strength and direction

### Volume Profile

#### Understanding Volume
- **Green bars**: Buying pressure (close > open)
- **Red bars**: Selling pressure (close < open)
- **High volume**: Strong conviction
- **Low volume**: Weak moves, potential reversals

#### Volume Analysis
1. **Volume Confirmation**: Price moves with high volume are stronger
2. **Volume Divergence**: Price up, volume down = weak trend
3. **Volume Spikes**: Indicate significant events

### Chart Interaction

#### Zoom and Pan
- **Zoom**: Scroll wheel or pinch
- **Pan**: Click and drag
- **Reset**: Double-click chart

#### Hover Details
- Hover over candle for OHLC data
- Hover over indicator for values
- Hover over volume for exact numbers

---

## Market Depth

### Accessing Market Depth
**Navigation**: INTRADAY → Market Depth

### Understanding the Order Book

#### Bid Side (Buy Orders)
- **Green**: Buyers waiting
- **Price**: Willing to pay
- **Quantity**: Number of shares
- **Cumulative**: Total up to that level

#### Ask Side (Sell Orders)
- **Red**: Sellers waiting
- **Price**: Asking price
- **Quantity**: Shares available
- **Cumulative**: Total supply

### Spread Analysis

#### Bid-Ask Spread
```
Spread = Ask Price - Bid Price
Spread % = (Spread / Bid Price) × 100
```

#### Interpreting Spread
- **Tight spread** (<0.1%): Liquid stock, easy to trade
- **Wide spread** (>0.5%): Illiquid, higher cost
- **Normal spread** (0.1-0.5%): Moderate liquidity

### Price Impact Calculator

#### What is Price Impact?
The difference between expected price and actual execution price due to order size.

#### Using the Calculator
1. Enter your **Order Quantity**
2. View **Buy Impact**: Cost of market buy
3. View **Sell Impact**: Cost of market sell
4. See **Average Price**: Actual execution price

#### Example
```
Best Bid: ₹100.00
Best Ask: ₹100.50
Order: 1000 shares

Buy Impact:
- Fills at ₹100.50, ₹100.55, ₹100.60
- Average: ₹100.55
- Impact: 0.55% above best ask

Sell Impact:
- Fills at ₹100.00, ₹99.95, ₹99.90
- Average: ₹99.95
- Impact: 0.05% below best bid
```

### Trading with Market Depth

#### When to Use Limit Orders
- Wide spread (>0.3%)
- Large order size
- Illiquid stocks
- Non-urgent trades

#### When to Use Market Orders
- Tight spread (<0.1%)
- Small order size
- Urgent execution needed
- Highly liquid stocks

---

## Intraday Scanner

### Accessing Scanner
**Navigation**: INTRADAY → Intraday Scanner

### Scanner Types

#### 1. Volume Breakout Scanner

**Purpose**: Find stocks with unusual volume activity

**How It Works**:
- Compares current volume to 20-period average
- Flags stocks exceeding threshold (default 2x)

**Settings**:
- **Threshold**: 1.5x to 5x (default 2x)
- Higher threshold = fewer, stronger signals

**Interpretation**:
- **Volume Ratio >2x**: Strong interest
- **Volume Ratio >3x**: Very strong, investigate news
- **Volume Ratio >5x**: Extreme, major event

**Trading Strategy**:
1. Scan for volume breakouts
2. Check price action (up or down?)
3. Look for news/catalysts
4. Enter on pullback with volume confirmation

#### 2. Momentum Scanner

**Purpose**: Find stocks with strong price movements

**How It Works**:
- Calculates % change from previous close
- Filters by minimum threshold

**Settings**:
- **Min % Change**: 1% to 10% (default 2%)
- Lower threshold = more results

**Interpretation**:
- **+2% to +5%**: Moderate bullish momentum
- **+5% to +10%**: Strong bullish momentum
- **>+10%**: Extreme move, caution
- Negative values: Bearish momentum

**Trading Strategy**:
1. Scan for momentum stocks
2. Check if trend is sustainable
3. Look for continuation patterns
4. Enter on retest of breakout level

#### 3. Price Action Patterns

**Purpose**: Identify candlestick patterns

**Patterns Detected**:

**Bullish Engulfing**:
- Previous candle: Red (bearish)
- Current candle: Green (bullish)
- Current opens below previous close
- Current closes above previous open
- **Signal**: Potential reversal up

**Bearish Engulfing**:
- Previous candle: Green (bullish)
- Current candle: Red (bearish)
- Current opens above previous close
- Current closes below previous open
- **Signal**: Potential reversal down

**Trading Strategy**:
1. Scan for patterns
2. Confirm with volume
3. Check support/resistance levels
4. Enter on next candle confirmation

### Using the Scanner

#### Step-by-Step
1. **Select Scanner Type**
2. **Enter Symbol List**:
   ```
   SBIN, RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK
   ```
3. **Set Parameters**:
   - Volume threshold: 2.0x
   - Min change: 2.0%
4. **Click 🔍 Scan Now**
5. **Review Results**:
   - Sort by volume ratio or % change
   - Click symbol to analyze

#### Best Practices
- **Scan regularly**: Every 15-30 minutes
- **Focus on liquid stocks**: High volume
- **Combine scanners**: Volume + Momentum
- **Verify with charts**: Don't trade on scanner alone
- **Check news**: Understand why stock is moving

---

## Intraday Trading Strategies

### Strategy 1: Trend Following

**Timeframe**: 15m or 30m

**Setup**:
1. Price above EMA 50 (uptrend)
2. RSI between 40-70 (not overbought)
3. Volume increasing

**Entry**:
- Buy on pullback to EMA 50
- Or buy on breakout of previous high

**Exit**:
- Stop loss: Below recent swing low
- Target: 1:2 risk-reward

### Strategy 2: Range Trading

**Timeframe**: 5m or 15m

**Setup**:
1. Identify support and resistance
2. Price oscillating between levels
3. RSI confirming overbought/oversold

**Entry**:
- Buy at support with RSI <30
- Sell at resistance with RSI >70

**Exit**:
- Stop loss: Beyond support/resistance
- Target: Opposite side of range

### Strategy 3: Breakout Trading

**Timeframe**: 5m or 15m

**Setup**:
1. Consolidation pattern
2. Volume drying up
3. Tight range

**Entry**:
- Buy on breakout above resistance
- Must have volume spike (>2x average)

**Exit**:
- Stop loss: Below breakout level
- Target: Range height added to breakout

### Strategy 4: MACD Crossover

**Timeframe**: 15m or 1h

**Setup**:
1. MACD crosses above signal line
2. Histogram turning positive
3. Price above EMA 50

**Entry**:
- Buy on crossover confirmation

**Exit**:
- Stop loss: Below recent swing low
- Exit when MACD crosses below signal

---

## Risk Management for Intraday

### Position Sizing
```
Position Size = (Account × Risk%) / (Entry - Stop Loss)
```

**Example**:
- Account: ₹1,00,000
- Risk: 1% = ₹1,000
- Entry: ₹100
- Stop: ₹98
- Position: ₹1,000 / ₹2 = 500 shares

### Stop Loss Placement

**For Longs**:
- Below recent swing low
- Below support level
- Below entry - (2 × ATR)

**For Shorts**:
- Above recent swing high
- Above resistance level
- Above entry + (2 × ATR)

### Time-Based Stops

**Avoid**:
- First 15 minutes (9:15-9:30): High volatility
- Last 15 minutes (3:15-3:30): Closing volatility

**Best Times**:
- 9:30-11:00: Morning momentum
- 11:00-2:00: Midday trends
- 2:00-3:15: Afternoon moves

---

## Performance Tracking

### Metrics to Track
1. **Win Rate**: % of profitable trades
2. **Average Win**: Average profit per winning trade
3. **Average Loss**: Average loss per losing trade
4. **Risk-Reward**: Avg Win / Avg Loss
5. **Profit Factor**: Total Profit / Total Loss

### Trading Journal
Record for each trade:
- Date and time
- Symbol and timeframe
- Entry and exit prices
- Position size
- Stop loss and target
- Reason for entry
- Outcome and lessons

---

## Common Mistakes to Avoid

1. **Overtrading**: Too many trades, high costs
2. **No stop loss**: Unlimited risk
3. **Revenge trading**: Emotional decisions
4. **Ignoring volume**: Weak confirmations
5. **Fighting the trend**: Low probability
6. **Large positions**: Excessive risk
7. **No plan**: Random entries/exits

---

## Advanced Tips

### Multi-Timeframe Analysis
1. **1h chart**: Identify trend
2. **15m chart**: Find entry setup
3. **5m chart**: Time precise entry

### Volume Price Analysis
- **Price up, Volume up**: Strong uptrend
- **Price up, Volume down**: Weak, potential reversal
- **Price down, Volume up**: Strong downtrend
- **Price down, Volume down**: Weak, potential reversal

### Support and Resistance
- Previous day high/low
- Opening price
- VWAP (Volume Weighted Average Price)
- Round numbers (₹100, ₹500, ₹1000)

---

## Conclusion

Intraday analysis requires:
- **Technical skills**: Chart reading, indicators
- **Discipline**: Following rules, managing risk
- **Practice**: Paper trading first
- **Patience**: Waiting for setups
- **Continuous learning**: Adapting to markets

Start small, trade liquid stocks, and always use stop losses!

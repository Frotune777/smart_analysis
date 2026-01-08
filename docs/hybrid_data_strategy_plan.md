# Hybrid Data Strategy - Implementation Plan

## Overview

Implement a smart data routing system that uses broker APIs for real-time trading data while maintaining existing sources (NSE, Screener.in, PKScreener) for their strengths.

**Goal**: Combine best of all worlds - real-time trading + comprehensive analysis + zero cost

---

## Phase 1: Core Infrastructure (Week 1)

### 1.1 Smart Data Router Module

**File**: `libs/smart_data_router.py`

```python
class SmartDataRouter:
    """Intelligent data source selection"""
    
    def __init__(self):
        self.broker = None  # Set based on active broker
        self.nse = NSEDataFetcher()
        self.screener = ScreenerAPI()
        self.cache = DataCache()
    
    def get_quote(self, symbol, exchange='NSE'):
        """Real-time quote - always from broker"""
        
    def get_history(self, symbol, interval, days):
        """Smart historical data routing"""
        
    def get_analysis(self, symbol):
        """Comprehensive multi-source analysis"""
```

**Key Features**:
- Automatic source selection based on data type
- Caching to reduce API calls
- Fallback mechanisms
- Error handling

### 1.2 Broker Data Adapter

**File**: `libs/broker_data_adapter.py`

```python
class BrokerDataAdapter:
    """Unified interface for all brokers"""
    
    def __init__(self, broker_name):
        self.broker = self._load_broker(broker_name)
    
    def get_quote(self, symbol, exchange):
        """Standardized quote interface"""
        
    def get_history(self, symbol, interval, start, end):
        """Standardized historical data"""
        
    def get_depth(self, symbol, exchange):
        """Standardized market depth"""
```

**Supports**:
- AngelOne
- Dhan
- Fyers
- Easy to add more

---

## Phase 2: Real-Time Features (Week 2)

### 2.1 Live Quote Display

**File**: `pages/live_quotes.py`

**Features**:
- Real-time price updates
- Bid/Ask spread
- Volume, OI
- % change indicators
- Auto-refresh (5 seconds)

**UI Components**:
```python
def show_live_quotes():
    st.header("📊 Live Market Quotes")
    
    # Symbol selector
    symbols = st.multiselect("Select Symbols", watchlist)
    
    # Live quote cards
    for symbol in symbols:
        quote = router.get_quote(symbol)
        display_quote_card(quote)
```

### 2.2 Order Execution Interface

**File**: `pages/order_placement.py`

**Features**:
- Quick order form
- Market/Limit/SL orders
- Position sizing calculator
- Risk management checks
- One-click execution

**Integration**:
- Uses active broker from `broker_manager`
- Real-time price validation
- Position tracking

### 2.3 Position Monitor

**File**: `pages/positions.py`

**Features**:
- Live P&L tracking
- Position-wise breakdown
- Auto-refresh
- Quick exit buttons
- Risk metrics

---

## Phase 3: Intraday Analysis (Week 3)

### 3.1 Intraday Charts

**File**: `pages/intraday_charts.py`

**Features**:
- 1m, 5m, 15m, 1h candles
- Volume profile
- Technical indicators
- Drawing tools
- Multiple timeframes

**Data Source**: Broker API (real-time)

### 3.2 Market Depth Viewer

**File**: `components/market_depth.py`

**Features**:
- Top 5 bid/ask levels
- Order book visualization
- Cumulative quantity
- Price impact calculator
- Real-time updates

### 3.3 Intraday Scanner

**File**: `pages/intraday_scanner.py`

**Features**:
- Volume breakouts
- Price action patterns
- Momentum indicators
- Real-time screening
- Alert system

---

## Phase 4: Integration with Existing Features (Week 4)

### 4.1 Enhance Stock Analysis Page

**Modifications**: `pages/stock_analysis.py`

**Add**:
- Real-time price header
- Live P&L if position exists
- Quick trade buttons
- Market depth widget

**Keep**:
- Daily charts (from NSE)
- Technical indicators
- Big money tracker
- Corporate milestones

### 4.2 Enhance Quad Report

**Modifications**: `libs/quad_analyzer.py`

**Add**:
- Real-time price in report
- Live market sentiment
- Intraday momentum score

**Keep**:
- Fundamental analysis (Screener.in)
- Technical analysis (NSE daily)
- Institutional analysis (NSE)
- Macro analysis (NSE)

### 4.3 Enhance Dashboard Home

**Modifications**: `dashboard.py`

**Add**:
- Live market status
- Active positions widget
- Today's P&L summary
- Quick trade panel

**Keep**:
- All existing pages
- Market overview
- Big money tracker
- Strategy screener

---

## Phase 5: Advanced Features (Week 5-6)

### 5.1 WebSocket Live Feed

**File**: `libs/websocket_manager.py`

**Features**:
- Multi-symbol streaming
- Connection pooling
- Auto-reconnect
- Data buffering
- Event callbacks

**Use Cases**:
- Live charts
- Price alerts
- Algo trading
- Market scanner

### 5.2 Algo Trading Framework

**File**: `libs/algo_trader.py`

**Features**:
- Strategy backtesting (NSE data)
- Live execution (Broker API)
- Risk management
- Performance tracking
- Paper trading mode

### 5.3 Multi-Broker Support

**Enhancement**: `libs/broker_manager.py`

**Features**:
- Switch between brokers
- Compare execution quality
- Aggregate positions
- Unified order book

---

## Implementation Details

### File Structure

```
trader_start/
├── libs/
│   ├── smart_data_router.py      [NEW]
│   ├── broker_data_adapter.py    [NEW]
│   ├── websocket_manager.py      [NEW]
│   ├── algo_trader.py             [NEW]
│   ├── broker_manager.py          [ENHANCE]
│   ├── quad_analyzer.py           [ENHANCE]
│   └── ...existing files...
├── pages/
│   ├── live_quotes.py             [NEW]
│   ├── order_placement.py         [NEW]
│   ├── positions.py               [NEW]
│   ├── intraday_charts.py         [NEW]
│   ├── intraday_scanner.py        [NEW]
│   ├── stock_analysis.py          [ENHANCE]
│   └── ...existing files...
├── components/
│   ├── market_depth.py            [NEW]
│   ├── quote_card.py              [NEW]
│   ├── order_form.py              [NEW]
│   └── ...existing files...
└── dashboard.py                    [ENHANCE]
```

---

## Data Flow Architecture

```
User Request
     │
     ▼
SmartDataRouter
     │
     ├─► Real-time? ──► Broker API
     │
     ├─► Intraday? ──► Broker API
     │
     ├─► Daily? ──────► NSE (if >5 years)
     │                  └─► Broker (if recent)
     │
     ├─► Fundamentals? ► Screener.in
     │
     └─► Screening? ───► PKScreener
```

---

## Database Schema Updates

### New Tables

```sql
-- Live quotes cache
CREATE TABLE live_quotes (
    symbol TEXT,
    exchange TEXT,
    ltp REAL,
    bid REAL,
    ask REAL,
    volume INTEGER,
    timestamp DATETIME,
    PRIMARY KEY (symbol, exchange)
);

-- Intraday candles cache
CREATE TABLE intraday_candles (
    symbol TEXT,
    exchange TEXT,
    interval TEXT,
    timestamp INTEGER,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    PRIMARY KEY (symbol, exchange, interval, timestamp)
);

-- Order history
CREATE TABLE order_history (
    order_id TEXT PRIMARY KEY,
    broker TEXT,
    symbol TEXT,
    exchange TEXT,
    action TEXT,
    quantity INTEGER,
    price REAL,
    status TEXT,
    timestamp DATETIME
);
```

---

## Configuration Updates

### `.env` additions

```bash
# Data source preferences
USE_BROKER_FOR_REALTIME=true
USE_BROKER_FOR_INTRADAY=true
USE_NSE_FOR_DAILY=true
USE_SCREENER_FOR_FUNDAMENTALS=true

# Cache settings
QUOTE_CACHE_SECONDS=5
INTRADAY_CACHE_MINUTES=1
DAILY_CACHE_HOURS=24

# WebSocket settings
WEBSOCKET_ENABLED=false
WEBSOCKET_SYMBOLS_LIMIT=100
```

---

## Testing Strategy

### Unit Tests
- `test_smart_data_router.py`
- `test_broker_data_adapter.py`
- `test_websocket_manager.py`

### Integration Tests
- Broker API connectivity
- Data source fallbacks
- Cache mechanisms
- Order execution flow

### User Acceptance Tests
- Live quote display
- Order placement
- Position tracking
- Chart rendering

---

## Rollout Plan

### Week 1: Infrastructure
- [x] Broker authentication (Done!)
- [ ] Smart data router
- [ ] Broker data adapter
- [ ] Unit tests

### Week 2: Core Features
- [ ] Live quotes page
- [ ] Order placement
- [ ] Position monitor
- [ ] Integration tests

### Week 3: Analysis Tools
- [ ] Intraday charts
- [ ] Market depth
- [ ] Intraday scanner
- [ ] UI/UX refinement

### Week 4: Integration
- [ ] Enhance existing pages
- [ ] Dashboard updates
- [ ] Navigation updates
- [ ] User testing

### Week 5-6: Advanced (Optional)
- [ ] WebSocket feed
- [ ] Algo trading
- [ ] Multi-broker
- [ ] Performance optimization

---

## Success Metrics

### Performance
- Quote latency: <1 second
- Chart load: <2 seconds
- Order execution: <500ms
- WebSocket uptime: >99%

### User Experience
- Seamless broker switching
- No data source confusion
- Clear error messages
- Intuitive navigation

### Cost
- Total cost: ₹0 (all free APIs)
- API call optimization
- Efficient caching

---

## Risk Mitigation

### API Failures
- Automatic fallback to cached data
- Multiple data source options
- Clear error notifications
- Retry mechanisms

### Data Quality
- Validation checks
- Anomaly detection
- Source verification
- User alerts

### Performance
- Lazy loading
- Data pagination
- Background updates
- Connection pooling

---

## Maintenance Plan

### Daily
- Monitor API health
- Check error logs
- Verify data quality

### Weekly
- Clear old cache
- Review performance metrics
- Update documentation

### Monthly
- API version updates
- Feature enhancements
- User feedback review

---

## Documentation

### User Guides
- [ ] Live trading guide
- [ ] Order placement tutorial
- [ ] Position management
- [ ] Intraday analysis guide

### Developer Docs
- [ ] API integration guide
- [ ] Data router architecture
- [ ] Adding new brokers
- [ ] Troubleshooting guide

---

## Next Steps

1. **Review this plan** - Confirm approach
2. **Set priorities** - Which features first?
3. **Start Week 1** - Build infrastructure
4. **Iterate** - Add features incrementally

**Current Status**: ✅ Broker authentication complete, ready to proceed!

"""
Smart Data Router - Intelligent data source selection

This module routes data requests to the optimal source:
- Broker API: Real-time quotes, intraday data, live feeds
- NSE: Long-term daily data, market statistics
- Screener.in: Fundamental metrics
- PKScreener: Technical screening

Author: Smart Analysis System
"""
import os
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
import pandas as pd
from libs.broker_manager import BrokerManager
from libs.broker_data_adapter import BrokerDataAdapter


class DataCache:
    """Simple in-memory cache for data"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {
            'quote': 5,  # 5 seconds for quotes
            'intraday': 60,  # 1 minute for intraday
            'daily': 3600  # 1 hour for daily
        }
    
    def get(self, key: str, data_type: str = 'quote') -> Optional[Any]:
        """Get cached data if not expired"""
        if key not in self.cache:
            return None
        
        cached_data, timestamp = self.cache[key]
        ttl = self.cache_ttl.get(data_type, 60)
        
        if (datetime.now() - timestamp).seconds > ttl:
            del self.cache[key]
            return None
        
        return cached_data
    
    def set(self, key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[key] = (data, datetime.now())
    
    def clear(self):
        """Clear all cached data"""
        self.cache.clear()


class SmartDataRouter:
    """
    Intelligent data routing to optimal sources
    
    Routes requests based on:
    - Data type (real-time, intraday, daily, fundamental)
    - Data age requirements
    - Source availability
    - Cost optimization (all free!)
    """
    
    def __init__(self):
        self.broker_manager = BrokerManager()
        self.broker_adapter = None
        self.cache = DataCache()
        
        # Initialize broker adapter if active broker exists
        active_broker = self.broker_manager.get_active_broker()
        if active_broker:
            self.broker_adapter = BrokerDataAdapter(active_broker)
        
        # Data source preferences from environment
        self.use_broker_realtime = os.getenv('USE_BROKER_FOR_REALTIME', 'true').lower() == 'true'
        self.use_broker_intraday = os.getenv('USE_BROKER_FOR_INTRADAY', 'true').lower() == 'true'
        self.use_nse_daily = os.getenv('USE_NSE_FOR_DAILY', 'true').lower() == 'true'
    
    def get_quote(self, symbol: str, exchange: str = 'NSE', use_cache: bool = True) -> Optional[Dict]:
        """
        Get real-time quote - always from broker API
        
        Args:
            symbol: Stock symbol
            exchange: Exchange (NSE, BSE, NFO, etc.)
            use_cache: Whether to use cached data
            
        Returns:
            Dict with quote data or None
        """
        cache_key = f"quote_{symbol}_{exchange}"
        
        # Check cache first
        if use_cache:
            cached = self.cache.get(cache_key, 'quote')
            if cached:
                return cached
        
        # Get from broker API
        if not self.broker_adapter:
            return None
        
        try:
            quote = self.broker_adapter.get_quote(symbol, exchange)
            if quote:
                self.cache.set(cache_key, quote)
            return quote
        except Exception as e:
            print(f"Error fetching quote: {e}")
            return None
    
    def get_history(self, symbol: str, interval: str = 'D', 
                   days: int = 365, exchange: str = 'NSE') -> Optional[pd.DataFrame]:
        """
        Get historical data from optimal source
        
        Args:
            symbol: Stock symbol
            interval: Timeframe (1m, 5m, 15m, 1h, D)
            days: Number of days of history
            exchange: Exchange
            
        Returns:
            DataFrame with OHLCV data
        """
        # Intraday data: Use broker API
        if interval in ['1m', '3m', '5m', '10m', '15m', '30m', '1h']:
            return self._get_intraday_history(symbol, interval, days, exchange)
        
        # Daily data: Use NSE if >2000 days, else broker
        elif interval == 'D':
            if days > 2000 and self.use_nse_daily:
                return self._get_nse_daily_history(symbol, days)
            else:
                return self._get_broker_daily_history(symbol, days, exchange)
        
        return None
    
    def _get_intraday_history(self, symbol: str, interval: str, 
                             days: int, exchange: str) -> Optional[pd.DataFrame]:
        """Get intraday data from broker API"""
        if not self.broker_adapter:
            return None
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            df = self.broker_adapter.get_history(
                symbol, exchange, interval,
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
            return df
        except Exception as e:
            print(f"Error fetching intraday history: {e}")
            return None
    
    def _get_broker_daily_history(self, symbol: str, days: int, 
                                  exchange: str) -> Optional[pd.DataFrame]:
        """Get daily data from broker API"""
        if not self.broker_adapter:
            return None
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            df = self.broker_adapter.get_history(
                symbol, exchange, 'D',
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
            return df
        except Exception as e:
            print(f"Error fetching daily history from broker: {e}")
            return None
    
    def _get_nse_daily_history(self, symbol: str, days: int) -> Optional[pd.DataFrame]:
        """Get daily data from NSE (for long-term history)"""
        # TODO: Implement NSE data fetching
        # This will use existing NSE fetcher
        print(f"NSE daily history not yet implemented, falling back to broker")
        return self._get_broker_daily_history(symbol, min(days, 2000), 'NSE')
    
    def get_depth(self, symbol: str, exchange: str = 'NSE') -> Optional[Dict]:
        """
        Get market depth - always from broker API
        
        Args:
            symbol: Stock symbol
            exchange: Exchange
            
        Returns:
            Dict with market depth data
        """
        if not self.broker_adapter:
            return None
        
        try:
            return self.broker_adapter.get_depth(symbol, exchange)
        except Exception as e:
            print(f"Error fetching market depth: {e}")
            return None
    
    def get_fundamentals(self, symbol: str) -> Optional[Dict]:
        """
        Get fundamental data - from Screener.in
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dict with fundamental metrics
        """
        # TODO: Implement Screener.in integration
        # This will use existing screener fetcher
        print(f"Fundamental data fetching not yet implemented")
        return None
    
    def get_comprehensive_data(self, symbol: str, exchange: str = 'NSE') -> Dict:
        """
        Get comprehensive data from all sources
        
        Args:
            symbol: Stock symbol
            exchange: Exchange
            
        Returns:
            Dict with data from all sources
        """
        return {
            'quote': self.get_quote(symbol, exchange),
            'depth': self.get_depth(symbol, exchange),
            'intraday_5m': self.get_history(symbol, '5m', 5, exchange),
            'daily': self.get_history(symbol, 'D', 365, exchange),
            'fundamentals': self.get_fundamentals(symbol)
        }
    
    def get_source_status(self) -> Dict:
        """Get status of all data sources"""
        return {
            'broker': {
                'available': self.broker_adapter is not None,
                'name': self.broker_manager.get_active_broker() if self.broker_adapter else None
            },
            'nse': {
                'available': True,  # Always available
                'enabled': self.use_nse_daily
            },
            'screener': {
                'available': False,  # TODO: Implement
                'enabled': True
            },
            'cache': {
                'size': len(self.cache.cache),
                'enabled': True
            }
        }

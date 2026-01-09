"""
Broker Data Adapter - Unified interface for all brokers

Provides standardized methods for:
- Real-time quotes
- Historical data
- Market depth
- Order execution

Supports: AngelOne, Dhan, Fyers

Author: Smart Analysis System
"""
from typing import Dict, Optional, List
import pandas as pd
from libs.broker_manager import BrokerManager


class BrokerDataAdapter:
    """
    Unified broker interface
    
    Abstracts broker-specific implementations into a common API
    """
    
    def __init__(self, broker_name: str):
        """
        Initialize adapter for specific broker
        
        Args:
            broker_name: Broker name (angel, dhan, fyers)
        """
        self.broker_name = broker_name
        self.broker_manager = BrokerManager()
        
        # Load broker-specific module
        self.broker_data = self._load_broker_module()
        
        # Get authentication token (if available)
        self.auth_token = self._get_auth_token()
    
    def _load_broker_module(self):
        """Load broker-specific data module"""
        try:
            if self.broker_name == 'angel':
                from broker.angel.api.data import BrokerData
                return BrokerData
            elif self.broker_name == 'dhan':
                from broker.dhan.api.data import BrokerData
                return BrokerData
            elif self.broker_name == 'fyers':
                from broker.fyers.api.data import BrokerData
                return BrokerData
            else:
                raise ValueError(f"Unsupported broker: {self.broker_name}")
        except ImportError as e:
            print(f"Error loading broker module: {e}")
            return None
    
    def _get_auth_token(self) -> Optional[str]:
        """Get authentication token for broker"""
        # TODO: Implement token retrieval from session/database
        # For now, return None (will need authentication)
        return None
    
    def get_quote(self, symbol: str, exchange: str) -> Optional[Dict]:
        """
        Get real-time quote
        
        Args:
            symbol: Trading symbol
            exchange: Exchange (NSE, BSE, NFO, etc.)
            
        Returns:
            Dict with quote data:
            {
                'ltp': float,
                'bid': float,
                'ask': float,
                'open': float,
                'high': float,
                'low': float,
                'prev_close': float,
                'volume': int,
                'oi': int (for F&O)
            }
        """
        if not self.broker_data or not self.auth_token:
            return None
        
        try:
            broker_instance = self.broker_data(self.auth_token)
            return broker_instance.get_quotes(symbol, exchange)
        except Exception as e:
            print(f"Error fetching quote from {self.broker_name}: {e}")
            return None
    
    def get_history(self, symbol: str, exchange: str, interval: str,
                   start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        Get historical OHLCV data
        
        Args:
            symbol: Trading symbol
            exchange: Exchange
            interval: Timeframe (1m, 5m, 15m, 1h, D)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with columns:
            [timestamp, open, high, low, close, volume, oi]
        """
        if not self.broker_data or not self.auth_token:
            return None
        
        try:
            broker_instance = self.broker_data(self.auth_token)
            return broker_instance.get_history(
                symbol, exchange, interval,
                start_date, end_date
            )
        except Exception as e:
            print(f"Error fetching history from {self.broker_name}: {e}")
            return None
    
    def get_depth(self, symbol: str, exchange: str) -> Optional[Dict]:
        """
        Get market depth (order book)
        
        Args:
            symbol: Trading symbol
            exchange: Exchange
            
        Returns:
            Dict with market depth:
            {
                'bids': [{'price': float, 'quantity': int}, ...],
                'asks': [{'price': float, 'quantity': int}, ...],
                'ltp': float,
                'volume': int,
                ...
            }
        """
        if not self.broker_data or not self.auth_token:
            return None
        
        try:
            broker_instance = self.broker_data(self.auth_token)
            return broker_instance.get_depth(symbol, exchange)
        except Exception as e:
            print(f"Error fetching depth from {self.broker_name}: {e}")
            return None
    
    def is_authenticated(self) -> bool:
        """Check if broker is authenticated"""
        return self.auth_token is not None
    
    def get_broker_info(self) -> Dict:
        """Get broker information"""
        broker_info = self.broker_manager.SUPPORTED_BROKERS.get(self.broker_name, {})
        return {
            'name': broker_info.get('name', self.broker_name),
            'authenticated': self.is_authenticated(),
            'supports_realtime': True,
            'supports_intraday': True,
            'supports_daily': True,
            'supports_websocket': True
        }


class MultiBrokerAdapter:
    """
    Adapter for managing multiple brokers simultaneously
    
    Useful for:
    - Comparing execution quality
    - Aggregating positions
    - Failover scenarios
    """
    
    def __init__(self):
        self.broker_manager = BrokerManager()
        self.adapters = {}
        
        # Load all configured brokers
        self._load_configured_brokers()
    
    def _load_configured_brokers(self):
        """Load adapters for all configured brokers"""
        configured = self.broker_manager.list_configured_brokers()
        
        for broker in configured:
            try:
                self.adapters[broker['broker']] = BrokerDataAdapter(broker['broker'])
            except Exception as e:
                print(f"Error loading {broker['broker']}: {e}")
    
    def get_quote(self, symbol: str, exchange: str, 
                 broker: Optional[str] = None) -> Optional[Dict]:
        """
        Get quote from specific broker or active broker
        
        Args:
            symbol: Trading symbol
            exchange: Exchange
            broker: Specific broker name (optional)
            
        Returns:
            Quote data
        """
        if broker and broker in self.adapters:
            return self.adapters[broker].get_quote(symbol, exchange)
        
        # Use active broker
        active = self.broker_manager.get_active_broker()
        if active and active in self.adapters:
            return self.adapters[active].get_quote(symbol, exchange)
        
        return None
    
    def get_all_quotes(self, symbol: str, exchange: str) -> Dict[str, Dict]:
        """
        Get quotes from all available brokers
        
        Useful for price comparison
        """
        quotes = {}
        for broker_name, adapter in self.adapters.items():
            quote = adapter.get_quote(symbol, exchange)
            if quote:
                quotes[broker_name] = quote
        return quotes
    
    def get_available_brokers(self) -> List[str]:
        """Get list of available broker names"""
        return list(self.adapters.keys())

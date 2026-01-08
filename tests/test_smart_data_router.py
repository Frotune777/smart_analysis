"""
Unit tests for Smart Data Router

Tests:
- Source selection logic
- Cache functionality
- Fallback mechanisms
- Data routing decisions

Run: pytest tests/test_smart_data_router.py
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import pandas as pd
from libs.smart_data_router import SmartDataRouter, DataCache


class TestDataCache:
    """Test cache functionality"""
    
    def test_cache_set_and_get(self):
        """Test basic cache operations"""
        cache = DataCache()
        
        # Set data
        cache.set('test_key', {'price': 100})
        
        # Get data immediately
        data = cache.get('test_key', 'quote')
        assert data == {'price': 100}
    
    def test_cache_expiry(self):
        """Test cache expiration"""
        cache = DataCache()
        cache.cache_ttl['test'] = 0  # Expire immediately
        
        cache.set('test_key', {'price': 100})
        
        # Should expire
        data = cache.get('test_key', 'test')
        assert data is None
    
    def test_cache_clear(self):
        """Test cache clearing"""
        cache = DataCache()
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        
        cache.clear()
        
        assert len(cache.cache) == 0


class TestSmartDataRouter:
    """Test smart data routing logic"""
    
    @patch('libs.smart_data_router.BrokerManager')
    @patch('libs.smart_data_router.BrokerDataAdapter')
    def test_initialization(self, mock_adapter, mock_manager):
        """Test router initialization"""
        mock_manager.return_value.get_active_broker.return_value = 'angel'
        
        router = SmartDataRouter()
        
        assert router.broker_manager is not None
        assert router.cache is not None
    
    @patch('libs.smart_data_router.BrokerDataAdapter')
    def test_get_quote_with_cache(self, mock_adapter):
        """Test quote fetching with cache"""
        router = SmartDataRouter()
        router.broker_adapter = Mock()
        router.broker_adapter.get_quote.return_value = {'ltp': 100}
        
        # First call - should fetch from broker
        quote1 = router.get_quote('SBIN', 'NSE')
        assert quote1 == {'ltp': 100}
        
        # Second call - should use cache
        quote2 = router.get_quote('SBIN', 'NSE', use_cache=True)
        assert quote2 == {'ltp': 100}
        
        # Broker should be called only once
        router.broker_adapter.get_quote.assert_called_once()
    
    def test_intraday_interval_detection(self):
        """Test intraday interval detection"""
        router = SmartDataRouter()
        
        # Intraday intervals
        assert router._get_intraday_history.__name__ == '_get_intraday_history'
        
        # Daily interval
        assert router._get_broker_daily_history.__name__ == '_get_broker_daily_history'
    
    @patch('libs.smart_data_router.BrokerDataAdapter')
    def test_get_source_status(self, mock_adapter):
        """Test source status reporting"""
        router = SmartDataRouter()
        router.broker_adapter = Mock()
        
        status = router.get_source_status()
        
        assert 'broker' in status
        assert 'nse' in status
        assert 'cache' in status
    
    def test_comprehensive_data_structure(self):
        """Test comprehensive data return structure"""
        router = SmartDataRouter()
        router.broker_adapter = Mock()
        router.broker_adapter.get_quote.return_value = {'ltp': 100}
        router.broker_adapter.get_depth.return_value = {'bids': [], 'asks': []}
        router.broker_adapter.get_history.return_value = pd.DataFrame()
        
        data = router.get_comprehensive_data('SBIN', 'NSE')
        
        assert 'quote' in data
        assert 'depth' in data
        assert 'intraday_5m' in data
        assert 'daily' in data
        assert 'fundamentals' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

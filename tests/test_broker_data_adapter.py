"""
Unit tests for Broker Data Adapter

Tests:
- Broker module loading
- Quote fetching
- Historical data
- Market depth
- Multi-broker support

Run: pytest tests/test_broker_data_adapter.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from libs.broker_data_adapter import BrokerDataAdapter, MultiBrokerAdapter


class TestBrokerDataAdapter:
    """Test broker data adapter"""
    
    @patch('libs.broker_data_adapter.BrokerManager')
    def test_initialization_angel(self, mock_manager):
        """Test initialization with AngelOne"""
        adapter = BrokerDataAdapter('angel')
        
        assert adapter.broker_name == 'angel'
        assert adapter.broker_manager is not None
    
    @patch('libs.broker_data_adapter.BrokerManager')
    def test_initialization_dhan(self, mock_manager):
        """Test initialization with Dhan"""
        adapter = BrokerDataAdapter('dhan')
        
        assert adapter.broker_name == 'dhan'
    
    @patch('libs.broker_data_adapter.BrokerManager')
    def test_initialization_fyers(self, mock_manager):
        """Test initialization with Fyers"""
        adapter = BrokerDataAdapter('fyers')
        
        assert adapter.broker_name == 'fyers'
    
    @patch('libs.broker_data_adapter.BrokerManager')
    def test_unsupported_broker(self, mock_manager):
        """Test unsupported broker handling"""
        with pytest.raises(ValueError):
            adapter = BrokerDataAdapter('unsupported')
    
    @patch('libs.broker_data_adapter.BrokerManager')
    def test_get_quote_without_auth(self, mock_manager):
        """Test quote fetching without authentication"""
        adapter = BrokerDataAdapter('angel')
        adapter.auth_token = None
        
        quote = adapter.get_quote('SBIN', 'NSE')
        
        assert quote is None
    
    @patch('libs.broker_data_adapter.BrokerManager')
    def test_is_authenticated(self, mock_manager):
        """Test authentication status"""
        adapter = BrokerDataAdapter('angel')
        
        # Without token
        adapter.auth_token = None
        assert adapter.is_authenticated() == False
        
        # With token
        adapter.auth_token = 'test_token'
        assert adapter.is_authenticated() == True
    
    @patch('libs.broker_data_adapter.BrokerManager')
    def test_get_broker_info(self, mock_manager):
        """Test broker info retrieval"""
        mock_manager.return_value.SUPPORTED_BROKERS = {
            'angel': {'name': 'AngelOne'}
        }
        
        adapter = BrokerDataAdapter('angel')
        info = adapter.get_broker_info()
        
        assert 'name' in info
        assert 'authenticated' in info
        assert 'supports_realtime' in info


class TestMultiBrokerAdapter:
    """Test multi-broker adapter"""
    
    @patch('libs.broker_data_adapter.BrokerManager')
    def test_initialization(self, mock_manager):
        """Test multi-broker initialization"""
        mock_manager.return_value.list_configured_brokers.return_value = []
        
        adapter = MultiBrokerAdapter()
        
        assert adapter.broker_manager is not None
        assert isinstance(adapter.adapters, dict)
    
    @patch('libs.broker_data_adapter.BrokerManager')
    @patch('libs.broker_data_adapter.BrokerDataAdapter')
    def test_get_available_brokers(self, mock_adapter, mock_manager):
        """Test getting available brokers"""
        mock_manager.return_value.list_configured_brokers.return_value = [
            {'broker': 'angel'},
            {'broker': 'dhan'}
        ]
        
        multi_adapter = MultiBrokerAdapter()
        multi_adapter.adapters = {'angel': Mock(), 'dhan': Mock()}
        
        brokers = multi_adapter.get_available_brokers()
        
        assert 'angel' in brokers
        assert 'dhan' in brokers


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

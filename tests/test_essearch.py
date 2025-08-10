import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the script's directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'search-elasticsearch', 'bin')))

from essearch import EsCommand

def test_es_command_success():
    """Test a successful search query."""
    # Mock Elasticsearch client
    mock_es_client = MagicMock()
    mock_es_client.search.return_value = {
        'hits': {
            'hits': [
                {
                    '_index': 'test_index',
                    '_type': 'test_type',
                    '_id': '1',
                    '_score': 1.0,
                    '_source': {'message': 'hello world'}
                }
            ]
        }
    }

    with patch('essearch.Elasticsearch', return_value=mock_es_client):
        # Instantiate the command
        cmd = EsCommand()
        cmd.q = "test query"
        cmd.index = "test_index"
        cmd.limit = 10

        # Run the generator
        results = list(cmd.generate())

        # Assertions
        assert len(results) == 1
        event = results[0]
        assert event['_id'] == '1'
        assert event['_index'] == 'test_index'
        # Check that the raw event is a JSON string of the original hit
        raw_event = json.loads(event['_raw'])
        assert raw_event['_source']['message'] == 'hello world'

        # Check that the search method was called with the correct arguments
        mock_es_client.search.assert_called_once_with(
            index='test_index',
            query={'query_string': {'query': 'test query'}},
            size=10
        )

def test_es_command_exception():
    """Test the command when Elasticsearch raises an exception."""
    # Mock Elasticsearch client to raise an exception
    mock_es_client = MagicMock()
    mock_es_client.search.side_effect = Exception("Connection error")

    with patch('essearch.Elasticsearch', return_value=mock_es_client):
        # Instantiate the command
        cmd = EsCommand()
        cmd.q = "error query"
        cmd.index = "error_index"
        cmd.limit = 10

        # Run the generator
        results = list(cmd.generate())

        # Assertions
        assert len(results) == 1
        error_event = results[0]
        assert "Error during Elasticsearch search: Connection error" in error_event['_raw']

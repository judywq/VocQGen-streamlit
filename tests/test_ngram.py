import pytest
from unittest.mock import patch, MagicMock
from vocqgen import ngram

# Mock get_general_pos for all tests
@pytest.fixture(autouse=True)
def mock_get_general_pos(monkeypatch):
    monkeypatch.setattr(ngram, "get_general_pos", lambda tag: tag)
    yield

def test_get_last_timeseries():
    data = [
        {"ngram": "dog_NOUN", "type": "NGRAM", "timeseries": [0.1, 0.2, 0.3]},
        {"ngram": "cat_NOUN", "type": "NGRAM", "timeseries": [0.2, 0.3, 0.4]},
    ]
    result = ngram.get_last_timeseries(data)
    assert result == [
        {"ngram": "dog_NOUN", "type": "NGRAM", "last_value": 0.3},
        {"ngram": "cat_NOUN", "type": "NGRAM", "last_value": 0.4},
    ]

@patch("vocqgen.ngram.requests.get")
def test_search_ngram(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"ngram": "dog_NOUN", "type": "NGRAM", "timeseries": [0.1, 0.2, 0.3]},
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    result = ngram.search_ngram("dog_NOUN")
    assert result[0]["ngram"] == "dog_NOUN"
    assert result[0]["last_value"] == 0.3

@patch("vocqgen.ngram.search_ngram")
def test_filter_high_freq_pos(mock_search_ngram):
    # Simulate search_ngram returning two POS, one above threshold
    mock_search_ngram.return_value = [
        {"ngram": "dog_NOUN", "type": "NGRAM", "last_value": 0.5},
        {"ngram": "dog_VERB", "type": "NGRAM", "last_value": 0.01},
    ]
    pos_list = ["NN", "VB"]
    result = ngram.filter_high_freq_pos("dog", pos_list, ratio_against_highest=0.1)
    assert "NN" in result
    assert "VB" not in result

@patch("vocqgen.ngram.search_ngram")
def test_filter_high_freq_inflections(mock_search_ngram):
    inf_data = {"NN": ["dogs", "dog"], "VB": ["dogged"]}
    # Only "dogs" and "dog" above threshold
    mock_search_ngram.return_value = [
        {"ngram": "dogs_NOUN", "type": "NGRAM", "last_value": 0.5},
        {"ngram": "dog_NOUN", "type": "NGRAM", "last_value": 0.05},
        {"ngram": "dogged_VERB", "type": "NGRAM", "last_value": 0.01},
    ]
    result = ngram.filter_high_freq_inflections(inf_data, th=0.1)
    assert "NN" in result
    assert "dogs" in result["NN"]
    assert "dog" in result["NN"]
    assert "VB" not in result or not result["VB"] 
    

def test_search_ngram_real():
    result = ngram.search_ngram("dog_NOUN")
    assert result[0]["ngram"] == "dog_NOUN"
    assert result[0]["last_value"] > 0


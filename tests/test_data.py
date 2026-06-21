import sys
import os
import pytest

# Add parent directory to sys.path to import data
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import data

def test_get_feed_items_no_filters():
    # Free user gets ads
    items = data.get_feed_items("Free", "", "")
    assert isinstance(items, list)
    # Check if there are any ads
    has_ads = any(item.get('type') == 'ad' for item in items)
    assert has_ads

def test_get_feed_items_premium_no_ads():
    items = data.get_feed_items("Premium", "", "")
    has_ads = any(item.get('type') == 'ad' for item in items)
    assert not has_ads

def test_get_feed_items_filters():
    items = data.get_feed_items("Premium", filter_sport="Volleyball", filter_location="München")
    assert all("Volleyball".lower() in item['sport'].lower() for item in items if item.get('type') == 'event')

def test_get_user_events():
    future, past = data.get_user_events()
    assert isinstance(future, list)
    assert isinstance(past, list)
    for e in future:
        assert e['is_joined']
        assert not e['is_past']
    for e in past:
        assert e['is_joined']
        assert e['is_past']

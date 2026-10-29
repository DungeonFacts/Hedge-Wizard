# tests/conftest.py
import pytest
import cards
import events
from tests.fixtures import TEST_CARD_TEMPLATES,TEST_EVENT_TEMPLATES

@pytest.fixture(autouse=True)
def use_test_templates(monkeypatch):
    monkeypatch.setattr(cards, "CARD_TEMPLATES", TEST_CARD_TEMPLATES)
    monkeypatch.setattr(events, "EVENT_TEMPLATES", TEST_EVENT_TEMPLATES)

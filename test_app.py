import pytest, requests
from app import index


@pytest.fixture
def test_index():
    test = index()
    return test

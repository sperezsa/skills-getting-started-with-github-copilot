import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def activities_data(monkeypatch):
    test_activities = copy.deepcopy(app_module.activities)
    monkeypatch.setattr(app_module, "activities", test_activities)
    return test_activities


@pytest.fixture
def client(activities_data):
    with TestClient(app_module.app) as test_client:
        yield test_client

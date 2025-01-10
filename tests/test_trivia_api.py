from src.trivia_api import ConnectToApi
import pytest


class TestTriviaRetrieval:
    @pytest.fixture
    def test_instance(self):
        limit: int = 3
        category: str = "science"
        difficulty = "easy"
        test_inst = ConnectToApi(
            difficulty=difficulty, categories=category, limit=limit
        )
        return test_inst

    def test_connect_to_api(self, test_instance):
        test_json = test_instance.connect_to_api
        assert test_json

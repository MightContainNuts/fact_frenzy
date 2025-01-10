from src.trivia_api import QAStorage
import pytest


class TestTriviaRetrieval:
    @pytest.fixture
    def test_instance(self):
        limit: int = 3
        category: str = "science"
        difficulty = "easy"
        test_inst = QAStorage(
            difficulty=difficulty, categories=category, limit=limit
        )  # noqa E501
        return test_inst

    @pytest.fixture
    def test_data_from_api(self, test_instance):
        test_json = test_instance.connect_to_api
        assert test_json
        return test_instance.connect_to_api()

    @pytest.fixture()
    def test_get_random_and_remove_from_dict(
        self, test_instance, test_data_from_api
    ):  # noqa E501
        assert len(test_instance.local_storage) == 3
        test_instance.get_random_qa_and_remove_from_dict()
        assert len(test_instance.local_storage) == 2
        return test_instance.get_random_qa_and_remove_from_dict()

    def test_create_list_random_answers(
        self, test_get_random_and_remove_from_dict, test_instance
    ):
        test_qa = test_instance.create_list_random_answers(
            test_get_random_and_remove_from_dict
        )
        for key, value in test_qa.items():
            assert len(value) == 4
            assert isinstance(value, list)

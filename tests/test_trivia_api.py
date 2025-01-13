from src.trivia_api import QAStorage
import pytest


class TestTriviaRetrieval:
    @pytest.fixture
    def test_instance(self):
        with QAStorage() as test_inst:
            return test_inst

    @pytest.fixture
    def test_data_from_api(self, test_instance):
        test_json = test_instance._fetch_trivia_questions
        assert test_json
        return test_instance._fetch_trivia_questions("easy")

    @pytest.fixture()
    def test_get_random_qa(self, test_instance, test_data_from_api):
        assert len(test_instance.trivia_storage) == 3
        test_instance._get_random_qa("easy")
        assert len(test_instance.trivia_storage) == 3
        return test_instance._get_random_qa("easy")

    def test_create_list_random_answers(
        self, test_get_random_qa, test_instance
    ):
        test_answers = test_instance._create_list_random_answers(
            test_get_random_qa
        )
        assert len(test_answers) == 4
        assert isinstance(test_answers, list)

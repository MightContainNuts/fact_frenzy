from src.trivia_api import (
    QAStorage,
    QAList,
    QATuple,
    TriviaItem,
    TriviaList,
    Answers,
    CorrectAnswer,
    Category,
)
import pytest


class TestTriviaRetrieval:

    test_trivia_item: TriviaItem = {
        "category": "science",
        "id": "6244374e746187c5e7be9345",
        "correctAnswer": "Correct_Ans!",
        "incorrectAnswers": [
            "Incorrect_Ans_1",
            "Incorrect_Ans_2",
            "Incorrect_Ans_3",
        ],
        "question": {"text": "Question?"},
        "tags": ["science"],
        "type": "text_choice",
        "difficulty": "hard",
        "regions": [],
        "isNiche": False,
    }
    test_trivia_list: TriviaList = [
        {
            "category": "science",
            "id": "6244374e746187c5e7be9345",
            "correctAnswer": "Correct_Ans1!",
            "incorrectAnswers": [
                "Incorrect_Ans_1.1",
                "Incorrect_Ans_1.2",
                "Incorrect_Ans_1.3",
            ],
            "question": {"text": "Question1?"},
            "tags": ["science"],
            "type": "text_choice",
            "difficulty": "hard",
            "regions": [],
            "isNiche": False,
        },
        {
            "category": "science",
            "id": "6244374e746187c5e7be9345",
            "correctAnswer": "Correct_Ans2",
            "incorrectAnswers": [
                "Incorrect_Ans_2.1",
                "Incorrect_Ans_2.2",
                "Incorrect_Ans_2.3",
            ],
            "question": {"text": "Question2?"},
            "tags": ["science"],
            "type": "text_choice",
            "difficulty": "medium",
            "regions": [],
            "isNiche": False,
        },
        {
            "category": "science",
            "id": "6244374e746187c5e7be9345",
            "correctAnswer": "Correct_Ans3!",
            "incorrectAnswers": [
                "Incorrect_Ans_3.1",
                "Incorrect_Ans_3.2",
                "Incorrect_Ans_3.3",
            ],
            "question": {"text": "Question3?"},
            "tags": ["science"],
            "type": "text_choice",
            "difficulty": "hard",
            "regions": [],
            "isNiche": False,
        },
    ]
    test_data_storage: QAList = [
        (
            "Category1",
            "Question_1",
            [
                "Incorrect_Ans_1.1",
                "Incorrect_Ans_1.2",
                "Incorrect_Ans_1.3",
                "Correct_Ans_1",
            ],
            "Correct_Ans_1",
            1,
        ),
        (
            "Category2",
            "Question_2",
            [
                "Incorrect_Ans_2.1",
                "Incorrect_Ans_2.2",
                "Correct_Ans_2" "Incorrect_Ans_2.3",
            ],
            "Correct_Ans_2",
            2,
        ),
        (
            "Catgegory3",
            "Question_3",
            [
                "Incorrect_Ans_3.1",
                "Correct_Ans_3" "Incorrect_Ans_3.2",
                "Incorrect_Ans_3.3",
            ],
            "Correct_Ans_3",
            2,
        ),
    ]

    @pytest.fixture
    def test_instance(self):
        with QAStorage() as test_inst:
            return test_inst

    def test_trivia_dict(self, test_instance):
        test_qa_dict = test_instance._fetch_trivia_dict("easy")
        assert test_qa_dict
        assert len(test_qa_dict) == 3
        for qa in test_qa_dict:
            assert qa["difficulty"] == "easy"

    def test_parse_question(self, test_instance):
        test_question = test_instance._parse_question(self.test_trivia_item)
        assert isinstance(test_question, str)
        assert test_question == self.test_trivia_item["question"]["text"]
        assert test_question == "Question?"

    def test_parse_correct_answer(self, test_instance):
        test_correct_answer: CorrectAnswer = (
            test_instance._parse_correct_answer(self.test_trivia_item)
        )
        assert isinstance(test_correct_answer, str)
        assert test_correct_answer == self.test_trivia_item["correctAnswer"]
        assert test_correct_answer == "Correct_Ans!"

    def test_parse_incorrect_answers(self, test_instance):
        test_incorrect_answers: Answers = (
            test_instance._parse_incorrect_answers(self.test_trivia_item)
        )
        assert isinstance(test_incorrect_answers, list)
        assert len(test_incorrect_answers) == 3

    def test_parse_category(self, test_instance):
        test_category: Category = test_instance._parse_category(
            self.test_trivia_item
        )
        assert isinstance(test_category, str)
        assert test_category == "science"

    def test_create_list_random_answer(self, test_instance):
        correct_answer = test_instance._parse_correct_answer(
            self.test_trivia_item
        )
        incorrect_answers = test_instance._parse_incorrect_answers(
            self.test_trivia_item
        )
        test_list: QAList = test_instance._create_list_random_answers(
            incorrect_answers, correct_answer
        )
        assert isinstance(test_list, list)
        assert len(test_list) == 4
        expected_answers = [
            "Incorrect_Ans_1",
            "Incorrect_Ans_2",
            "Incorrect_Ans_3",
            "Correct_Ans!",
        ]
        print(f"Expected answers: {expected_answers}")
        print(f"Generated test list: {test_list}")
        assert all(answer in test_list for answer in expected_answers)
        assert test_list != [
            "Incorrect_Ans_1",
            "Incorrect_Ans_2",
            "Incorrect_Ans_3",
            "Correct_Ans!",
        ]

    def test_calculate_points_for_question(self, test_instance):
        test_points = test_instance._calculate_points_for_question(
            self.test_trivia_item
        )
        assert isinstance(test_points, int)
        assert test_points == 3

    def test_create_qa_tuple(self, test_instance):
        qa_tuple: QATuple = test_instance._create_qa_tuple(
            self.test_trivia_item
        )
        assert isinstance(qa_tuple, tuple)
        assert len(qa_tuple) == 5
        assert isinstance(qa_tuple[0], str)
        assert isinstance(qa_tuple[1], str)
        assert isinstance(qa_tuple[2], list) and all(
            isinstance(ans, str) for ans in qa_tuple[1]
        )
        assert isinstance(qa_tuple[3], str)
        assert isinstance(qa_tuple[4], int)

    def test_get_random_qa(self, test_instance):
        test_instance.qa_storage = self.test_data_storage
        assert len(test_instance.qa_storage) == 3
        test_instance._get_random_qa()
        assert len(test_instance.qa_storage) == 2

    def test_select_question_from_trivia_list(self, test_instance):
        test_instance.qa_storage = self.test_data_storage
        selected_qa: TriviaItem = (
            test_instance.select_question_from_trivia_list()
        )
        assert isinstance(selected_qa, tuple)
        assert len(selected_qa) == 5

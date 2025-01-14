import random
import requests
from src.logger import setup_logger
from typing import Tuple

Category = str
Question = str
Answers = list[str]
CorrectAnswer = str
QuestionValue = int
TriviaItem = dict[str : [str | list[str]]]  # noqa: E203
TriviaList = list[TriviaItem]
QATuple = Tuple[
    Category, Question, Answers, CorrectAnswer, QuestionValue
]  # noqa: E203
QAList = list[QATuple]  # noqa: E203# noqa: E203


class QAStorage:
    URL = "https://the-trivia-api.com/v2/questions/?"

    def __init__(
        self,
        tags: list[str] = None,
        types: str = "text",
        categories: list[str] = "None",
        limit: int = 10,
    ):
        self.tags = tags
        self.types = types
        self.categories = categories
        self.limit = limit
        self.qa_storage: QAList = []

        self.logger = setup_logger(__name__)
        self.logger.info(
            "Starting new instance of Connect to API %s %s %s %s",
            tags,
            types,
            categories,
            limit,
        )

    def __enter__(self):
        """
        using context manager
        :return:
        :rtype:
        """
        try:
            self._populate_trivia_storage()
        except Exception as e:
            self.logger.error("Error during resource initialization: %s", e)
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handle errors and cleanup resources
        """
        if exc_type is not None:
            self.logger.error("An error occurred: %s", exc_val)
        self.logger.info("Exiting context and cleaning up resources.")
        return exc_type is None

    def select_question_from_trivia_list(self) -> QATuple:
        """
        select a question from the dictionary based on difficulty
        return tuple with question, right answer and value
        :param difficulty:
        :type difficulty:
        :return:
        :rtype:
        """
        random_question = self._get_random_qa()
        return random_question if random_question else None

    def _get_random_qa(self) -> QATuple:
        """
        geta random Question and Answers from the trivia dict
        and return one. Remove the chosen one from the trivia dict
        :return:
        :rtype:
        """
        if len(self.qa_storage):
            random_question = random.choice(self.qa_storage)
            self.qa_storage.remove(random_question)
            self.logger.info("random question picked %s", random_question)
            return random_question

    # populate trivia storage - happens on class instance
    def _populate_trivia_storage(self) -> QAList:
        """
        get 3 questions of each difficulty and add them to a storage
        :return:
        :rtype:
        """

        difficulties = ["easy", "medium", "hard"]
        for difficulty in difficulties:
            trivia_temp_storage: TriviaList = self._fetch_trivia_dict(
                difficulty
            )
            self.logger.info(f"Questions added for {difficulty} class")
            for trivia_item in trivia_temp_storage:
                qa_item: QATuple = self._create_qa_tuple(trivia_item)
                self.qa_storage.append(qa_item)
        random.shuffle(self.qa_storage)
        return self.qa_storage

    def _fetch_trivia_dict(self, difficulty) -> TriviaList:
        """
        connect to api and retrieve trivia
        :return:

        :rtype:
        """
        trivia_dict: TriviaList = {}
        LIMIT = 3
        PATH = "https://the-trivia-api.com/v2/questions/?"
        difficulty = f"difficulties={difficulty}"
        categories = f"&categories={self.categories}"
        limit = f"&limit={LIMIT}"

        URL = PATH + difficulty + categories + limit
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                self.logger.info(
                    f"Connected to api, status code: {response.status_code}"
                )
                trivia_dict = response.json()
                self.logger.info("converting response to json ")
        except requests.exceptions.RequestException as e:
            self.logger.error("Exception caught by requests %s", e)
            return []
        return trivia_dict

    # create qa tuple from parsed trivia item
    def _create_qa_tuple(self, trivia_item: TriviaItem) -> QATuple:
        category: Category = self._parse_category(trivia_item)
        question: Question = self._parse_question(trivia_item)
        correct_answer: CorrectAnswer = self._parse_correct_answer(trivia_item)
        incorrect_answers: Answers = self._parse_incorrect_answers(trivia_item)
        answers: Answers = self._create_list_random_answers(
            incorrect_answers, correct_answer
        )
        question_value: QuestionValue = self._calculate_points_for_question(
            trivia_item
        )
        return category, question, answers, correct_answer, question_value

    def _parse_question(self, trivia_item: TriviaItem) -> Question:
        """
        parse question from qa dict
        :param question:
        :type question:
        :return:
        :rtype:
        """
        return trivia_item["question"]["text"]

    def _parse_correct_answer(self, trivia_item: TriviaItem) -> CorrectAnswer:
        """
        get eh correct answer for the selected question
        :param selected_question:
        :type selected_question:
        :return:
        :rtype:
        """
        self.logger.info("Correct answer for question parsed")
        return trivia_item["correctAnswer"]

    def _parse_incorrect_answers(self, trivia_item: TriviaItem) -> Answers:
        """
        parse list of false answers from trivia item
        :param trivia_item:
        :type trivia_item:
        :return:
        :rtype:
        """
        return trivia_item["incorrectAnswers"]

    def _create_list_random_answers(
        self, incorrect_answers: Answers, correct_answer: CorrectAnswer
    ) -> Answers:  # noqa E501
        """
        create a list of random placed answers based on json
        :return:
        :rtype:
        """
        incorrect_answers.append(correct_answer)
        answers = incorrect_answers
        random.shuffle(answers)
        self.logger.info("List of answers created and shuffled %s", answers)
        return answers

    def _calculate_points_for_question(
        self, trivia_item: TriviaItem
    ) -> QuestionValue:
        """
        calculater points based on difficulty
        :return:
        :rtype:
        """
        points = {
            "easy": 1,
            "medium": 2,
            "hard": 3,
        }
        difficulty = trivia_item["difficulty"]
        question_value = points[difficulty]
        self.logger.info(
            f"Points calculated for question {difficulty} : {points} %s",
            trivia_item,
        )
        return question_value

    def _parse_category(self, trivia_item: TriviaItem) -> Category:
        """
        parse category from trivia item
        :return:
        :rtype:
        """
        return trivia_item["category"]

import random
import requests
from src.logger import setup_logger

TriviaDict = dict[str : list[dict[str:str]]]  # noqa: E203
TriviaItem = dict[str : [str | list[str]]]  # noqa: E203
QADict = dict[str : list[str]]  # noqa: E203


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
        self.trivia_storage: TriviaDict = {}

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
            self._create_trivia_storage()
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

    def select_question_from_trivia_store(self, difficulty):
        """
        select a question from the dictionary based on difficulty
        return tuple with question, right answer and value
        :param difficulty:
        :type difficulty:
        :return:
        :rtype:
        """
        random_question = self._get_random_qa(difficulty)

        question = random_question["question"]["text"]

        correct_answer = self._get_correct_answer_for_selected_question(
            random_question
        )

        answers = self._create_list_random_answers(random_question)

        question_value = self._calculate_points_for_question(random_question)

        return question, answers, correct_answer, question_value

    def _create_trivia_storage(self):
        """
        get 10 questions of each difficulty and add them to a storage
        :return:
        :rtype:
        """
        difficulties = ["easy", "medium", "hard"]
        for difficulty in difficulties:
            self.trivia_storage[difficulty] = self._fetch_trivia_questions(
                difficulty
            )
            self.logger.info(f"Questions added for {difficulty} class")

    def _fetch_trivia_questions(self, difficulty) -> TriviaDict:
        """
        connect to api and retrieve trivia
        :return:
        :rtype:
        """
        question_storage = {}
        PATH = "https://the-trivia-api.com/v2/questions/?"
        difficulty = f"difficulties={difficulty}"
        categories = f"&categories={self.categories}"
        limit = f"&limit={self.limit}"

        URL = PATH + difficulty + categories + limit
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                self.logger.info(
                    f"Connected to api, status code: {response.status_code}"
                )
                question_storage = response.json()
                self.logger.info("converting response to json ")
        except requests.exceptions.RequestException as e:
            self.logger.error("Exception caught by requests %s", e)
            return []
        return question_storage

    def _create_list_random_answers(
        self, selected_question: dict
    ) -> TriviaItem:  # noqa E501
        """
        create a list of random placed answers based on json
        :return:
        :rtype:
        """
        correct_answer = selected_question["correctAnswer"]
        answers = selected_question["incorrectAnswers"]
        answers.append(correct_answer)
        random.shuffle(answers)
        self.logger.info("List of answers created and shuffled %s", answers)
        return answers

    def _get_random_qa(self, difficulty) -> QADict:
        """
        geta random Question and Answers from the trivia dict
        and return one. Remove the chosen one from the trivia dict
        :return:
        :rtype:
        """
        random_question = random.choice(self.trivia_storage[difficulty])
        self.trivia_storage[difficulty].remove(random_question)
        self.logger.info(
            f"random question picked based on {difficulty} %s", random_question
        )
        return random_question

    def _calculate_points_for_question(self, selected_question) -> int:
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
        difficulty = selected_question["difficulty"]
        question_value = points[difficulty]
        self.logger.info(
            f"Points calculated for question {difficulty} : {points} %s",
            selected_question,
        )
        return question_value

    def _get_correct_answer_for_selected_question(
        self, selected_question
    ) -> str:
        """
        get eh correct answer for the selected question
        :param selected_question:
        :type selected_question:
        :return:
        :rtype:
        """
        self.logger.info("Correct answer for question parsed")
        return selected_question["correctAnswer"]

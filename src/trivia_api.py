import random
import requests
from src.logger import setup_logger

TriviaDict = list[dict[str:str]]
TriviaItem = dict[str : [str | list[str]]]  # noqa: E203
QADict = dict[str : list[str]]  # noqa: E203


class QAStorage:
    URL = "https://the-trivia-api.com/v2/questions/?"

    def __init__(
        self,
        difficulty: str = "easy",
        tags: list[str] = None,
        types: str = "text",
        categories: list[str] = "None",
        limit: int = 20,
    ):
        self.difficulty = difficulty
        self.tags = tags
        self.types = types
        self.categories = categories
        self.limit = limit
        self.local_storage: TriviaDict = {}

        self.logger = setup_logger(__name__)
        self.logger.info(
            "Starting new instance of Connect to API %s %s %s %s %s",
            difficulty,
            tags,
            types,
            categories,
            limit,
        )

    def connect_to_api(self) -> TriviaDict:
        """
        connect to api and retrieve trivia
        :return:
        :rtype:
        """
        PATH = "https://the-trivia-api.com/v2/questions/?"
        difficulty = f"difficulties={self.difficulty}"
        categories = f"&categories={self.categories}"
        limit = f"&limit={self.limit}"

        URL = PATH + difficulty + categories + limit
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                self.logger.info(
                    f"Connected to api, status code: {response.status_code}"
                )
                self.local_storage = response.json()
                self.logger.info("converting response to json ")
        except requests.exceptions.RequestException as e:
            self.logger.error("Exception caught by requests %s", e)
            return []
        return self.local_storage

    def create_list_random_answers(
        self, selected_question: dict
    ) -> TriviaItem:  # noqa E501
        """
        create a list of random placed answers based on json
        :return:
        :rtype:
        """
        question = selected_question["question"]["text"]
        correct_answer = selected_question["correctAnswer"]
        answers = selected_question["incorrectAnswers"]
        answers.append(correct_answer)
        random.shuffle(answers)
        qa_dict = {question: answers}
        return qa_dict

    def get_random_qa_and_remove_from_dict(self) -> QADict:
        """
        geta random Question and Answers from the trivia dict
        and return one. Remove the chosen one from the trivia dict
        :return:
        :rtype:
        """
        random_question = random.choice(self.local_storage)
        self.local_storage.remove(random_question)
        return random_question

import requests
from src.logger import setup_logger

TriviaDict = list[dict[str:str]]


class ConnectToApi:
    URL = "https://the-trivia-api.com/v2/questions/?"

    def __init__(
        self,
        difficulty: str = "easy",
        tags: list[str] = None,
        types: str = "text",
        categories: list[str] = "None",
        limit: int = 50,
    ):
        self.difficulty = difficulty
        self.tags = tags
        self.types = types
        self.categories = categories
        self.limit = limit

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
        trivia_data_json = {}
        PATH = "https://the-trivia-api.com/v2/questions/?"
        difficulty = f"difficulties={self.difficulty}&"
        categories = f"categories={self.categories}"
        URL = PATH + difficulty + categories
        try:
            response = requests.get(URL)

            if response.status_code == 200:
                self.logger.info(
                    f"Connected to api, status code: {response.status_code}"
                )
                trivia_data_json = response.json()
                self.logger.info("converting response to json ")
        except requests.exceptions.RequestException as e:
            self.logger.error("Exception caught by requests %s", e)
            return []
        return trivia_data_json


if __name__ == "__main__":
    app = ConnectToApi()
    app.connect_to_api()

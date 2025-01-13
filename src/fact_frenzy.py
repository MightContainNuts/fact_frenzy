from src.trivia_api import QAStorage
from src.utils import Utils
from logger import setup_logger


class FactFrenzy:
    def __init__(self, qa_storage: QAStorage):
        self.qa_storage = qa_storage
        self.logger = setup_logger(__name__)
        self.logger.info("starting fact frenzy initialisation")

    def run(self):
        selected_question = self.qa_storage.select_question_from_trivia_store(
            "easy"
        )
        self.logger.info(
            "getting a question item from trivia storage %s", selected_question
        )

        Utils.print_question(selected_question)


if __name__ == "__main__":
    with QAStorage() as app:
        start = FactFrenzy(app)
        start.run()

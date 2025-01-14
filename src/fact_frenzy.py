from src.trivia_api import QAStorage, QAList
from src.utils import Utils
from logger import setup_logger


class FactFrenzy:
    def __init__(self, qas_instance: QAStorage):
        self.qas_instance: QAStorage = qas_instance
        self.qa_list: QAList = qas_instance.qa_storage
        self.qa_item = qas_instance.select_question_from_trivia_list()
        self.logger = setup_logger(__name__)
        self.logger.info("starting fact frenzy initialisation")

    def run(self):
        Utils.print_qa_storage(self.qa_list)

        for item in range(len(self.qa_list) + 1):
            question = self.qas_instance.select_question_from_trivia_list()
            if question:
                print("\n")
                Utils.print_question(question)
            else:
                print("QA List is empty")


if __name__ == "__main__":
    with QAStorage() as app:
        start = FactFrenzy(app)
        start.run()

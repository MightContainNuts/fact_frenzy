from src.trivia_api import QAStorage
from src.utils import Utils


class FactFrenzy:
    def __init__(self, qa_storage: QAStorage):
        self.qa_storage = qa_storage
        self.qa_storage.connect_to_api()

    def run(self):
        selected_question = (
            self.qa_storage.get_random_qa_and_remove_from_dict()
        )  # noqa E501
        correct_answer = selected_question["correctAnswer"]
        qa_list = self.qa_storage.create_list_random_answers(selected_question)
        Utils.print_question(qa_list, correct_answer)


if __name__ == "__main__":
    app = QAStorage()
    start = FactFrenzy(app)
    start.run()

from src.trivia_api import QAList, QATuple
from src.logger import setup_logger

logger = setup_logger(__name__)


class Utils:
    @staticmethod
    def print_question(qa_item: QATuple) -> None:
        """
        print out question and answer
        :param selected_question:
        :type selected_question:
        :return:
        :rtype:
        """
        question, answers, correct_answer, question_value = qa_item
        print(question)
        for idx, answer in enumerate(answers, start=1):
            print(f"{idx}: {answer}")
        print(f"{correct_answer=}, {question_value=}")
        logger.info("QATuple printed %s", qa_item)

    staticmethod

    def print_qa_storage(qa_list: QAList):
        """
        for debugging purposes
        print storage
        :return:
        :rtype:
        """
        for idx, qa_item in enumerate(qa_list, start=1):
            print(f"\nQuestion Nr: {idx}")
            print("-" * 10)
            Utils.print_question(qa_item)

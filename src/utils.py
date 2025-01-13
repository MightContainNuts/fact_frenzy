class Utils:
    @staticmethod
    def print_question(selected_question) -> None:
        """
        print out question and answer
        :param selected_question:
        :type selected_question:
        :return:
        :rtype:
        """
        question, answers, correct_answer, question_value = selected_question
        print(question)
        for idx, answer in enumerate(answers, start=1):
            print(f"{idx}: {answer}")
        print(f"{correct_answer=}, {question_value=}")

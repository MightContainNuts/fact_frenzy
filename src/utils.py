class Utils:
    @staticmethod
    def print_question(selected_question, correct_answer) -> None:
        """
        print out question and answer
        :param selected_question:
        :type selected_question:
        :return:
        :rtype:
        """
        for question, answers in selected_question.items():
            print(question)
            for idx, answer in enumerate(answers, start=1):
                print(f"{idx}: {answer}")
            print(f"{correct_answer=}")

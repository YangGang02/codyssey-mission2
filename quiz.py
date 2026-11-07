class Quiz:
    def __init__(self, question, choices, answer, hint=None):  # 문제 한 개의 정보 저장
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def show(self):  # 문제와 선택지 출력
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def is_correct(self, guess):  # 입력 번호와 정답 비교
        return guess == self.answer

from storage import load_state, save_state
from quiz import Quiz


def read_number(prompt, minimum, maximum):
    while True:
        text = input(prompt).strip()
        if not text:
            print("값을 입력해 주세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("숫자를 입력해 주세요.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"{minimum}~{maximum} 사이의 숫자를 입력해 주세요.")


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value

        print("빈 값은 입력할 수 없습니다.")


class QuizGame:
    def __init__(self):
        self.quizzes, self.best_score = load_state()

    def show_menu(self):
        print("\n=== Python 기초 퀴즈 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수")
        print("5. 종료")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct = 0
        total = len(self.quizzes)

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {number}/{total}]")
            quiz.show()
            guess = read_number("정답 번호: ", 1, 4)

            if quiz.is_correct(guess):
                correct += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(correct / total * 100)
        print(f"\n결과: {total}문제 중 {correct}문제 정답 ({score}점)")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            save_state(self.quizzes, self.best_score)
            print("새로운 최고 점수입니다!")

    def add_quiz(self):
        question = read_text("문제: ")
        choices = []

        for number in range(1, 5):
            choice = read_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = read_number("정답 번호: ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if save_state(self.quizzes, self.best_score):
            print("퀴즈를 추가하고 저장했습니다.")
        else:
            print("퀴즈를 추가했지만 이번 실행에서만 볼 수 있습니다.")

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def show_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"최고 점수: {self.best_score}점")

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 5)

                if choice == 5:
                    save_state(self.quizzes, self.best_score)
                    print("게임을 종료합니다.")
                    break
                elif choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()

        except (KeyboardInterrupt, EOFError):
            save_state(self.quizzes, self.best_score)
            print("\n입력이 중단되어 게임을 종료합니다.")
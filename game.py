import random
from datetime import datetime

from storage import load_state, save_state
from quiz import Quiz


HINT_PENALTY = 10


def parse_number(text, minimum, maximum):
    if not text:
        print("값을 입력해 주세요.")
        return None

    try:
        number = int(text)
    except ValueError:
        print("숫자를 입력해 주세요.")
        return None

    if minimum <= number <= maximum:
        return number

    print(f"{minimum}~{maximum} 사이의 숫자를 입력해 주세요.")
    return None


def read_number(prompt, minimum, maximum):
    while True:
        number = parse_number(input(prompt).strip(), minimum, maximum)
        if number is not None:
            return number


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value

        print("빈 값은 입력할 수 없습니다.")


class QuizGame:
    def __init__(self):
        self.quizzes, self.best_score, self.history = load_state()

    def show_menu(self):
        print("\n=== Python 기초 퀴즈 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수")
        print("5. 종료")
        print("6. 퀴즈 삭제")
        print("7. 점수 기록")

    def read_answer(self, quiz):
        used_hint = False
        while True:
            text = input("정답 번호 (힌트: h): ").strip()
            if text.lower() == "h":
                if not quiz.hint:
                    print("등록된 힌트가 없습니다.")
                    continue
                print(f"힌트: {quiz.hint}")
                if not used_hint:
                    print(f"힌트를 사용해 최종 점수에서 {HINT_PENALTY}점을 뺍니다.")
                    used_hint = True
                continue

            answer = parse_number(text, 1, len(quiz.choices))
            if answer is not None:
                return answer, used_hint

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        total = read_number(f"몇 문제를 풀까요? (1~{len(self.quizzes)}): ", 1, len(self.quizzes))
        selected = random.sample(self.quizzes, total)
        correct = 0
        hints_used = 0

        for number, quiz in enumerate(selected, start=1):
            print(f"\n[문제 {number}/{total}]")
            quiz.show()
            guess, used_hint = self.read_answer(quiz)
            if used_hint:
                hints_used += 1

            if quiz.is_correct(guess):
                correct += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        score = max(0, round(correct / total * 100) - hints_used * HINT_PENALTY)
        print(f"\n결과: {total}문제 중 {correct}문제 정답 ({score}점)")
        if hints_used:
            print(f"힌트 사용: {hints_used}문제")

        self.history.append({
            "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "total": total,
            "correct": correct,
            "hints_used": hints_used,
            "score": score,
        })

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
        save_state(self.quizzes, self.best_score, self.history)

    def add_quiz(self):
        question = read_text("문제: ")
        choices = []

        for number in range(1, 5):
            choice = read_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = read_number("정답 번호: ", 1, 4)
        hint = input("힌트 (생략하려면 Enter): ").strip() or None
        self.quizzes.append(Quiz(question, choices, answer, hint))
        if save_state(self.quizzes, self.best_score, self.history):
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

    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        choice = read_number("삭제할 번호 (0: 취소): ", 0, len(self.quizzes))
        if choice == 0:
            print("삭제를 취소했습니다.")
            return

        index = choice - 1
        question = self.quizzes[index].question
        remaining = self.quizzes[:index] + self.quizzes[index + 1:]
        if save_state(remaining, self.best_score, self.history):
            self.quizzes = remaining
            print(f"퀴즈를 삭제했습니다: {question}")

    def show_history(self):
        if not self.history:
            print("저장된 점수 기록이 없습니다.")
            return

        print("\n=== 점수 기록 (최근 순) ===")
        for record in reversed(self.history):
            played_at = record["played_at"].replace("T", " ")
            print(
                f"{played_at} | {record['total']}문제 | "
                f"정답 {record['correct']}개 | {record['score']}점"
            )

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 7)

                if choice == 5:
                    save_state(self.quizzes, self.best_score, self.history)
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
                elif choice == 6:
                    self.delete_quiz()
                elif choice == 7:
                    self.show_history()

        except (KeyboardInterrupt, EOFError):
            save_state(self.quizzes, self.best_score, self.history)
            print("\n입력이 중단되어 게임을 종료합니다.")

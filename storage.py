import json
from pathlib import Path

from questions import default_quizzes
from quiz import Quiz


STATE_PATH = Path(__file__).resolve().parent / "state.json"


def quiz_from_data(item):
    question = item["question"]
    choices = item["choices"]
    answer = item["answer"]

    if not isinstance(question, str) or not question.strip():
        raise ValueError("문제는 빈 문자열일 수 없습니다.")
    if not isinstance(choices, list) or len(choices) != 4:
        raise ValueError("선택지가 네 개여야 합니다.")
    for choice in choices:
        if not isinstance(choice, str) or not choice.strip():
            raise ValueError("선택지는 빈 문자열일 수 없습니다.")
    if type(answer) is not int or not 1 <= answer <= 4:
        raise ValueError("정답 번호는 1~4여야 합니다.")

    return Quiz(question, choices, answer)


def load_state():
    try:
        with STATE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)

        items = data["quizzes"]
        best_score = data["best_score"]
        if not isinstance(items, list):
            raise ValueError("퀴즈 목록이 올바르지 않습니다.")
        if best_score is not None:
            if type(best_score) is not int or not 0 <= best_score <= 100:
                raise ValueError("최고 점수가 올바르지 않습니다.")

        quizzes = [quiz_from_data(item) for item in items]
        print(f"저장된 퀴즈 {len(quizzes)}개를 불러왔습니다.")
        return quizzes, best_score

    except FileNotFoundError:
        return default_quizzes(), None
    except (OSError, ValueError, KeyError, TypeError):
        print("저장 파일을 읽을 수 없어 기본 문제로 시작합니다.")
        return default_quizzes(), None


def save_state(quizzes, best_score):
    data = {
        "quizzes": [
            {
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer,
            }
            for quiz in quizzes
        ],
        "best_score": best_score,
    }

    temp_path = STATE_PATH.with_suffix(".json.tmp")
    try:
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        temp_path.replace(STATE_PATH)
        return True
    except OSError:
        print("저장에 실패했습니다. 파일 경로와 쓰기 권한을 확인해 주세요.")
        return False
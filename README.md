# Python 기초 퀴즈

터미널에서 객관식 문제를 풀고, 새 문제를 추가할 수 있는 Python 퀴즈 게임입니다. 이번 미션에서 배운 자료형과 반복문 같은 기본 문법을 복습하기 위해 Python 기초를 주제로 골랐습니다.

## 실행 방법

Python 3.10 이상이 필요합니다. 프로젝트 폴더에서 다음 명령을 실행합니다.

```bash
python3 main.py
```

## 기능

- **퀴즈 풀기** — 기본 문제 5개와 추가한 문제를 풀고, 정답 여부와 최종 점수를 확인합니다.
- **퀴즈 추가** — 문제, 선택지 4개, 정답 번호를 입력해 저장합니다.
- **퀴즈 목록** — 등록된 문제를 확인합니다.
- **최고 점수** — 지금까지 받은 가장 높은 점수를 확인합니다.
- **종료** — 게임을 종료합니다.

## 파일 구조

```text
main.py       게임 실행
game.py       메뉴, 퀴즈 풀이, 문제 추가, 목록과 점수 관리
quiz.py       개별 문제를 표현하는 Quiz 클래스
questions.py  기본 문제 5개
storage.py    데이터 저장과 불러오기
state.json    게임이 실행 중에 생성하는 저장 파일
state.json.bak  마지막 정상 저장본의 자동 백업
```

## 코드 설계

- `Quiz`는 문제 하나의 질문·선택지·정답을 보관하고, 문제 출력과 채점을 맡습니다. `QuizGame`은 문제 목록과 최고 점수를 보관하고 메뉴와 게임 진행을 맡습니다.
- 클래스로 관련 데이터와 동작을 묶으면 문제마다 값을 따로 전달할 필요가 줄어듭니다. 상태가 없는 입력 검사에는 `read_number()`와 `read_text()` 같은 함수가 더 간단합니다. 화면에서 받은 입력은 `game.py`에서 검사하고, 파일에서 읽은 값의 구조 검사와 저장은 `storage.py`에서 처리합니다.
- 메뉴를 바꾸려면 `QuizGame.show_menu()`와 `run()`을, 점수 계산을 바꾸려면 `play()`를 수정합니다. 문제 형식을 바꾸면 `Quiz`와 `storage.py`의 읽기·쓰기 형식도 함께 확인해야 합니다.

## 데이터 저장

프로젝트 폴더의 `state.json`에 UTF-8로 저장합니다. `quizzes`에는 문제(`question`), 선택지(`choices`), 정답 번호(`answer`)가 들어갑니다. `best_score`는 최고 점수이며, 아직 기록이 없으면 `null`입니다. 다시 실행할 때는 저장된 문제와 점수를 불러옵니다.

`quizzes`는 문제 순서를 유지하기 위해 목록으로 저장하고, 각 문제의 질문·선택지·정답은 한 객체에 묶었습니다. `answer`는 화면과 같은 1~4번을 사용합니다. 전체 게임의 최고 점수인 `best_score`는 문제 목록과 나란히 둡니다.

실행 시 JSON을 읽고 필드와 값의 범위를 검사합니다. `state.json`이 없거나 손상됐으면 `state.json.bak`에서 문제와 최고 점수를 복구합니다. 두 파일 모두 사용할 수 없으면 기본 문제로 시작합니다. 문제 추가, 최고 점수 갱신, 종료 시에는 임시 파일을 완성한 뒤 `state.json`을 교체합니다. 정상 저장 후 같은 내용을 `state.json.bak`에 자동으로 백업합니다.

JSON은 표준 라이브러리로 읽고 쓰기 쉽고 파일을 직접 확인할 수 있어 이 정도 규모에 적합합니다. 이 프로그램은 저장할 때 전체 파일을 다시 쓰고 읽을 때 전체 데이터를 메모리에 올립니다. 문제 수가 많아지거나 여러 사용자가 동시에 쓰는 경우에는 일부 데이터만 조회·수정할 수 있는 SQLite 같은 데이터베이스가 더 적합합니다.

저장에 실패하면 경로와 쓰기 권한을 확인합니다. 프로그램이 열려 있으면 메뉴 5번으로 종료하면서 저장을 다시 시도할 수 있습니다. 백업으로 실행한 뒤 5번으로 종료하면 복구한 내용이 `state.json`에 다시 저장됩니다.

저장 파일이 손상됐을 때의 백업 복구 출력입니다.

```text
state.json 파일을 읽을 수 없습니다.
백업에서 퀴즈 6개를 복구했습니다.
최고 점수: 100점
```

## 실행 결과

기본 문제 5개에 새 문제를 추가해 플레이하고 다시 실행한 예시입니다.

```text
=== Python 기초 퀴즈 ===
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 최고 점수
5. 종료

[문제 추가] 퀴즈를 추가하고 저장했습니다.
[풀이 결과] 결과: 6문제 중 6문제 정답 (100점)
[재실행] 저장된 퀴즈 6개를 불러왔습니다.
[목록] 6. 파이썬의 확장자명은?
[점수] 최고 점수: 100점
[잘못된 입력] 숫자를 입력해 주세요. / 1~5 사이의 숫자를 입력해 주세요. / 값을 입력해 주세요.
[Ctrl+C] 입력이 중단되어 게임을 종료합니다.
```

## 실행 화면

- [개발 환경](docs/screenshots/environment.png)
- [퀴즈 추가](docs/screenshots/add_quiz.png)
- [퀴즈 풀이 결과](docs/screenshots/play.png)
- [재실행 후 퀴즈 목록](docs/screenshots/list.png)
- [재실행 후 최고 점수](docs/screenshots/score.png)
- [Ctrl+C 입력으로 종료](docs/screenshots/ctrl-c.png)
- [잘못된 입력 처리](docs/screenshots/invalid-input.png)
- [저장소 복제 및 푸시](docs/screenshots/clone.png)
- [Git 커밋 및 병합 기록](docs/screenshots/git-log.png)

## Git 작업 기록

원격 저장소는 [codyssey-mission2](https://github.com/YangGang02/codyssey-mission2)입니다. 메뉴, 문제 클래스, 풀이, 추가, 점수, 저장 기능은 각각 별도 커밋으로 기록되어 있습니다. 퀴즈 풀기는 `git checkout -b feature/quiz-play`로 분리한 뒤 `git merge --no-ff feature/quiz-play`로 `main`에 병합했습니다.

복제본(`git clone`)에서 README를 수정한 커밋 `0aca034`는 원격에 푸시한 뒤 원본 폴더에 `git pull --ff-only`로 반영했습니다.

```text
$ git rev-list --count main
16

$ git branch --list
  feature/quiz-play
* main

$ git log --oneline --graph --all
...
* 77d836b 퀴즈 추가와 입력 검사 구현
*   7335423 Merge: 퀴즈 풀이 기능 병합
|\
| * 5bad3f9 퀴즈 출제와 정오답 및 결과 표시 구현
|/
* be0c7e5 게임 진행을 QuizGame 클래스로 분리
```

커밋 수는 `f9dd815` 시점 기준이며, 그래프는 병합 구간의 발췌입니다.

## 보너스 과제

### 1. 랜덤 출제

`random.sample()`은 전체 목록에서 선택한 수만큼 문제를 중복 없이 뽑습니다. 뽑힌 순서대로 출제합니다.

```python
selected = random.sample(self.quizzes, total)
```

### 2. 문제 수 선택

1번을 선택하면 1부터 등록된 문제 수까지 입력할 수 있습니다. 예를 들어 `2`를 입력하면 두 문제를 출제합니다.

```python
total = read_number(f"몇 문제를 풀까요? (1~{len(self.quizzes)}): ", 1, len(self.quizzes))
```

### 3. 힌트 기능

각 `Quiz`는 선택 사항인 `hint`를 가집니다. 풀이 중 `h`를 누르면 힌트를 표시하고, 힌트를 본 문제마다 10점을 차감합니다. 같은 문제에서 힌트를 여러 번 열어도 한 번만 차감합니다.

```python
score = max(0, round(correct / total * 100) - hints_used * HINT_PENALTY)
```

두 문제를 모두 맞히고 그중 한 문제에서 힌트를 사용한 경우의 출력입니다.

```text
결과: 2문제 중 2문제 정답 (90점)
힌트 사용: 1문제
```

### 4. 퀴즈 삭제

6번에서 삭제할 번호를 선택합니다. `0`을 입력하면 취소합니다. 삭제한 문제를 제외한 목록을 저장합니다. 다음 실행부터는 이 목록을 불러옵니다.

```python
remaining = self.quizzes[:index] + self.quizzes[index + 1:]
if save_state(remaining, self.best_score, self.history):
    self.quizzes = remaining
```

### 5. 점수 기록 히스토리

게임을 끝낼 때마다 날짜·시간, 문제 수, 정답 수, 힌트 사용 수, 점수를 `state.json`의 `history`에 저장합니다. 7번은 저장된 기록을 최근 순서대로 표시합니다.

```python
self.history.append({
    "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    "total": total,
    "correct": correct,
    "hints_used": hints_used,
    "score": score,
})
```

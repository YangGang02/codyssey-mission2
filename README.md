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
```

## 데이터 저장

프로젝트 폴더의 `state.json`에 UTF-8로 저장합니다. `quizzes`에는 문제(`question`), 선택지(`choices`), 정답 번호(`answer`)가 들어갑니다. `best_score`는 최고 점수이며, 아직 기록이 없으면 `null`입니다. 저장 파일이 없으면 기본 문제로 시작하고, 다시 실행할 때는 저장된 문제와 점수를 불러옵니다.

## 실행 화면

- [개발 환경](docs/screenshots/environment.png)
- [퀴즈 추가](docs/screenshots/add_quiz.png)
- [퀴즈 풀이 결과](docs/screenshots/play.png)
- [재실행 후 퀴즈 목록](docs/screenshots/list.png)
- [재실행 후 최고 점수](docs/screenshots/score.png)
- [Git 커밋 및 병합 기록](docs/screenshots/git-log.png)
#!/bin/bash

# 1. requirements.txt에 있는 Python 패키지 중 설치되지 않은 것이 있다면 설치
pip install pipenv
pipenv install -r requirements.txt

# 2. 현재 실행 중인 check.py 프로세스 종료
pkill -f check.py

# 3. tmux 세션 선언 및 생성
SESSION_NAME="mysession"
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
  tmux new-session -d -s $SESSION_NAME
fi

# 4. tmux 세션에서 check.py 실행
tmux send-keys -t $SESSION_NAME 'pipenv run python3 check.py' C-m
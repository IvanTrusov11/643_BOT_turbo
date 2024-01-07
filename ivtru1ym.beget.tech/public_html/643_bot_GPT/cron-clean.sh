#!/bin/bash

# Получаем список PID всех запущенных процессов 643_bot.py с временем их запуска
PIDS=$(ps -eo pid,stime,cmd | grep '[p]ython3 .*643_bot.py' | awk '{print $1}')

# Находим PID самого последнего запущенного процесса
LATEST_PID=$(echo "$PIDS" | tail -n1)

# Убиваем все процессы, кроме самого последнего
for PID in $PIDS; do
    if [ "$PID" != "$LATEST_PID" ]; then
        echo "Убиваем процесс с PID $PID"
        kill -9 $PID
    fi
done

#!/bin/bash

# Загрузка переменных окружения из .env файла
export $(grep -v '^#' .env | xargs)

# Функция для отправки уведомлений (можно заменить на отправку сообщений в Slack, электронную почту и т.д.)
send_error_notification() {
    local message=$1
    echo "$message"
    # Пример отправки уведомления на электронную почту (можно заменить на ваш метод уведомлений)
    # echo "$message" | mail -s "Deployment Error" your-email@example.com
}

# Подключение к серверу и выполнение команд
ssh -p "$REMOTE_PORT" "$REMOTE_SERVER" << EOF
  set -e  # Прекращает выполнение скрипта при любой ошибке

  # Проверка наличия директории и её создание при необходимости
  if [ ! -d "$REMOTE_DIR" ]; then
    echo "Directory $REMOTE_DIR does not exist. Creating now."
    mkdir -p "$REMOTE_DIR"
    cd "$REMOTE_DIR"
    echo "Cloning repository from $REPO_URL."
    git clone "$REPO_URL" .
  else
    echo "Directory $REMOTE_DIR already exists."
    cd "$REMOTE_DIR"
    echo "Updating repository."
    git pull
  fi

  # Остановка и удаление контейнеров
  echo "Stopping and removing Docker containers."
  docker compose down || { echo "Failed to stop and remove containers"; exit 1; }

  # Выполнение docker-compose build и up
  echo "Building and starting Docker containers."
  docker compose up -d --build || { echo "Failed to build and start containers"; exit 1; }

  # Выполнение миграций
  echo "Applying database migrations."
  docker exec -it my_helper pdm run alembic upgrade heads || { echo "Failed to apply migrations"; exit 1; }
EOF

# Проверка последнего кода завершения SSH команды
if [ $? -ne 0 ]; then
    send_error_notification "Deployment failed on server $REMOTE_SERVER. Please check the server logs for details."
fi


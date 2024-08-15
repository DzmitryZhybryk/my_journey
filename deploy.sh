!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)

send_error_notification() {
    local message=$1
    echo "$message"
    # Пример отправки уведомления на электронную почту (замените на ваш метод уведомлений)
    # echo "$message" | mail -s "Deployment Error" your-email@example.com
}

set -e

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

echo "Stopping and removing Docker containers."
docker compose down || { echo "Failed to stop and remove containers"; exit 1; }

echo "Building and starting Docker containers."
docker compose up -d --build || { echo "Failed to build and start containers"; exit 1; }

echo "Waiting for containers to start..."
# sleep 10  # Вы можете увеличить или уменьшить время ожидания, если нужно

# Проверка состояния контейнеров
echo "Checking if containers are up and running..."
if ! docker compose ps | grep -q 'Up'; then
    echo "Containers are not up. Exiting."
    exit 1
fi

echo "Applying database migrations."
docker exec -i my_helper pdm run alembic upgrade heads || { echo "Failed to apply migrations"; exit 1; }

if [ $? -ne 0 ]; then
    send_error_notification "Deployment failed. Please check the logs for details."
fi
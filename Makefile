BOT_DIR = ./src
DOCKER_COMPOSE_FILE = ./docker-compose.yaml

build:
	docker-compose -f $(DOCKER_COMPOSE_FILE) build

up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

logs:
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f

clean:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down --volumes --rmi all

backup_all:
	docker exec postgres_backup ./create_backup_all.sh

backup_data:
	docker exec postgres_backup ./backup_only_data.sh

backup_schema:
	docker exec postgres_backup ./backup_only_schema.sh

restore:
	./backup/restore_db.sh

rebuild: down build up

reup: down up

help:
	@echo "Доступные цели:"
	@echo "  build       - Собрать Docker контейнеры"
	@echo "  up          - Запустить Docker контейнеры в фоновом режиме"
	@echo "  down        - Остановить и удалить Docker контейнеры"
	@echo "  logs        - Просмотреть логи Docker контейнеров в реальном времени"
	@echo "  clean       - Полное удаление контейнеров, образов и томов (осторожно!)"
	@echo "  backup_all  - Создать полную резервную копию БД (данные + схема)"
	@echo "  backup_data - Создать резервную копию только данных"
	@echo "  backup_schema - Создать резервную копию только схемы БД"
	@echo "  restore     - Восстановить БД из резервной копии"
	@echo "  rebuild     - Пересобрать и перезапустить Docker контейнеры (down → build → up)"
	@echo "  reup        - Быстрый перезапуск контейнеров (down → up)"

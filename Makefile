# Makefile for Data Engineering Workshop
# Convenience commands for managing the environment

.PHONY: help setup start stop restart status logs clean

help:
	@echo "Data Engineering Workshop - Available Commands"
	@echo ""
	@echo "  make setup    - Initial setup (create .env, directories)"
	@echo "  make start    - Start all services"
	@echo "  make stop     - Stop all services (data preserved)"
	@echo "  make restart  - Restart all services"
	@echo "  make status   - Show service status and health"
	@echo "  make logs     - Show logs (use SERVICE=name for specific)"
	@echo "  make clean    - Remove all containers and volumes ⚠️"
	@echo "  make ps       - Show running containers"
	@echo "  make build    - Rebuild all images"
	@echo ""

setup:
	@./scripts/setup.sh

start:
	@./scripts/start.sh

stop:
	@./scripts/stop.sh

restart: stop start

status:
	@./scripts/status.sh

logs:
ifdef SERVICE
	@docker-compose logs -f $(SERVICE)
else
	@docker-compose logs -f
endif

clean:
	@./scripts/clean.sh

ps:
	@docker-compose ps

build:
	@docker-compose build --no-cache

# Service-specific commands
mysql-shell:
	@docker-compose exec mysql mysql -u$(MYSQL_USER) -p$(MYSQL_PASSWORD) $(MYSQL_DATABASE)

redis-cli:
	@docker-compose exec redis redis-cli

spark-shell:
	@docker-compose exec spark-master spark-shell

# Backup and restore
backup-mysql:
	@mkdir -p backups
	@docker-compose exec mysql mysqldump -u$(MYSQL_USER) -p$(MYSQL_PASSWORD) $(MYSQL_DATABASE) > backups/beer_db_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backups/"

# Development
dev-start:
	@docker-compose up

dev-build:
	@docker-compose up --build


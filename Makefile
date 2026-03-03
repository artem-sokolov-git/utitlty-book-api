.PHONY: $(MAKECMDGOALS)

RED=\033[31m
GREEN=\033[32m
YELLOW=\033[33m
CYAN=\033[36m
RESET=\033[0m

COMPOSE_FILES=--env-file .env -f docker/storages.yaml -f docker/apps.yaml
EXEC=docker compose $(COMPOSE_FILES) exec -it api

# DOCKER
run: ## Start container in detached mode (rebuild image)
	@echo "$(CYAN)>>> Starting containers...$(RESET)"
	@docker compose $(COMPOSE_FILES) up -d pg api --build

down: ## Stop and remove container
	@echo "$(YELLOW)>>> Stopping containers...$(RESET)"
	@docker compose $(COMPOSE_FILES) down
	@echo "$(GREEN)[✓] Containers stopped$(RESET)"

clear: ## Stop container and remove all volumes
	@echo "$(RED)>>> Clearing volumes...$(RESET)"
	@docker compose $(COMPOSE_FILES) down -v
	@echo "$(GREEN)[✓] Volumes cleared$(RESET)"

logs: ## Show container logs
	@docker compose $(COMPOSE_FILES) logs -f

# CHECKS
check: ## Ruff lint and format check
	@uv run ruff check .
	@uv run ruff format --check .

tests: ## Run tests (spins up test database)
	@echo "$(CYAN)>>> Running tests...$(RESET)"
	@docker compose -f docker/tests.yaml up pg-test -d --wait
	@uv run pytest
	@docker compose -f docker/tests.yaml down
	@echo "$(GREEN)[✓] Tests passed$(RESET)"

## DJANGO COMMANDS
migrations: ## Make database migrations
	@uv run python -W ignore::RuntimeWarning manage.py makemigrations

migrate: ## Apply database migrations
	@$(EXEC) python manage.py migrate

superuser: ## Create superuser
	@$(EXEC) python manage.py create_superuser

shell: ## Open shell
	@$(EXEC) python manage.py shell

## POSTGRES
import-sql: ## Import SQL file into pg (usage: make import-sql file=data/gas_insert.sql)
	@docker exec -i pg sh -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB' < $(file)
	@echo "$(GREEN)[✓] Done$(RESET)"

## DEVELOPMENT
rebuild: ## Dev rebuild project
	@$(MAKE) clear
	@$(MAKE) migrations
	@$(MAKE) run
	@$(MAKE) migrate
	@$(MAKE) superuser
	@$(MAKE) import-sql file="data/gas_insert.sql"
	@$(MAKE) import-sql file="data/elect_insert.sql"

.DEFAULT_GOAL := help

help: ## Show available commands
	@echo "$(GREEN)============================================================================================$(RESET)"
	@echo "$(GREEN)>>> List of commands:$(RESET)"
	@echo "$(GREEN)============================================================================================$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo "$(GREEN)============================================================================================$(RESET)"

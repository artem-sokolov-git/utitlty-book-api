.PHONY: $(MAKECMDGOALS)

RED=\033[31m
GREEN=\033[32m
YELLOW=\033[33m
CYAN=\033[36m
RESET=\033[0m

COMPOSE_FILES=--env-file .env -f docker/storages.yaml -f docker/apps.yaml
WEB_EXEC=docker compose $(COMPOSE_FILES) exec -it web

run: ## Start container in detached mode (rebuild image)
	@echo "$(CYAN)>>> Starting containers...$(RESET)"
	@docker compose $(COMPOSE_FILES) up pg web --build

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

check: ## Pre-commit check
	@git add .
	@uv run pre-commit run --all-files

tests: ## Run tests (spins up test database)
	@echo "$(CYAN)>>> Running tests...$(RESET)"
	@docker compose -f docker/tests.yaml up pg-test -d --wait
	@uv run pytest
	@docker compose -f docker/tests.yaml down
	@echo "$(GREEN)[✓] Tests passed$(RESET)"

full-check: ## Make full-check with tests
	@$(MAKE) check
	@$(MAKE) tests

## DJANGO COMMANDS

migrate: ## Apply database migrations
	@$(WEB_EXEC) python manage.py migrate

superuser: ## Create superuser
	@$(WEB_EXEC) python manage.py createsuperuser

.DEFAULT_GOAL := help

help: ## Show available commands
	@echo "$(GREEN)============================================================================================$(RESET)"
	@echo "$(GREEN)>>> List of commands:$(RESET)"
	@echo "$(GREEN)============================================================================================$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo "$(GREEN)============================================================================================$(RESET)"

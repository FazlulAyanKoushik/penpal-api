.PHONY: help build up up-build down logs shell migrate createsuperuser clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker images
	docker-compose build

up: ## Start containers
	docker-compose up -d

up-build: ## Build and start containers
	docker-compose up --build

down: ## Stop containers
	docker-compose down

logs: ## View logs
	docker-compose logs -f web

shell: ## Open Django shell
	docker-compose exec web python manage.py shell

migrate: ## Run migrations
	docker-compose exec web python manage.py migrate

makemigrations: ## Create migrations
	docker-compose exec web python manage.py makemigrations

createsuperuser: ## Create a superuser
	docker-compose exec web python manage.py createsuperuser

test: ## Run tests
	docker-compose exec web python manage.py test

clean: ## Remove containers and volumes
	docker-compose down -v
	docker system prune -f

restart: ## Restart containers
	docker-compose restart

status: ## Show container status
	docker-compose ps


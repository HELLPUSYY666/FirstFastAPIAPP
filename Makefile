.DEFAULT_GOAL := help

run:
	poetry run uvicorn alembic.src.main:app --host 0.0.0.0 --port 8000 --reload



install:
	@echo "Install dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall:
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

help:
	@echo "Usage make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-Za-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ".*?## "}; {printf " %-20s %s\n", $$1, $$2}'

update:
	@echo "Updating Poetry to the latest version..."
	poetry self update
	@echo "Updating all dependencies..."
	poetry update


.PHONY: setup clean test lint type-check format refactor
# Variables
SRC_DIR := .
TEST_DIR := .
help:
	@echo ""
	@echo "\033[1;32m▶ LOCAL COMMANDS:\033[0m"
	@echo "  make setup         - Create virtual environment and install dependencies"
	@echo "  make clean         - Remove virtual environment and cache files"
	@echo " "
	@echo "  make format        - Run format code"
	@echo "  make lint          - Run linter"
	@echo "  make test          - Run all tests"
	@echo "  make refactor      - Run all checks"
	@echo "  make demo          - Simple demoS"
	@echo "  make gwip          - Git wip 'some cmd'"
setup: clean
	curl -Ls https://astral.sh/uv/install.sh | bash
clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf **/__pycache__
test:
	uv run pytest
lint:
	uv run ruff check $(SRC_DIR) --fix
format:
	uv run ruff format $(SRC_DIR) $(TEST_DIR)
refactor: format lint test
demo:
	uv run py_fetch_skillboost.py course_templates 621
	uv run py_fetch_skillboost.py paths 16
	uv run py_fetch_skillboost.py paths 1 --allow_invalid_results
	uv run py_fetch_skillboost.py paths 2 --only_valid_results

gwip:
	git add -A && git commit -m "wip $$(date +%F)" && git push
gpush: refactor gwip
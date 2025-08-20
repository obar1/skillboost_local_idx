.PHONY: setup clean test lint type-check format refactor
# Variables
PYTHON := python3
VENV := .venv
SRC_DIR := .
TEST_DIR := .
PKG := 'https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb'
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
	@echo "  make demo      	- Simple demoS"
	@echo "  make gwip          - Git wip"
setup: clean
	$(PYTHON) -m pip install --upgrade uv
clean:
	rm -rf $(VENV)
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
	$(PYTHON) -m uv run py_fetch_skillboost.py paths 119
	$(PYTHON) -m uv run py_fetch_skillboost.py course_templates 939
gwip:
	git add -A && git commit -m "wip" && git push
gpush: refactor gwip 
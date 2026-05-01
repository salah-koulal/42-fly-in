NAME		=	fly-in

PYTHON		=	python3
PIP			=	pip3
MAIN		=	fly-in.py

# Colors
GREEN		=	\033[0;32m
CYAN		=	\033[0;36m
RESET		=	\033[0m

all:
	@echo "$(CYAN)Usage:$(RESET)"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run the project"
	@echo "  make clean     - Remove cache files"
	@echo "  make lint      - Run flake8 + mypy"

install:
	@echo "$(CYAN)Installing dependencies...$(RESET)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Done.$(RESET)"

run:
	@echo "$(CYAN)Running $(NAME)...$(RESET)"
	$(PYTHON) $(MAIN)

clean:
	@echo "$(CYAN)Cleaning...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc"       -delete 2>/dev/null || true
	find . -type f -name "*.pyo"       -delete 2>/dev/null || true
	@echo "$(GREEN)Clean.$(RESET)"

lint:
	@echo "$(CYAN)Running flake8...$(RESET)"
	flake8 .
	@echo "$(CYAN)Running mypy...$(RESET)"
	mypy . --warn-return-any --warn-unused-ignores \
		   --ignore-missing-imports \
		   --disallow-untyped-defs \
		   --check-untyped-defs
	@echo "$(GREEN)All checks passed.$(RESET)"

.PHONY: all install run clean lint
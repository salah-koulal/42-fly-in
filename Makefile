NAME        =   fly-in

PYTHON      =   python3
PIP         =   pip3
MAIN        =   fly-in.py

# (Default values)
MAPS_DIR         =  maps
VIZ         ?=
DEF_MAP = $(MAPS_DIR)/easy/01_linear_path.txt
# Colors
GREEN       =   \033[0;32m
CYAN        =   \033[0;36m
YELLOW      =   \033[0;33m
RESET       =   \033[0m

all:
	@echo "$(CYAN)🚀 Fly-in Makefile Usage:$(RESET)"
	@echo "  $(YELLOW)make install$(RESET)   - Install dependencies"
	@echo "  $(YELLOW)make run$(RESET)       - Run with default map ($(MAP))"
	@echo "  $(YELLOW)make run MAP=x$(RESET) - Run specific map (e.g., make run MAP=downloads/level1.txt)"
	@echo "  $(YELLOW)make run VIZ=1$(RESET) - Run with visualization (e.g., make run VIZ=1)"
	@echo "  $(YELLOW)make menu$(RESET)      - Interactive menu to choose a map"
	@echo "  $(YELLOW)make clean$(RESET)     - Remove cache files"
	@echo "  $(YELLOW)make lint$(RESET)      - Run flake8 + mypy"

install:
	@echo "$(CYAN)Installing dependencies...$(RESET)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Done.$(RESET)"

run:
	@echo "$(CYAN)Running $(NAME) with map: $(YELLOW)$(DEF_MAP)$(RESET)"
	@if [ "$(VIZ)" = "1" ]; then \
		$(PYTHON) $(MAIN) $(DEF_MAP) --viz; \
	else \
		$(PYTHON) $(MAIN) $(DEF_MAP); \
	fi

# ==========================================
# 🌟 BONUS: Interactive Menu
# ==========================================
menu:
	@echo "$(CYAN) Scanning for Maps in '$(MAPS_DIR)/'...$(RESET)"
	@FILES=$$(find $(MAPS_DIR) -type f -name "*.txt" | sort); \
	if [ -z "$$FILES" ]; then \
		echo "$(YELLOW)❌ No .txt maps found in $(MAPS_DIR) !$(RESET)"; \
	else \
		echo "$$FILES" | cat -n; \
		echo ""; \
		read -p "> Choose a map number: " num; \
		map=$$(echo "$$FILES" | sed -n "$$num"p); \
		if [ -z "$$map" ]; then \
			echo "$(YELLOW)❌ Invalid selection.$(RESET)"; \
		else \
			read -p "🎨 Enable Pygame Visualization? (y/n): " viz_ans; \
			echo ""; \
			if [ "$$viz_ans" = "y" ]; then \
				$(PYTHON) $(MAIN) $$map --viz; \
			else \
				$(PYTHON) $(MAIN) $$map; \
			fi \
		fi \
	fi

clean:
	@echo "$(CYAN)Cleaning...$(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc"       -delete 2>/dev/null || true
	@find . -type f -name "*.pyo"       -delete 2>/dev/null || true
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

.PHONY: all install run menu clean lint
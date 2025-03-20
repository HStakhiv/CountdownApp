PYTHON = python
PIP = pip
APP_NAME = CountdownApp
MAIN_FILE = main.py
VENV_NAME = venv
DIST_DIR = dist
BUILD_DIR = build

.PHONY: all
all: setup run

.PHONY: setup
setup:
	@echo "Setting up virtual environment..."
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Installing dependencies..."
ifeq ($(OS),Windows_NT)
	$(VENV_NAME)\Scripts\pip install -r requirements.txt
else
	$(VENV_NAME)/bin/pip install -r requirements.txt
endif

.PHONY: run
run:
	@echo "Running application..."
ifeq ($(OS),Windows_NT)
	$(VENV_NAME)\Scripts\python $(MAIN_FILE)
else
	$(VENV_NAME)/bin/python $(MAIN_FILE)
endif

.PHONY: test
test:
	@echo "Running unit tests..."
ifeq ($(OS),Windows_NT)
	$(VENV_NAME)\Scripts\python timer_unittest.py
else
	$(VENV_NAME)/bin/python timer_unittest.py
endif

.PHONY: build
build:
	@echo "Building executable..."
ifeq ($(OS),Windows_NT)
	$(VENV_NAME)\Scripts\pip install pyinstaller
	$(VENV_NAME)\Scripts\pyinstaller --name $(APP_NAME) --onefile --windowed $(MAIN_FILE)
else
	$(VENV_NAME)/bin/pip install pyinstaller
	$(VENV_NAME)/bin/pyinstaller --name $(APP_NAME) --onefile --windowed $(MAIN_FILE)
endif

.PHONY: freeze
freeze:
	@echo "Creating requirements.txt..."
ifeq ($(OS),Windows_NT)
	$(VENV_NAME)\Scripts\pip freeze > requirements.txt
else
	$(VENV_NAME)/bin/pip freeze > requirements.txt
endif

.PHONY: format
format:
	@echo "Formatting code with Black..."
ifeq ($(OS),Windows_NT)
	$(VENV_NAME)\Scripts\pip install black
	$(VENV_NAME)\Scripts\black *.py
else
	$(VENV_NAME)/bin/pip install black
	$(VENV_NAME)/bin/black *.py
endif

.PHONY: help
help:
	@echo "Kivy Countdown Timer Application Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  all       : Setup environment and run the application (default)"
	@echo "  setup     : Create virtual environment and install dependencies"
	@echo "  run       : Run the application"
	@echo "  test      : Run unit tests"
	@echo "  build     : Build standalone executable using PyInstaller"
	@echo "  freeze    : Generate requirements.txt from current environment"
	@echo "  format    : Format Python code using Black"
	@echo "  help      : Display this help message"

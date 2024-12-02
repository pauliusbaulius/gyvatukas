POETRY = ~/.local/bin/poetry  # TODO: Change to path on your system.
VENV = .venv
VENV_PY = $(VENV)/bin/python

$(VENV):
	python3 -m venv $(VENV)
	$(VENV_PY) -m pip install --upgrade pip


.PHONY: install
install: $(VENV)
	@echo "📦 installing dependencies"
	$(POETRY) export -f requirements.txt --without-hashes --dev > requirements.txt
	$(VENV_PY) -m pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: test
test: install
	@echo "🧪 running tests"
	$(VENV_PY) -m pytest tests/

.PHONY: docs
docs: install
	@echo "♻️ generating docs"
	$(VENV_PY) -m pdoc --html --force --output-dir docs gyvatukas

.PHONY: lint
lint:
	@echo "🧹 linting"
	$(VENV_PY) -m ruff check gyvatukas/ tests/

.PHONY: format
format:
	@echo "🧹 formatting"
	$(VENV_PY) -m ruff check --fix gyvatukas/ tests/
	$(VENV_PY) -m ruff format gyvatukas/ tests/

.PHONY: buildpackage
buildpkg: lint format test docs
	@echo "📦 building package"
	# TODO: Check if version already exists in dist/ and fail if it does.

	$(POETRY) build

.PHONY: publish
publishpkg: buildpkg
	@echo "🚀 publish package with `poetry publish`. this will not be implemented to prevent oopsies."

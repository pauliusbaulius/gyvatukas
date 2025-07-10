POETRY = ~/.local/bin/poetry  # TODO: Change to path on your system.
VENV = .venv
VENV_PY = $(VENV)/bin/python

$(VENV):
	$(POETRY) config virtualenvs.create true
	$(POETRY) config virtualenvs.in-project true
	$(POETRY) env use python3
	$(POETRY) install --with dev

.PHONY: install
install: $(VENV)
	@echo "📦 installing dependencies"
	$(POETRY) install --with dev

.PHONY: clean
clean:
	$(POETRY) env remove --all 2>/dev/null || true
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: test
test: install
	@echo "🧪 running tests"
	$(POETRY) run pytest tests/

.PHONY: docs
docs: install
	@echo "♻️ generating docs"
	$(POETRY) run pdoc --html --force --output-dir docs gyvatukas

.PHONY: lint
lint: install
	@echo "🧹 linting"
	$(POETRY) run ruff check gyvatukas/ tests/

.PHONY: format
format: install
	@echo "🧹 formatting"
	$(POETRY) run ruff check --fix gyvatukas/ tests/
	$(POETRY) run ruff format gyvatukas/ tests/

.PHONY: buildpkg
buildpkg: lint format test docs
	@echo "📦 building package"
	# TODO: Check if version already exists in dist/ and fail if it does.
	$(POETRY) build

.PHONY: publishpkg
publishpkg: buildpkg
	@echo "🚀 publish package with \`poetry publish\`. this will not be implemented to prevent oopsies."

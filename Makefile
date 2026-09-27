PANEL ?= http://127.0.0.1:8000

.PHONY: spec generate test lint docs build

spec:            ## fetch openapi.json from a panel running with DOCS=1
	curl -fsS $(PANEL)/openapi.json -o spec/openapi.json

generate:        ## regenerate models and resource classes from spec/openapi.json
	uv run datamodel-codegen --input spec/openapi.json --input-file-type openapi \
	  --output src/ixraypy/models.py --output-model-type pydantic_v2.BaseModel \
	  --use-standard-collections --use-union-operator --use-annotated \
	  --use-schema-description --use-field-description --target-python-version 3.11 \
	  --disable-timestamp --use-double-quotes --collapse-root-models
	uv run python scripts/generate.py
	uv run ruff format src scripts
	uv run ruff check src scripts --fix

test:
	uv run pytest -q

lint:
	uv run ruff check src scripts tests
	uv run ruff format --check src scripts tests

docs:
	uv run mkdocs build --strict

build:
	uv build

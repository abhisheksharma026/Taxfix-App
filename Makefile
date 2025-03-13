.PHONY: run install clean runner
.DEFAULT_GOAL := run
run: install
	cd src; poetry run python runner.py

install:
	poetry install --no-root

clean:
	rm -rf 'find . -type d -name __pycache__'
	rm -rf .ruff_cache

runner:
	run clean

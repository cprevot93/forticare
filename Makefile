.PHONY: init tests

init:
	pip install -r requirements.txt

tests:
	pytest tests --cov=forticare --cov-report=term-missing --cov-report=html --cov-fail-under=75 --no-cov-on-fail

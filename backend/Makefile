.PHONY: setup test run clean docker-build docker-run

setup:
	pip install -r requirements.txt

test:
	cd tests && python run_tests.py

run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker-compose build

docker-run:
	docker-compose up

docker-run-gpu:
	docker-compose up -d

docker-stop:
	docker-compose down

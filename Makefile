init:
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements-docker.txt

train:
	source venv/bin/activate && \
	python3 -m src.Models.Orquetrator

run:
	source venv/bin/activate && \
	python3 -m uvicorn src.Api.main:app --reload

freeze:
	source venv/bin/activate && \
	pip3 freeze > requirements-docker.txt

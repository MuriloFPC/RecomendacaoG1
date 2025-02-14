init:
	python -m venv venv
	.\venv\Scripts\activate && pip install -r requirements.txt

venv:
	.\venv\Scripts\activate

train:
	.\venv\Scripts\activate && python -m src.Models.Orquetrator

run:
	.\venv\Scripts\activate && python -m uvicorn src.Api.main:app --reload

freeze:
	.\venv\Scripts\activate &&	pip freeze > requirements.txt

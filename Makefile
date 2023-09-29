run:
	poetry run python manage.py runserver

lint:
	poetry run black examination/ exam66/
	poetry run flake8

test:
	poetry run pytest

cov:
	poetry run pytest --cov-report term-missing --cov=examination

start-cont:
	docker start psqlbox

run-cont:
	docker run -itd -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pw -p 5432:5432 --mount source=exam66vol,target=/var/lib/postgresql/data --name psqlbox postgres
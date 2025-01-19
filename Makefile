run:
	uv run python manage.py runserver

lint:
	uv run ruff check --fix examination/ exam66/

test:
	uv run pytest

test_noconf:
	uv run pytest --noconftest

dump-testdb:
	DROPDB=TRUE uv run pytest examination/tests/test_command.py::test_dumpdb

#run-testdb:
#	poetry run python manage.py testserver test_db_dump.json

#cov:
#	poetry run pytest --cov-report term-missing --cov=examination

drop-testdb:
	dropdb -h localhost -U user test_exam66db

start-cont:
	docker start psqlbox

run-cont:
	docker run -itd -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pw -p 5432:5432 --mount source=exam66vol,target=/var/lib/postgresql/data --name psqlbox postgres

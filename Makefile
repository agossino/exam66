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

cov:
#	uv run pytest --cov=path_to_be_checked_for_coverage --cov-report term-missing path_where_test_is_located
#	you can check even if the source of your test is executed (in order to discover some anomalies):
	uv run pytest --cov=users/ --cov=test/users/ --cov-report term-missing test/users/

drop-testdb:
	dropdb -h localhost -U user test_exam66db

start-cont:
	docker start psqlbox

run-cont:
	docker run -itd -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pw -p 5432:5432 --mount source=exam66vol,target=/var/lib/postgresql/data --name psqlbox postgres

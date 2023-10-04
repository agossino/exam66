import pytest

from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "data.json")
        call_command(
            "createuser",
            "examiners",
            "view_multichoicequestion",
            "examiner0",
            "examiner0@sciara.com",
            "pw",
        )

import pytest

from django.core.management import call_command
from django.contrib.auth.models import Group, Permission, User


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "data.json")


@pytest.fixture
def create_user():
    codename = "view_multichoicequestion"

    permission = Permission.objects.get(codename=codename)

    group_name = "examiners"

    examiners = Group.objects.create(name=group_name)

    examiners.permissions.add(permission)

    username = "examiner0"

    user = User.objects.create_user(username, "examiner0@sciara.com", "pw")

    user.save()

    user.groups.add(examiners)

    print("Users: ", User.objects.all().count())

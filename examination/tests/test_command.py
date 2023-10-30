from io import StringIO
import os


from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import transaction

import pytest


@pytest.mark.django_db
def test_users():
    users = User.objects.all()

    users_list = [user.username for user in users]

    assert users_list == ["user1", "user2", "user3", "examiner", "not_authorized"]


@pytest.mark.skipif(
    os.environ.get("DROPDB") is None, reason="Run only for dumping test database"
)
@pytest.mark.django_db
def test_dumpdb():
    ago = User.objects.create_superuser(username="ago", password="pw")
    print(ago)
    call_command("dumpdata", "--all", "-o", "examination/fixtures/test_db_dump.json")

    assert ago.check_password(r"pw")


@pytest.mark.django_db
class TestCreateuser:
    def test_user_created(self):
        user = "new_user"
        password = "pw"
        email = "user@sciara.com"
        group = "new_group"
        permission = "view_essayquestion"
        out = StringIO()
        call_command(
            "createuser",
            user,
            password,
            email,
            group=group,
            permission=permission,
            stdout=out,
        )

        assert f"{user} created" in out.getvalue()
        assert user in str(User.objects.all())

    def test_existing_user(self):
        user = "new_user"
        password = "pw"
        email = "user@sciara.com"
        out = StringIO()
        call_command(
            "createuser",
            user,
            password,
            email,
            stdout=out,
        )

        with transaction.atomic():
            with pytest.raises(CommandError):
                call_command(
                    "createuser",
                    user,
                    password,
                    email,
                    stdout=out,
                )
        assert user in str(User.objects.all())

    def test_user_without_permission_created(self):
        user = "new_user"
        password = "pw"
        email = "user@sciara.com"
        group = "new_group"
        out = StringIO()
        call_command("createuser", user, password, email, group=group, stdout=out)

        assert f"{user} created" in out.getvalue()
        assert user in str(User.objects.all())

    def test_user_without_group_created(self):
        user = "new_user"
        password = "pw"
        email = "user@sciara.com"
        out = StringIO()
        call_command("createuser", user, password, email, stdout=out)

        assert f"{user} created" in out.getvalue()
        assert user in str(User.objects.all())

    def test_wrong_permission(self):
        user = "new_user"
        password = "pw"
        email = "user@sciara.com"
        group = "new_group"
        permission = "wrong_permission"
        out = StringIO()
        with pytest.raises(CommandError):
            call_command(
                "createuser",
                user,
                password,
                email,
                group=group,
                permission=permission,
                stdout=out,
            )

    def test_existing_group(self):
        user = "new_user_1"
        password = "pw"
        email = "user@sciara.com"
        group = "new_group"
        out = StringIO()
        call_command("createuser", user, password, email, group=group, stdout=out)
        user = "new_user_2"
        call_command("createuser", user, password, email, group=group, stdout=out)

        assert f"{user} created" in out.getvalue()

    def test_group_existing_with_permission(self):
        user = "new_user"
        password = "pw"
        email = "user@sciara.com"
        group = "new_group"
        permission = "view_essayquestion"
        out = StringIO()
        call_command(
            "createuser",
            user,
            password,
            email,
            group=group,
            permission=permission,
            stdout=out,
        )
        user = "new_user_2"
        call_command(
            "createuser",
            user,
            password,
            email,
            group=group,
            permission=permission,
            stdout=out,
        )

        assert f"{user} created" in out.getvalue()

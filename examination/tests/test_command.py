from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError

import pytest


@pytest.mark.django_db
def test_users():
    from django.contrib.auth.models import User

    users = User.objects.all()

    users_list = [user.username for user in users]

    assert users_list == ["examiner0"]


@pytest.mark.django_db
class TestCreateuser:
    def test_user_created(self):
        group = "new_group"
        permission = "view_essayquestion"
        user = "new_user"
        email = "user@sciara.com"
        password = "pw"
        out = StringIO()
        call_command("createuser", group, permission, user, email, password, stdout=out)

        assert f"{user} created" in out.getvalue()

    def test_wrong_permission(self):
        group = "new_group"
        permission = "wrong_permission"
        user = "new_user"
        email = "user@sciara.com"
        password = "pw"
        out = StringIO()
        with pytest.raises(CommandError):
            call_command(
                "createuser", group, permission, user, email, password, stdout=out
            )

    def test_group_already_exists(self):
        group = "examiners"
        permission = "view_essayquestion"
        user = "new_user"
        email = "user@sciara.com"
        password = "pw"
        out = StringIO()
        with pytest.raises(CommandError):
            call_command(
                "createuser", group, permission, user, email, password, stdout=out
            )

    def test_user_already_exists(self):
        group = "new_group"
        permission = "view_essayquestion"
        user = "examiner0"
        email = "user@sciara.com"
        password = "pw"
        out = StringIO()
        with pytest.raises(CommandError):
            call_command(
                "createuser", group, permission, user, email, password, stdout=out
            )

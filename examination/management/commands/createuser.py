from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group, Permission, User


class Command(BaseCommand):
    help = """Create a new group with permission, add a new user to the group.
    Saved in app_folder/management/, run with: $ python manage.py createuser
    """

    def handle(self, *args, **kwargs):
        codename = "view_multichoicequestion"

        try:
            permission = Permission.objects.get(codename=codename)
        except NameError:
            raise CommandError("Wrong codename: %s", codename)

        group_name = "examiners"

        try:
            examiners = Group.objects.create(name=group_name)
        except IntegrityError:
            raise CommandError("Group %s already exists", group_name)

        examiners.permissions.add(permission)

        username = "examiner0"
        try:
            user = User.objects.create_user(username, "examiner0@sciara.com", "pw")
        except IntegrityError:
            raise CommandError("User %s already exists", username)

        user.save()

        user.groups.add(examiners)

        self.stdout.write(self.style.SUCCESS("User %s created" % user.username))

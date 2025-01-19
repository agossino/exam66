from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group, Permission, User


class Command(BaseCommand):
    """Create a new group with permission, add a new user to the group.
    Saved in app_folder/management/, run with: $ python manage.py createuser
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "username", help="User to be created and added to the given group"
        )
        parser.add_argument("password", help="User password")
        parser.add_argument("email", help="User email")
        parser.add_argument(
            "--group",
            help="Group name to be created, if not exists, and used for permission and user",
        )
        parser.add_argument(
            "--permission", help="Permission codename to be added to the given group"
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        password = kwargs["password"]
        email = kwargs["email"]
        group_name = kwargs["group"]
        permission_name = kwargs["permission"]

        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            raise CommandError("User %s already exists", username)

        if permission_name:
            try:
                permission = Permission.objects.get(codename=permission_name)
            except Permission.DoesNotExist:
                raise CommandError("Wrong permission codename: %s", permission_name)

        if group_name:
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                group = Group.objects.create(name=group_name)

        if group_name and permission_name:
            group.permissions.add(permission)

        user.save()

        if group_name:
            user.groups.add(group)

        self.stdout.write(self.style.SUCCESS("User %s created" % user.username))

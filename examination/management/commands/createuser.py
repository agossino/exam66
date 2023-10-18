from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group, Permission, User


class Command(BaseCommand):
    """Create a new group with permission, add a new user to the group.
    Saved in app_folder/management/, run with: $ python manage.py createuser
    """

    def add_arguments(self, parser):
        parser.add_argument("group", help="Group name to be created")
        parser.add_argument(
            "permission", help="Permission codename to be added to the given group"
        )
        parser.add_argument(
            "username", help="User to be created and added to the given group"
        )
        parser.add_argument("email", help="User email")
        parser.add_argument("password", help="User password")

    def handle(self, *args, **kwargs):
        group_name = kwargs["group"]
        permission = kwargs["permission"]
        username = kwargs["username"]
        email = kwargs["email"]
        password = kwargs["password"]

        try:
            permission = Permission.objects.get(codename=permission)
        except Permission.DoesNotExist:
            raise CommandError("Wrong permission codename: %s", permission)

        try:
            examiners = Group.objects.create(name=group_name)
        except IntegrityError:
            raise CommandError("Group %s already exists", group_name)

        examiners.permissions.add(permission)

        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            raise CommandError("User %s already exists", username)

        user.save()

        user.groups.add(examiners)

        self.stdout.write(self.style.SUCCESS("User %s created" % user.username))

    # def play_with_group_permission(self, *arg, **kwargs):
    #     permission_name = "Can change given answer"
    #     examinee = Group.objects.create(name="examinee")
    #     can_change_given_answer = Permission.objects.get(name=permission_name)
    #     examinee.permissions.add(can_change_given_answer)
    #     weired_group = Group.objects.create(name="Weired group made in 2023!!")
    #     weired_group.delete()

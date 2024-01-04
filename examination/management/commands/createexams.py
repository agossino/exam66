from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


from examination.models import EXAMINATION_TYPE, IssuedExam


class Command(BaseCommand):
    """Create a new group with permission, add a new user to the group.
    Saved in app_folder/management/, run with: $ python manage.py createuser
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "exam_tags_group_name", help="IssuedExam and Group to be created", nargs="*"
        )

    def handle(self, *args, **kwargs):
        """ "Create IssuedExam with the given exam_tag, new Group for each exam
        with exam_tag as name, and add the relevant Permission to the group."""
        permission_codenames = (
            "view_issuedexam",
            "view_selectedquestion",
            "view_givenanswer",
            "change_givenanswer",
        )

        for exam_tag_group_name in kwargs["exam_tags_group_name"]:
            permissions = [
                Permission.objects.get(codename=permission)
                for permission in permission_codenames
            ]
            group = Group.objects.create(name=exam_tag_group_name)
            group.permissions.add(*permissions)
            IssuedExam.objects.create(
                exam_tag=exam_tag_group_name,
                type=EXAMINATION_TYPE[0][0],
                groupname=group,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    "IssuedExam and Group %s created" % exam_tag_group_name
                )
            )
            for codename in permissions:
                self.stdout.write(
                    self.style.SUCCESS("Added %s to %s" % (codename, group))
                )

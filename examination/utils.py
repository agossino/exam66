from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse
from http import HTTPStatus

from examination.models import IssuedExam

EXAMINERS_GROUP_NAME = "examiners"


def get_groups_can_take_exam() -> set[Group]:
    """Return the groups that can take all exams: usually examiners group."""
    return {Group.objects.get(name=EXAMINERS_GROUP_NAME)}


def user_get_401_or_none(
    request: HttpRequest, issued_exam: IssuedExam
) -> HttpResponse | None:
    """Check if the logged in user belongs to a an allowed group."""
    allowed_groups = {issued_exam.groupname}.union(get_groups_can_take_exam())
    if not allowed_groups.intersection(set(request.user.groups.all())):
        response = HttpResponse(f"User {request.user} is not authorized.")
        response.status_code = HTTPStatus.UNAUTHORIZED
        return response

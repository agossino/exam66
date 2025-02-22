
from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse

import pytest

from selenium import webdriver

def test_dashboard_anonymous(client):
    url = reverse("dashboard")
    response = client.get(url)
    login_href = b'<a href="/users/accounts/login/">Login</a>'
    sign_up_href = b'<a href="/users/sign_up/">Sign up</a>'

    assert login_href in response.content
    assert sign_up_href in response.content

@pytest.mark.django_db
def test_dashboard_user(client):
    user = User.objects.create_user("user", "user@world.com", "pw")
    user.save()
    url = reverse("dashboard")
    client.login(username="user", password="pw")
    response = client.get(url, follow=True)
    logout_str = b'value="Logout"'
    pw_change_str =b'Change password'

    assert response.status_code == HTTPStatus.OK
    assert b"<title>django-bootstrap5 template title</title>" in response.content

    assert logout_str in response.content
    assert pw_change_str in response.content

@pytest.mark.usefixtures("selenium_drivers_init")
@pytest.mark.django_db
class TestBrowser1:
    def test_example(self, live_server):
        url = live_server.url + reverse("dashboard")
        self.driver.get(url)
        print(url)

        assert "django-bootstrap5 template title" in self.driver.title

    def test_user(self, user, live_server):
        # test/users/test_view.py::TestBrowser1::test_user[chrome]
        # test/users/test_view.py::TestBrowser1::test_user[firefox]
        # /home/ago/Devel/Python/exam66/.venv/lib/python3.11/site-packages/factory/django.py:182: DeprecationWarning: UserFactory._after_postgeneration will stop saving the instance after postgeneration hooks in the next major release.
        # If the save call is extraneous, set skip_postgeneration_save=True in the UserFactory.Meta.
        # To keep saving the instance, move the save call to your postgeneration hooks or override _after_postgeneration.
        #     warnings.warn(

        # -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
        print(f"{user}")
        assert True
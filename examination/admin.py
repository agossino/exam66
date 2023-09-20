from django.contrib import admin

from .models import EssayQuestion, MultiChoiceQuestion

admin.site.register([EssayQuestion, MultiChoiceQuestion])

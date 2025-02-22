import factory
from faker.providers import BaseProvider

from examination.models import EssayQuestion, SubjectModule
from django.contrib.auth.models import Group, User

class ExamProvider(BaseProvider):
    def auth_group(self):
        return self.random_element(
            ["examiners", "examinee A", "examinee B", "examinee C"]
        )

    def subject_module_description(self):
        return self.random_element(
            [
                "Maintenance Practices",
                "Human Factors",
                "Turbine Aeroplane Aerodynamics, Structures and Systems",
                "Piston Aeroplane Aerodynamics, Structures and Systems",
                "Piston Aeroplane Aerodynamics, Structures and Systems",
                "Helicopter Aerodynamics, Structures and Systems",
                "Aircraft Aerodynamics, Structures and Systems",
                "Propulsion",
                "Gas Turbine Engine",
                "Piston Engine",
                "Propeller",
                "Propeller",
                "Digital Techniques/Electronic Instrument Systems",
                "Materials and Hardware",
                "Maintenance Practices",
                "Basic Aerodynamics",
                "Human Factors",
                "Aviation Legislation",
                "Materials and hardware",
                "Aviation legislation",
                "Physics",
                "Propeller",
            ]
        )

factory.Faker.add_provider(ExamProvider)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.groups.add(*extracted)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker("auth_group")


class SubjectModuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubjectModule

    code = factory.Faker("lexify", text="??")
    description = factory.Faker("subject_module_description")


class EssayQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EssayQuestion
    module = factory.SubFactory(SubjectModuleFactory)
    text = factory.Faker("text")
    level = 1
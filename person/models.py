from django.utils import timezone

from django.db import models
from django.core.exceptions import ValidationError

from django.conf import settings


class UnsignedTinyIntField(models.SmallIntegerField):

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'tinyint unsigned'
        else:
            return super(UnsignedTinyIntField, self).db_type(connection)


# Create your models here.
class BaseModel(models.Model):
    create_at = models.DateTimeField(db_index=True, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(BaseModel):
    class Meta:
        db_table = "person"

    name = models.CharField(max_length=15, unique=True, null=False)
    age = UnsignedTinyIntField()
    etc = models.CharField(max_length=100, null=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name}:{self.age}"

    def clean(self):
        if self.create_at >= self.update_at:
            raise ValidationError("Update date cannot be before create date")


class PersonProfile(BaseModel):
    class Meta:
        db_table = "person_profile"

    person = models.OneToOneField(Person, related_name='person', name='person', on_delete=models.CASCADE)
    level = UnsignedTinyIntField()
    description = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f"Profile{self.person.name}"


class Watch(models.Model):
    class Meta:
        db_table = "watch"

    start_at = models.DateTimeField(db_index=True, auto_now_add=True)
    end_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

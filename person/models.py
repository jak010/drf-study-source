from django.db import models
from django.core.exceptions import ValidationError


class UnsignedTinyIntField(models.SmallIntegerField):

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'tinyint unsigned'
        else:
            return super(UnsignedTinyIntField, self).db_type(connection)


# Create your models here.
class BaseModel(models.Model):
    create_at = models.DateField(db_index=True, auto_now_add=True)
    update_at = models.DateField(auto_now=True)

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

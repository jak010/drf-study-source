import os
import pytz

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'config.settings'
)

import random
import django

django.setup()
from person import models
from django_seed import Seed

import datetime

create_at_start_date = datetime.date(year=1990, month=1, day=1)
create_at_end_date = datetime.date(year=2000, month=3, day=30)

update_at_start_date = datetime.date(year=2022, month=1, day=1)
update_at_end_date = datetime.date(year=2022, month=3, day=30)

seeder = Seed.seeder()

_LIMIT = 100

seeder.add_entity(models.Person, _LIMIT, {
    'age': lambda x: random.randint(1, 100),
    'name': lambda x: seeder.faker.name(),
    'etc': lambda x: seeder.faker.text(),
    'create_at': lambda x: seeder.faker.date_between(
        start_date=create_at_start_date,
        end_date=create_at_end_date,
    ),
    'update_at': lambda x: seeder.faker.date_between(
        start_date=update_at_start_date,
        end_date=update_at_end_date,
    )
})

seeder.execute()

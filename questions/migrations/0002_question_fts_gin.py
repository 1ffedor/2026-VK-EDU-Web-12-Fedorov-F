from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='question',
            index=GinIndex(
                SearchVector('title', weight='A', config='russian')
                + SearchVector('text', weight='B', config='russian'),
                name='question_fts_gin',
            ),
        ),
    ]

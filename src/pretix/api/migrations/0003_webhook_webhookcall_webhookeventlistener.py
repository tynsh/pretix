# Generated by Django 2.1.1 on 2018-11-07 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0102_auto_20181017_0024'),
        ('pretixapi', '0002_auto_20180604_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enable webhook')),
                ('target_url', models.URLField(verbose_name='Target URL')),
                ('all_events', models.BooleanField(default=False, verbose_name='All events (including newly created ones)')),
                ('limit_events', models.ManyToManyField(blank=True, to='pretixbase.Event', verbose_name='Limit to events')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.Organizer')),
            ],
        ),
        migrations.CreateModel(
            name='WebHookCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('target_url', models.URLField()),
                ('is_retry', models.BooleanField(default=False)),
                ('execution_time', models.FloatField(null=True)),
                ('return_code', models.PositiveIntegerField(default=0)),
                ('payload', models.TextField()),
                ('response_body', models.TextField()),
                ('webhook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixapi.WebHook')),
            ],
        ),
        migrations.CreateModel(
            name='WebHookEventListener',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(max_length=255)),
                ('webhook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixapi.WebHook')),
            ],
        ),
        migrations.AddField(
            model_name='webhookcall',
            name='success',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='webhook',
            name='all_events',
            field=models.BooleanField(default=True, verbose_name='All events (including newly created ones)'),
        ),
        migrations.AlterField(
            model_name='webhook',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webhooks', to='pretixbase.Organizer'),
        ),
        migrations.AlterField(
            model_name='webhookcall',
            name='webhook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='pretixapi.WebHook'),
        ),
        migrations.AlterField(
            model_name='webhookeventlistener',
            name='webhook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listeners', to='pretixapi.WebHook'),
        ),
    ]

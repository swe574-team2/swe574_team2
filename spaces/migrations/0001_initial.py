# Generated by Django 4.1.2 on 2023-03-26 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('policy', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=10)),
                ('image', models.ImageField(default='space_default.jpg', upload_to='space_pics')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='SpaceMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('basic_member', 'Basic Member'), ('pro_member', 'Pro Member'), ('moderator', 'Moderator')], default='basic_member', max_length=20)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'space')},
            },
        ),
        migrations.AddField(
            model_name='space',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='spaces', through='spaces.SpaceMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='space',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_spaces', to=settings.AUTH_USER_MODEL),
        ),
    ]
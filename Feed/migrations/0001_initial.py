# Generated by Django 4.1.1 on 2022-12-24 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_english', models.CharField(max_length=255)),
                ('title_telugu', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(max_length=255)),
                ('description_english', models.TextField(blank=True, null=True)),
                ('description_telugu', models.TextField(blank=True, null=True)),
                ('source_link', models.TextField()),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('shares_count', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('likes_count', models.IntegerField(default=0)),
                ('liked_users', models.JSONField(default=dict)),
                ('bookmarked_users', models.JSONField(default=dict)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(blank=True, max_length=1000, null=True)),
                ('post_type', models.CharField(blank=True, max_length=255, null=True)),
                ('user_id', models.IntegerField()),
                ('published', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_by', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Feed.posts')),
            ],
            options={
                'db_table': 'Likes',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=10000, null=True)),
                ('commented_by', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Feed.posts')),
            ],
            options={
                'db_table': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Bookmarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarked_by', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Feed.posts')),
            ],
            options={
                'db_table': 'Bookmarks',
            },
        ),
    ]

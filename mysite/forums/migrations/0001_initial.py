# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('closed', models.DateTimeField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('view_count', models.IntegerField(default=0, editable=False)),
                ('post_count', models.IntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='ForumCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(blank=True, to='forums.ForumCategory', related_name='subcategories', null=True)),
            ],
            options={
                'verbose_name_plural': 'forum categories',
            },
        ),
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('content_html', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('author', models.ForeignKey(related_name='forums_forumreply_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'forum replies',
                'verbose_name': 'forum reply',
            },
        ),
        migrations.CreateModel(
            name='ForumThread',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('content_html', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('title', models.CharField(max_length=100)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('sticky', models.IntegerField(default=0)),
                ('closed', models.DateTimeField(blank=True, null=True)),
                ('view_count', models.IntegerField(default=0, editable=False)),
                ('reply_count', models.IntegerField(default=0, editable=False)),
                ('subscriber_count', models.IntegerField(default=0, editable=False)),
                ('author', models.ForeignKey(related_name='forums_forumthread_related', to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(related_name='threads', to='forums.Forum')),
                ('last_reply', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.SET_NULL, to='forums.ForumReply', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThreadSubscription',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('kind', models.CharField(max_length=15)),
                ('thread', models.ForeignKey(related_name='subscriptions', to='forums.ForumThread')),
                ('user', models.ForeignKey(related_name='forum_subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPostCount',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(related_name='post_count', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='forumreply',
            name='thread',
            field=models.ForeignKey(related_name='replies', to='forums.ForumThread'),
        ),
        migrations.AddField(
            model_name='forum',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='forums.ForumCategory', null=True),
        ),
        migrations.AddField(
            model_name='forum',
            name='last_thread',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.SET_NULL, to='forums.ForumThread', related_name='+', null=True),
        ),
        migrations.AddField(
            model_name='forum',
            name='parent',
            field=models.ForeignKey(blank=True, to='forums.Forum', related_name='subforums', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='threadsubscription',
            unique_together=set([('thread', 'user', 'kind')]),
        ),
    ]

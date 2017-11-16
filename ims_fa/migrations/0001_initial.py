# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 09:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('nickname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=32)),
                ('salt', models.CharField(max_length=30)),
                ('avatar', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('loginfailure', models.IntegerField()),
                ('logintime', models.IntegerField()),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('token', models.CharField(max_length=59)),
                ('status', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ims_fa_admin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_id', models.IntegerField()),
                ('username', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('ip', models.CharField(max_length=50)),
                ('useragent', models.CharField(max_length=255)),
                ('createtime', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AmountRecords',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('member_name', models.CharField(max_length=45)),
                ('av_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('freeze_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('record_type', models.CharField(max_length=50)),
                ('remark', models.CharField(max_length=255)),
                ('createtime', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_amount_records',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(blank=True, null=True)),
                ('shortname', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('mergename', models.CharField(blank=True, max_length=255, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('pinyin', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
                ('first', models.CharField(blank=True, max_length=50, null=True)),
                ('lng', models.CharField(blank=True, max_length=100, null=True)),
                ('lat', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'ims_fa_area',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('imagewidth', models.CharField(max_length=30)),
                ('imageheight', models.CharField(max_length=30)),
                ('imagetype', models.CharField(max_length=30)),
                ('imageframes', models.IntegerField()),
                ('filesize', models.IntegerField()),
                ('mimetype', models.CharField(max_length=30)),
                ('extparam', models.CharField(max_length=255)),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('uploadtime', models.IntegerField()),
                ('storage', models.CharField(max_length=5)),
                ('sha1', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'ims_fa_attachment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('rules', models.TextField()),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('status', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ims_fa_auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('group_id', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_auth_group_access',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=4)),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=100, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=50)),
                ('condition', models.CharField(max_length=255)),
                ('remark', models.CharField(max_length=255)),
                ('ismenu', models.IntegerField()),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('weigh', models.IntegerField()),
                ('status', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ims_fa_auth_rule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=50)),
                ('flag', models.CharField(max_length=19)),
                ('image', models.CharField(max_length=100)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('diyname', models.CharField(max_length=30)),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('weigh', models.IntegerField()),
                ('status', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ims_fa_blog_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('pid', models.IntegerField()),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('comments', models.IntegerField()),
                ('ip', models.CharField(max_length=50)),
                ('useragent', models.CharField(max_length=50)),
                ('subscribe', models.IntegerField()),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('status', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'ims_fa_blog_comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.IntegerField()),
                ('flag', models.CharField(max_length=19)),
                ('title', models.CharField(max_length=50)),
                ('summary', models.CharField(max_length=1500)),
                ('content', models.TextField()),
                ('thumb', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=100)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('views', models.IntegerField()),
                ('comments', models.IntegerField()),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('weigh', models.IntegerField()),
                ('status', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'ims_fa_blog_post',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('starttime', models.IntegerField()),
                ('endtime', models.IntegerField()),
                ('background', models.CharField(max_length=10)),
                ('classname', models.CharField(max_length=30)),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('status', models.CharField(max_length=9)),
            ],
            options={
                'db_table': 'ims_fa_calendar',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('background', models.CharField(max_length=10)),
                ('classname', models.CharField(max_length=30)),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_calendar_event',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('type', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=50)),
                ('flag', models.CharField(max_length=19)),
                ('image', models.CharField(max_length=100)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('diyname', models.CharField(max_length=30)),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('weigh', models.IntegerField()),
                ('status', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ims_fa_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('group', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=100)),
                ('tip', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=30)),
                ('value', models.TextField()),
                ('content', models.TextField()),
                ('rule', models.CharField(max_length=100)),
                ('extend', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'ims_fa_config',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('member_id', models.IntegerField()),
                ('fb_content', models.CharField(max_length=255)),
                ('fb_images', models.CharField(max_length=500)),
                ('fb_state', models.IntegerField()),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_feedback',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('owner_id', models.IntegerField()),
                ('path', models.CharField(max_length=255)),
                ('image_type', models.IntegerField()),
                ('image_state', models.IntegerField()),
                ('is_selected', models.IntegerField()),
                ('createtime', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_images',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImagesShow',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=255)),
                ('image_type', models.IntegerField()),
                ('image_state', models.IntegerField()),
                ('is_selected', models.IntegerField()),
                ('createtime', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_images_show',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.IntegerField()),
                ('uniacid', models.IntegerField()),
                ('openid', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=11)),
                ('password', models.CharField(max_length=32)),
                ('withdraw_pwd', models.CharField(max_length=32)),
                ('salt', models.CharField(max_length=8)),
                ('nickname', models.CharField(max_length=20)),
                ('avatar', models.CharField(max_length=255)),
                ('wechat', models.CharField(max_length=30)),
                ('qq', models.CharField(max_length=15)),
                ('inviter_id', models.IntegerField()),
                ('realname', models.CharField(max_length=10)),
                ('nationality', models.CharField(max_length=15)),
                ('province', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('district', models.CharField(max_length=20)),
                ('taobao', models.CharField(max_length=30)),
                ('taoqi', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('taobao_image', models.CharField(max_length=255)),
                ('taoqi_image', models.CharField(max_length=255)),
                ('rating_image', models.CharField(max_length=255)),
                ('money_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('money_frozen', models.DecimalField(decimal_places=2, max_digits=8)),
                ('first_order', models.IntegerField()),
                ('reward_state', models.IntegerField()),
                ('state', models.IntegerField()),
                ('state_info', models.CharField(max_length=255)),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_members',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Merchants',
            fields=[
                ('merchant_id', models.AutoField(primary_key=True, serialize=False)),
                ('mobile', models.CharField(max_length=11)),
                ('password', models.CharField(default='', max_length=32)),
                ('salt', models.CharField(default='', max_length=8)),
                ('wechat', models.CharField(default='', max_length=30)),
                ('qq', models.CharField(default='', max_length=15)),
                ('realname', models.CharField(max_length=10)),
                ('own_shop', models.IntegerField(default=0, editable=False)),
                ('merchant_state', models.IntegerField(default=0, editable=False)),
                ('money_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('createtime', models.IntegerField(editable=False)),
                ('updatetime', models.IntegerField(editable=False)),
            ],
            options={
                'db_table': 'ims_fa_merchants',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Models',
            fields=[
                ('model_id', models.AutoField(primary_key=True, serialize=False)),
                ('realname', models.CharField(max_length=10)),
                ('gender', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.FloatField()),
                ('shoe', models.FloatField()),
                ('birthday', models.IntegerField()),
                ('nation', models.CharField(max_length=10)),
                ('avatar_image', models.CharField(max_length=255)),
                ('type', models.IntegerField()),
                ('level', models.IntegerField()),
                ('state', models.IntegerField()),
                ('is_del', models.IntegerField()),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
            ],
            options={
                'db_table': 'ims_fa_models',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_sn', models.CharField(max_length=20)),
                ('order_type', models.IntegerField()),
                ('platform_ordersn', models.CharField(max_length=20)),
                ('platform_payment', models.DecimalField(decimal_places=2, max_digits=8)),
                ('platform_orderimage', models.CharField(max_length=255)),
                ('platform_comment_pre', models.CharField(max_length=255)),
                ('platform_comment', models.CharField(max_length=255)),
                ('platform_comment_images', models.CharField(max_length=1024)),
                ('goods_title', models.CharField(max_length=80)),
                ('goods_url', models.CharField(max_length=255)),
                ('goods_image', models.CharField(max_length=255)),
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('goods_freight', models.DecimalField(decimal_places=2, max_digits=8)),
                ('task_commission', models.DecimalField(decimal_places=2, max_digits=6)),
                ('order_state', models.IntegerField()),
                ('evaluation_state', models.IntegerField()),
                ('tracking_company', models.CharField(max_length=50)),
                ('tracking_number', models.CharField(max_length=50)),
                ('createtime', models.IntegerField()),
                ('overdue_time', models.IntegerField()),
                ('payment_time', models.IntegerField()),
                ('sending_time', models.IntegerField()),
                ('finnshed_time', models.IntegerField()),
                ('back_consignee', models.CharField(max_length=20)),
                ('back_phone', models.CharField(max_length=12)),
                ('back_province', models.CharField(max_length=20)),
                ('back_city', models.CharField(max_length=20)),
                ('back_district', models.CharField(max_length=20)),
                ('back_address', models.CharField(max_length=45)),
                ('back_company', models.CharField(max_length=50)),
                ('back_number', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'ims_fa_order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('keywords', models.CharField(max_length=255)),
                ('flag', models.CharField(max_length=19)),
                ('image', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('icon', models.CharField(max_length=50)),
                ('views', models.IntegerField()),
                ('comments', models.IntegerField()),
                ('createtime', models.IntegerField()),
                ('updatetime', models.IntegerField()),
                ('weigh', models.IntegerField()),
                ('status', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ims_fa_page',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('publish_id', models.AutoField(primary_key=True, serialize=False)),
                ('pub_start', models.IntegerField()),
                ('pub_end', models.IntegerField(default=0)),
                ('pub_quantity', models.SmallIntegerField(default=0)),
                ('pub_surplus', models.SmallIntegerField(default=0)),
                ('pub_finished', models.SmallIntegerField(default=0)),
                ('pub_state', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'ims_fa_publish',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Saddress',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('consignee', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=12)),
                ('province', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('district', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=45)),
                ('is_default', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'ims_fa_saddress',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('store_id', models.AutoField(primary_key=True, serialize=False)),
                ('store_platform', models.IntegerField(default=0)),
                ('store_name', models.CharField(default='', max_length=45)),
                ('store_url', models.CharField(default='', max_length=45)),
                ('store_state', models.IntegerField(default=0, editable=False)),
                ('createtime', models.IntegerField(editable=False)),
            ],
            options={
                'db_table': 'ims_fa_stores',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_type', models.IntegerField()),
                ('task_name', models.CharField(default='', max_length=50, verbose_name='任务名称')),
                ('task_platform', models.IntegerField(default=0, verbose_name='任务平台')),
                ('goods_title', models.CharField(default='', max_length=80)),
                ('goods_url', models.CharField(default='', max_length=255)),
                ('goods_image', models.CharField(default='', max_length=255)),
                ('sku_image', models.CharField(default='', max_length=255)),
                ('goods_body', models.TextField(default='')),
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('goods_weight', models.FloatField(default=0)),
                ('goods_freight', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('task_commission', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('task_discount', models.FloatField(default=0)),
                ('keyword', models.CharField(default='', max_length=45)),
                ('position', models.CharField(default='', max_length=45)),
                ('search_image', models.CharField(default='', max_length=255)),
                ('condition_image', models.CharField(default='', max_length=255)),
                ('taotoken', models.TextField(default='')),
                ('qrcode_image', models.CharField(default='', max_length=255)),
                ('staytime', models.IntegerField(default=0)),
                ('add_favirate', models.IntegerField(default=0)),
                ('add_cart', models.IntegerField(default=0)),
                ('add_follow', models.IntegerField(default=0)),
                ('share_taotoken', models.IntegerField(default=0)),
                ('share_qrcode', models.IntegerField(default=0)),
                ('task_attention', models.TextField(default='')),
                ('model_taoqi_min', models.SmallIntegerField(default=0)),
                ('model_taoqi_max', models.SmallIntegerField(default=0)),
                ('model_level', models.IntegerField(default=0)),
                ('model_gender', models.IntegerField(default=0)),
                ('model_age_min', models.IntegerField(default=0)),
                ('model_age_max', models.IntegerField(default=0)),
                ('model_area', models.CharField(default='', max_length=255)),
                ('model_height_min', models.IntegerField(default=0)),
                ('model_height_max', models.IntegerField(default=0)),
                ('model_weight_min', models.IntegerField(default=0)),
                ('model_weight_max', models.IntegerField(default=0)),
                ('model_shoe_min', models.IntegerField(default=0)),
                ('model_shoe_max', models.IntegerField(default=0)),
                ('model_designated', models.CharField(default='', max_length=255)),
                ('photograph_scene', models.CharField(default='', max_length=45)),
                ('photograph_collocation', models.CharField(default='', max_length=45)),
                ('photograph_images', models.CharField(default='', max_length=255)),
                ('photograph_attention', models.TextField(default='')),
                ('address_id', models.IntegerField(null=True)),
                ('return_attention', models.TextField(default='')),
                ('task_state', models.IntegerField(default=0)),
                ('createtime', models.IntegerField(default=0, editable=False)),
                ('updatetime', models.IntegerField(default=0, editable=False)),
                ('taoqi_filter', models.IntegerField(default=0)),
                ('age_filter', models.IntegerField(default=0)),
                ('height_filter', models.IntegerField(default=0)),
                ('weight_filter', models.IntegerField(default=0)),
                ('shoe_filter', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'ims_fa_tasks',
                'managed': False,
            },
        ),
    ]

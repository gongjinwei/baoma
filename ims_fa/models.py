# -*- coding:UTF-8 -*-
from urllib.parse import urlsplit

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
import datetime
from .permission import create_records


class Admin(models.Model):
    username = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    salt = models.CharField(max_length=30)
    avatar = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    loginfailure = models.IntegerField()
    logintime = models.IntegerField()
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    token = models.CharField(max_length=59)
    status = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ims_fa_admin'


class AdminLog(models.Model):
    admin_id = models.IntegerField()
    username = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    ip = models.CharField(max_length=50)
    useragent = models.CharField(max_length=255)
    createtime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ims_fa_admin_log'


class AmountRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey('Members', db_column='member_id')
    member_name = models.CharField(max_length=45)
    av_amount = models.DecimalField(max_digits=8, decimal_places=2)
    freeze_amount = models.DecimalField(max_digits=8, decimal_places=2)
    record_type = models.CharField(max_length=50)
    remark = models.CharField(max_length=255)
    createtime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ims_fa_amount_records'


class Area(models.Model):
    pid = models.IntegerField(blank=True, null=True)
    shortname = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    mergename = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    pinyin = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    first = models.CharField(max_length=50, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)
    lat = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ims_fa_area'


class Attachment(models.Model):
    url = models.CharField(max_length=255)
    imagewidth = models.CharField(max_length=30)
    imageheight = models.CharField(max_length=30)
    imagetype = models.CharField(max_length=30)
    imageframes = models.IntegerField()
    filesize = models.IntegerField()
    mimetype = models.CharField(max_length=30)
    extparam = models.CharField(max_length=255)
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    uploadtime = models.IntegerField()
    storage = models.CharField(max_length=5)
    sha1 = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'ims_fa_attachment'


class AuthGroup(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=100)
    rules = models.TextField()
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    status = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ims_fa_auth_group'


class AuthGroupAccess(models.Model):
    uid = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ims_fa_auth_group_access'
        unique_together = (('uid', 'group_id'),)


class AuthRule(models.Model):
    type = models.CharField(max_length=4)
    pid = models.IntegerField()
    name = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    condition = models.CharField(max_length=255)
    remark = models.CharField(max_length=255)
    ismenu = models.IntegerField()
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    weigh = models.IntegerField()
    status = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ims_fa_auth_rule'


class BlogCategory(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50)
    flag = models.CharField(max_length=19)
    image = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    diyname = models.CharField(max_length=30)
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    weigh = models.IntegerField()
    status = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ims_fa_blog_category'


class BlogComment(models.Model):
    post_id = models.IntegerField()
    pid = models.IntegerField()
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    content = models.TextField()
    comments = models.IntegerField()
    ip = models.CharField(max_length=50)
    useragent = models.CharField(max_length=50)
    subscribe = models.IntegerField()
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    status = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'ims_fa_blog_comment'


class BlogPost(models.Model):
    category_id = models.IntegerField()
    flag = models.CharField(max_length=19)
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=1500)
    content = models.TextField()
    thumb = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    views = models.IntegerField()
    comments = models.IntegerField()
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    weigh = models.IntegerField()
    status = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'ims_fa_blog_post'


class Calendar(models.Model):
    admin_id = models.IntegerField()
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    starttime = models.IntegerField()
    endtime = models.IntegerField()
    background = models.CharField(max_length=10)
    classname = models.CharField(max_length=30)
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    status = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'ims_fa_calendar'


class CalendarEvent(models.Model):
    admin_id = models.IntegerField()
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    background = models.CharField(max_length=10)
    classname = models.CharField(max_length=30)
    createtime = models.IntegerField()
    updatetime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ims_fa_calendar_event'


class Category(models.Model):
    pid = models.IntegerField()
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50)
    flag = models.CharField(max_length=19)
    image = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    diyname = models.CharField(max_length=30)
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    weigh = models.IntegerField()
    status = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ims_fa_category'


class Config(models.Model):
    name = models.CharField(unique=True, max_length=30)
    group = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    tip = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    value = models.TextField()
    content = models.TextField()
    rule = models.CharField(max_length=100)
    extend = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ims_fa_config'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField()
    fb_content = models.CharField(max_length=255)
    fb_images = models.CharField(max_length=500)
    fb_state = models.IntegerField()
    createtime = models.IntegerField()
    updatetime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ims_fa_feedback'


class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    owner_id = models.IntegerField()
    path = models.CharField(max_length=255)
    image_type = models.IntegerField()
    image_state = models.IntegerField()
    is_selected = models.IntegerField()
    createtime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ims_fa_images'


class ImagesShow(models.Model):
    image_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey('Order',related_name='imagesShow',db_column='owner_id')
    path = models.ImageField(max_length=255,editable=False)
    image_type = models.IntegerField()
    image_state = models.IntegerField(editable=False)
    is_selected = models.IntegerField(editable=False)
    createtime = models.IntegerField(editable=False)

    class Meta:
        managed = False
        db_table = 'ims_fa_images_show'


class Members(models.Model):
    member_id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    uniacid = models.IntegerField()
    openid = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    password = models.CharField(max_length=32)
    withdraw_pwd = models.CharField(max_length=32)
    salt = models.CharField(max_length=8)
    nickname = models.CharField(max_length=20)
    avatar = models.CharField(max_length=255)
    wechat = models.CharField(max_length=30)
    qq = models.CharField(max_length=15)
    inviter_id = models.IntegerField()
    realname = models.CharField(max_length=10)
    nationality = models.CharField(max_length=15)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    taobao = models.CharField(max_length=30)
    taoqi = models.IntegerField()
    rating = models.IntegerField()
    taobao_image = models.CharField(max_length=255)
    taoqi_image = models.CharField(max_length=255)
    rating_image = models.CharField(max_length=255)
    money_balance = models.DecimalField(max_digits=8, decimal_places=2)
    money_frozen = models.DecimalField(max_digits=8, decimal_places=2)
    first_order = models.IntegerField()
    reward_state = models.IntegerField()
    state = models.IntegerField()
    state_info = models.CharField(max_length=255)
    createtime = models.IntegerField()
    updatetime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ims_fa_members'


class Merchants(models.Model):
    merchant_id = models.AutoField(primary_key=True)
    mobile = models.CharField(max_length=11)
    password = models.CharField(max_length=32,default='')
    salt = models.CharField(max_length=8,default='')
    wechat = models.CharField(max_length=30,default='')
    qq = models.CharField(max_length=15,default='')
    realname = models.CharField(max_length=10)
    own_shop = models.IntegerField(editable=False,default=0)
    merchant_state = models.IntegerField(editable=False,default=10)
    money_balance = models.DecimalField(max_digits=10, decimal_places=2,default=0,editable=False)
    level = models.ForeignKey('MerchantLevel',default=1)
    referee_id = models.IntegerField(default=0)
    expiry_time = models.IntegerField(default=0,editable=False)
    createtime = models.IntegerField(editable=False)
    updatetime = models.IntegerField(editable=False)
    user = models.OneToOneField(User,editable=False,null=True)

    class Meta:
        managed = False
        db_table = 'ims_fa_merchants'

    def save(self, *args,**kwargs):
        self.updatetime=datetime.datetime.timestamp(datetime.datetime.now())
        super(Merchants,self).save(*args,**kwargs)

    def __str__(self):
        return self.realname


pre_save.connect(create_records,Merchants)


class MerchantLevel(models.Model):
    level_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    discount = models.SmallIntegerField(default=100)
    store_num = models.SmallIntegerField(default=0)
    sort = models.IntegerField(default=0)
    createtime = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table='ims_fa_merchant_level'


class Models(models.Model):
    model_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey('Members', db_column='member_id')
    realname = models.CharField(max_length=10)
    gender = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    shoe = models.FloatField()
    birthday = models.IntegerField()
    nation = models.CharField(max_length=10)
    avatar_image = models.CharField(max_length=255)
    type = models.IntegerField()
    level = models.IntegerField()
    state = models.IntegerField()
    is_del = models.IntegerField()
    createtime = models.IntegerField()
    updatetime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ims_fa_models'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey('Members', db_column='member_id', related_name='orders')
    publish_id = models.ForeignKey('Publish', db_column='publish_id', related_name='orders')
    order_sn = models.CharField(max_length=20)
    order_type = models.IntegerField()
    platform_ordersn = models.CharField(max_length=20)
    platform_payment = models.DecimalField(max_digits=8, decimal_places=2)
    platform_orderimage = models.CharField(max_length=255)
    platform_comment_pre = models.CharField(max_length=255)
    platform_comment = models.CharField(max_length=255)
    platform_comment_images = models.CharField(max_length=1024)
    goods_title = models.CharField(max_length=80)
    goods_url = models.CharField(max_length=255)
    goods_image = models.ImageField(max_length=255,editable=False)
    goods_price = models.DecimalField(max_digits=8, decimal_places=2)
    goods_freight = models.DecimalField(max_digits=8, decimal_places=2)
    task_commission = models.DecimalField(max_digits=6, decimal_places=2)
    order_state = models.IntegerField()
    evaluation_state = models.IntegerField()
    tracking_company = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50)
    createtime = models.IntegerField()
    overdue_time = models.IntegerField()
    payment_time = models.IntegerField()
    sending_time = models.IntegerField()
    finnshed_time = models.IntegerField()
    back_consignee = models.CharField(max_length=20)
    back_phone = models.CharField(max_length=12)
    back_province = models.CharField(max_length=20)
    back_city = models.CharField(max_length=20)
    back_district = models.CharField(max_length=20)
    back_address = models.CharField(max_length=45)
    back_company = models.CharField(max_length=50)
    back_number = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ims_fa_order'


class Page(models.Model):
    category_id = models.IntegerField()
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    flag = models.CharField(max_length=19)
    image = models.CharField(max_length=255)
    content = models.TextField()
    icon = models.CharField(max_length=50)
    views = models.IntegerField()
    comments = models.IntegerField()
    createtime = models.IntegerField()
    updatetime = models.IntegerField()
    weigh = models.IntegerField()
    status = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ims_fa_page'


class Publish(models.Model):
    publish_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey('Tasks', db_column='task_id', related_name='publishes', null=True)
    pub_start = models.IntegerField(null=True)
    pub_end = models.IntegerField(default=0)
    pub_quantity = models.SmallIntegerField(default=0)
    pub_surplus = models.SmallIntegerField(default=0)
    pub_finished = models.SmallIntegerField(default=0)
    pub_state = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'ims_fa_publish'


class Saddress(models.Model):
    address_id = models.AutoField(primary_key=True)
    merchant_id = models.ForeignKey('Merchants', db_column='merchant_id', related_name='addresses',editable=False)
    consignee = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    address = models.CharField(max_length=45)
    is_default = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'ims_fa_saddress'

    def save(self,*args,**kwargs):
        if self.is_default:
            addresses=Saddress.objects.filter(merchant_id=self.merchant_id)
            if addresses:
                addresses.update(is_default=0)
        super(Saddress,self).save(*args,**kwargs)


class Stores(models.Model):
    store_id = models.AutoField(primary_key=True)
    merchant_id = models.ForeignKey('Merchants', db_column='merchant_id', related_name='stores',editable=False)
    store_platform = models.IntegerField(default=0)
    store_name = models.CharField(max_length=45,default='')
    store_url = models.CharField(max_length=255,default='')
    store_state = models.IntegerField(default=0,editable=False)
    createtime = models.IntegerField(editable=False)

    class Meta:
        managed = False
        db_table = 'ims_fa_stores'

    def __str__(self):
        return self.store_name


class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey('Stores',db_column='store_id',related_name='tasks')
    task_type = models.IntegerField()
    task_name = models.CharField(max_length=50, verbose_name='任务名称', default='')
    task_platform = models.IntegerField(verbose_name='任务平台', default=0)
    goods_title = models.CharField(max_length=80, default='')
    goods_url = models.CharField(max_length=255, default='')
    goods_image = models.CharField(max_length=255, default='')
    sku_image = models.CharField(max_length=255, default='')
    goods_body = models.CharField(default='',max_length=1024)
    goods_price = models.DecimalField(max_digits=8, decimal_places=2)
    goods_weight = models.FloatField(default=0)
    goods_freight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    task_commission = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    task_discount = models.FloatField(default=0)
    keyword = models.CharField(max_length=45, default='')
    position = models.CharField(max_length=45, default='')
    search_image = models.CharField(max_length=255, default='')
    condition_image = models.CharField(max_length=255, default='')
    taotoken = models.CharField(default='',max_length=1024,null=True)
    qrcode_image = models.CharField(max_length=255, default='')
    staytime = models.IntegerField(default=0)
    add_favirate = models.IntegerField(default=0)
    add_cart = models.IntegerField(default=0)
    add_follow = models.IntegerField(default=0)
    share_taotoken = models.IntegerField(default=0)
    share_qrcode = models.IntegerField(default=0)
    task_attention = models.TextField(default='',null=True)
    model_taoqi_min = models.SmallIntegerField(default=0)
    model_taoqi_max = models.SmallIntegerField(default=0)
    model_level = models.IntegerField(default=0)
    model_gender = models.IntegerField(default=0)
    model_age_min = models.IntegerField(default=0)
    model_age_max = models.IntegerField(default=0)
    model_area = models.CharField(max_length=255, default='')
    model_height_min = models.IntegerField(default=0)
    model_height_max = models.IntegerField(default=0)
    model_weight_min = models.IntegerField(default=0)
    model_weight_max = models.IntegerField(default=0)
    model_shoe_min = models.IntegerField(default=0)
    model_shoe_max = models.IntegerField(default=0)
    model_designated = models.CharField(max_length=255, default='')
    photograph_scene = models.CharField(max_length=45, default='')
    photograph_collocation = models.CharField(max_length=45, default='')
    photograph_images = models.CharField(max_length=255, default='')
    photograph_attention = models.TextField(default='',null=True)
    address_id = models.IntegerField()
    return_attention = models.TextField(default='',null=True)
    task_state = models.IntegerField(default=10)
    createtime = models.IntegerField(default=0,editable=False)
    updatetime = models.IntegerField(default=0,editable=False)
    taoqi_filter = models.IntegerField(default=0)
    age_filter = models.IntegerField(default=0)
    height_filter = models.IntegerField(default=0)
    weight_filter = models.IntegerField(default=0)
    shoe_filter = models.IntegerField(default=0)
    is_return = models.SmallIntegerField(default=0)
    owner = models.ForeignKey(User, null=True)
    more_comment_filter=models.SmallIntegerField(default=0)
    more_comment_attention=models.TextField(default='')
    video_comment_filter=models.SmallIntegerField(default=0)
    video_comment_attention=models.TextField(default='')

    class Meta:
        managed = False
        db_table = 'ims_fa_tasks'

    def save(self,*args,**kwargs):
        self.goods_image=self.cut_host(self.goods_image)
        self.sku_image=self.cut_host(self.sku_image)
        self.search_image=self.cut_host(self.search_image)
        self.qrcode_image=self.cut_host(self.qrcode_image)
        self.photograph_images=self.cut_host(self.photograph_images)
        self.condition_image=self.cut_host(self.condition_image)
        self.updatetime=datetime.datetime.timestamp(datetime.datetime.now())
        super(Tasks,self).save(*args,**kwargs)

    def cut_host(self,charfield):
        if charfield.startswith('http'):
            charfield = urlsplit(charfield).path

        return charfield


class ImageUp(models.Model):
    image = models.ImageField(upload_to='baoma/%Y%m%d', max_length=255)
    merchant=models.ForeignKey('Merchants',on_delete=models.DO_NOTHING,editable=False,null=True)
    createtime=models.IntegerField(editable=False)

    class Meta:
        managed = False


class ConsumeRecords(models.Model):
    consume_id = models.AutoField(primary_key=True)
    merchant_id = models.ForeignKey('Merchants',related_name='consumerecords',db_column='merchant_id',on_delete=models.DO_NOTHING)
    merchant_name = models.CharField(max_length=55)
    pay_type = models.IntegerField()
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expense = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.CharField(max_length=255)
    createtime = models.IntegerField()
    operator_id = models.IntegerField()
    operator_name = models.CharField(max_length=55)

    class Meta:
        managed = False
        db_table = 'ims_fa_consume_records'


class MerchantRecharge(models.Model):
    recharge_id = models.AutoField(primary_key=True)
    merchant = models.ForeignKey('Merchants')
    realname=models.CharField(max_length=45,default='')
    mobile = models.CharField(max_length=45,default='')
    pay_type=models.SmallIntegerField(default=0)
    order_num=models.CharField(max_length=45,default='')
    amount = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    voucher_image=models.CharField(max_length=255,default='')
    state = models.SmallIntegerField(default=0)
    remark = models.CharField(max_length=45,default='')
    operator_id=models.IntegerField(default=0)
    createtime=models.IntegerField(editable=False)
    operator_name =models.CharField(max_length=55,default='')


    class Meta:
        managed = False
        db_table = 'ims_fa_merchant_recharge'

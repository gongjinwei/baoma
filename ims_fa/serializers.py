# -*- coding:UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models
import uuid, re

from django.contrib.auth.models import User


class UUIDImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Image validation is a bit grungy, so we'll just outright
        # defer to Django's implementation so we don't need to
        # consider it, or treat PIL as a test dependency.
        file_object = serializers.FileField.to_internal_value(self, data)
        extension = file_object.name.split('.')[-1]
        file_object.name = '.'.join([str(uuid.uuid4()).replace('-', '')[:20], extension])
        django_field = self._DjangoImageField()
        django_field.error_messages = self.error_messages
        return django_field.clean(file_object)


class ImagesShowSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner_id.order_id')

    class Meta:
        model = models.ImagesShow
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    imagesShow = ImagesShowSerializer(read_only=True, many=True)
    taobao = serializers.ReadOnlyField(source='member_id.taobao')

    class Meta:
        model = models.Order
        fields = '__all__'


class PublishSerializer(serializers.ModelSerializer):
    task_id = serializers.ReadOnlyField(source='task_id.task_id')

    class Meta:
        model = models.Publish
        fields = '__all__'


class TasksSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    publish_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Tasks
        fields = '__all__'
        read_only_fields = ('owner',)

    def get_publish_count(self, obj):
        publishes = obj.publishes
        pub_surplus = sum(publishes.values_list('pub_surplus', flat=True))
        pub_quantity = sum(publishes.values_list('pub_quantity', flat=True))
        return dict(pub_quantity=pub_quantity, pub_surplus=pub_surplus)


class StoresSerializer(serializers.ModelSerializer):
    merchant_id = serializers.ReadOnlyField(source='merchant_id.merchant_id')  # 设置了readOnly的字段不会在写入时被检测到

    class Meta:
        model = models.Stores
        fields = '__all__'


class SaddressSerializer(serializers.ModelSerializer):
    merchant_id = serializers.ReadOnlyField(source='merchant_id.merchant_id')

    class Meta:
        model = models.Saddress
        fields = '__all__'


class MerchantLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MerchantLevel
        fields = '__all__'


class MerchantsSerializer(serializers.ModelSerializer):
    stores = serializers.StringRelatedField(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.id')
    email = serializers.ReadOnlyField(source='user.email')
    level = MerchantLevelSerializer(read_only=True)

    class Meta:
        model = models.Merchants
        exclude = ['password', 'salt']


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = '__all__'


class ImageUpSerializer(serializers.ModelSerializer):
    image = UUIDImageField(required=True)
    merchant = serializers.ReadOnlyField(source='merchant.merchant_id')

    class Meta:
        model = models.ImageUp
        fields = '__all__'


class ConsumeRecordsSerializer(serializers.ModelSerializer):
    merchant_id = serializers.ReadOnlyField(source='merchant_id.merchant_id')

    class Meta:
        model = models.ConsumeRecords
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class MerchantRechargeSerializer(serializers.ModelSerializer):
    merchant = serializers.ReadOnlyField(source='merchant.merchant_id')

    class Meta:
        model = models.MerchantRecharge
        fields = '__all__'


def mobile_validator(value):
    matcher = re.match('^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$', value)
    if not matcher:
        raise serializers.ValidationError('手机号码不正确')


def code_validator(value):
    matcher = re.match(r'^\d{6}$', value)
    if not matcher:
        raise serializers.ValidationError('验证码不正确')


class MerchantRegisterSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=True, validators=[mobile_validator],
                                   help_text='11位手机号，符号手机号规则，不能与注册手机重复')
    code = serializers.CharField(required=True, validators=[code_validator], help_text='6位数字短信验证码')
    password = serializers.CharField(required=True, min_length=5, help_text='密码，不少于5位',
                                     style={'input_type': 'password'})
    username = serializers.CharField(required=True, source='user.username', help_text='登录用户名')
    email = serializers.EmailField(required=True, source='user.email', help_text='邮箱')

    class Meta:
        model = models.Merchants
        exclude = ['password', 'salt']


class RegisterMobileSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, validators=[mobile_validator,
                                                              UniqueValidator(queryset=models.Merchants.objects.all(),
                                                                              message='该手机号已经注册过了')],
                                   help_text='11位手机号，符号手机号规则')


class ForgetMobileSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, validators=[mobile_validator], help_text='11位手机号，符号手机号规则')


class PasswordSetSerializer(ForgetMobileSerializer):
    code = serializers.CharField(required=True, validators=[code_validator], help_text='6位数字短信验证码')
    password = serializers.CharField(required=True, min_length=5, help_text='新密码，不少于5位',
                                     style={'input_type': 'password'})


class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=5, help_text='输入登录密码/旧密码',
                                         style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, min_length=5, help_text='新密码！如果是超级用户可修改具体的商家密码，否则只能修改登录密码',
                                         style={'input_type': 'password'})

# -*- coding:UTF-8 -*-
from rest_framework import serializers
from . import models
import uuid


class UUIDImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Image validation is a bit grungy, so we'll just outright
        # defer to Django's implementation so we don't need to
        # consider it, or treat PIL as a test dependency.
        file_object = serializers.FileField.to_internal_value(self,data)
        extension = file_object.name.split('.')[-1]
        file_object.name='.'.join([str(uuid.uuid4()).replace('-','')[:12],extension])
        django_field = self._DjangoImageField()
        django_field.error_messages = self.error_messages
        return django_field.clean(file_object)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Admin
        fields = '__all__'


class ImagesShowSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner_id.order_id')

    class Meta:
        model = models.ImagesShow
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    imagesShow = ImagesShowSerializer(read_only=True,many=True)

    class Meta:
        model = models.Order
        fields = '__all__'


class PublishSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(source='task_id.task_id')

    class Meta:
        model = models.Publish
        fields = '__all__'


class TasksSerializer(serializers.ModelSerializer):
    owner =serializers.ReadOnlyField(source='owner.username')
    store_id = serializers.IntegerField(source='store_id.store_id')

    class Meta:
        model = models.Tasks
        fields = '__all__'
        read_only_fields = ('owner',)


class StoresSerializer(serializers.ModelSerializer):
    merchant_id =serializers.ReadOnlyField(source='merchant_id.merchant_id')

    class Meta:
        model = models.Stores
        fields = '__all__'


class SaddressSerializer(serializers.ModelSerializer):
    merchant_id=serializers.ReadOnlyField(source='merchant_id.merchant_id')

    class Meta:
        model = models.Saddress
        fields = '__all__'


class MerchantsSerializer(serializers.ModelSerializer):
    stores = serializers.StringRelatedField(many=True,read_only=True)
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = models.Merchants
        exclude = ['password',]


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = '__all__'


class MembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Members
        fields = '__all__'


class ModelsSerializer(serializers.ModelSerializer):
    member_id = MembersSerializer()

    class Meta:
        model = models.Models
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = '__all__'


class ImageUpSerializer(serializers.ModelSerializer):
    image = UUIDImageField(required=True)
    merchant = serializers.ReadOnlyField(source='merchant.merchant_id')

    class Meta:
        model = models.ImageUp
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Feedback
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Images
        fields = '__all__'


class BlogCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BlogComment
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BlogPost
        fields = '__all__'


class BlogCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BlogCategory
        fields = '__all__'


class ConsumeRecordsSerializer(serializers.ModelSerializer):
    merchant_id = serializers.ReadOnlyField(source='merchant_id.merchant_id')

    class Meta:
        model = models.ConsumeRecords
        fields = '__all__'




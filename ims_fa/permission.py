# -*- coding:UTF-8 -*-
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission
from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import ValidationError,PermissionDenied
import operator
from django.db import models
from functools import reduce
from decimal import Decimal

from datetime import datetime


def create_permission(sender, instance, created=False, *args, **kwargs):
    from .models import Tasks
    task = instance
    content_type = ContentType.objects.get_for_model(Tasks)
    codename = 'taskpermission_{}'.format(task.task_id)
    name = task.task_name

    if created:
        Permission.objects.create(
            codename=codename,
            name=name,
            content_type=content_type
        )

    else:
        if task.is_active:
            permissions = Permission.objects.filter(codename=codename, content_type=content_type)
            if not permissions.exists():
                Permission.objects.create(
                    codename=codename,
                    content_type=content_type,
                    name=name
                )
            else:
                permission=permissions[0]
                if permission.name != name:
                    permission.name = name
                    permission.save()
        else:
            Permission.objects.filter(codename=codename, content_type=content_type)


class UserPermissionFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        """
            如果是超级用户不对它进行过滤，普通用户根据view.filter_from进行判断
        """
        user = request.user
        if user.is_superuser:
            return queryset
        if queryset.model._meta.model_name != 'merchants':
            if not hasattr(request.user,'merchants'):
                raise ValidationError('you must create merchant first')
        assert view.filter_from is not None,"view hasn't attribute `filter_from`"
        assert isinstance(view.filter_from,list),"filter_from must be a list"
        filter_from = getattr(view, 'filter_from')
        conditions =[]
        queries = [models.Q(**{lookup:request.user.id}) for lookup in filter_from]
        conditions.append(reduce(operator.or_,queries))
        return queryset.filter(reduce(operator.and_,conditions))


class ModulePermission(BasePermission):
    '''
    ModulePermission, 检查一个用户是否有对应某些module的权限

    APIView需要实现module_perms属性:
        type: list
        example: ['information.information', 'school.school']

    权限说明:
        1. is_superuser有超级权限
        2. 权限列表请在api.models.Permission的class Meta中添加(请不要用数据库直接添加)
        3. 只要用户有module_perms的一条符合结果即认为有权限, 所以module_perms是or的意思
    '''

    authenticated_users_only = True

    def has_perms(self, user, perms):
        user_perms = user.get_all_permissions()
        for perm in perms:
            if perm in user_perms:
                return True
        return False

    def get_module_perms(self, view):
        return ['ims_fa.{}'.format(perm) for perm in view.module_perms]

    def has_permission(self, request, view):
        '''
        is_superuser用户有上帝权限，测试的时候注意账号
        '''
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        # is_superuser用户有上帝权限

        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
        else:
            queryset = getattr(view, 'queryset', None)

        assert queryset is not None, (
            'Cannot apply DjangoModelPermissions on a view that '
            'does not set `.queryset` or have a `.get_queryset()` method.'
        )

        if request.user.is_superuser:
            return True

        if getattr(view, '_ignore_model_permissions', False):
            return True
        return (
            request.user and
            (request.user.is_authenticated() or not self.authenticated_users_only)
            and self.has_perms(request.user, self.get_module_perms(view))
        )


def create_records(sender, instance, created=False, *args, **kwargs):
    if not created and instance.merchant_id:
        from .models import ConsumeRecords, Merchants
        before_minus = Merchants.objects.get(pk=instance.merchant_id).money_balance
        if instance.money_balance != before_minus:
            records=ConsumeRecords()
            records.merchant_id=instance
            records.merchant_name=instance.realname
            records.pay_type = 2
            if before_minus>instance.money_balance:
                records.income = Decimal('0.00')
                records.expense=before_minus-instance.money_balance
                records.remark='发单扣款'
            else:
                income =instance.money_balance-before_minus
                records.income = income
                records.expense = Decimal('0.00')
                records.remark = '充值 %s' % income
            records.balance = instance.money_balance
            records.createtime=datetime.timestamp(datetime.now())
            records.operator_id=instance.user.id
            records.operator_name=instance.user.username
            records.save()


class FilterPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        assert view.filter_from is not None, "view hasn't attribute `filter_from`"
        assert isinstance(view.filter_from, list), "filter_from must be a list"
        filter_from = getattr(view, 'filter_from')
        conditions = []
        queries = [models.Q(**{lookup: request.user.id}) for lookup in filter_from]
        conditions.append(reduce(operator.or_, queries))
        if request.user.is_authenticated() and view.queryset.filter(reduce(operator.and_,conditions)).exists():
            return True
        else:
            raise PermissionDenied('你无此操作权限')
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class ExpressBase(models.Model):
    ERROR_TYPES = (
        ('遗失', '遗失'),
        ('破损', '破损'),
        ('已退回', '已退回'),
        ('未发出', '未发出'),
        ('已收到', '已收到'),
        ('拦截退回', '拦截退回'),
        ('签收未收', '签收未收'),
        ('虚假签收', '虚假签收'),
        ('未签收', '未签收'),
        ('已签收', '已签收'),
        ('中转中', '中转中'),
    )
    RESAONS = (
        ('错录签收/无法签收', '错录签收/无法签收'),
        ('多件/少件', '多件/少件'),
        ('费用类', '费用类'),
        ('货物错分', '货物错分'),
        ('货物异常', '货物异常'),
        ('货物转同行', '货物转同行'),
        ('拒收退件', '拒收退件'),
        ('客户原因', '客户原因'),
        ('拦截件', '拦截件'),
        ('盲区件', '盲区件'),
        ('派送异常', '派送异常'),
        ('网点异常', '网点异常'),
        ('特殊派送时效', '特殊派送时效'),
        ('遗失/破损', '遗失/破损'),
        ('已催未派', '已催未派'),
        ('以收未签', '以收未签'),
        ('自提件', '自提件'),
        ('其他', '其他'),
    )
    number = models.BigIntegerField(unique=True, verbose_name='运单号')
    orig = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='发件网点'
    )
    start_time = models.DateTimeField(verbose_name='开单时间')
    status = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='运单状态'
    )
    detail = models.TextField(
        max_length=1000, blank=True, null=True, verbose_name='客户诉求'
    )
    detail_time = models.DateTimeField(
        null=True, blank=True, verbose_name='诉求提交时间'
    )
    error_type = models.CharField(
        max_length=20,
        blank=True, null=True,
        choices=ERROR_TYPES,
        verbose_name='异常类型'
    )
    progess = models.TextField(
        max_length=500, blank=True, null=True, verbose_name='解决进展'
    )
    progess_time = models.DateTimeField(
        null=True, blank=True, verbose_name='回复时间'
    )
    resaon = models.CharField(
        max_length=500,
        blank=True, null=True,
        choices=RESAONS,
        verbose_name='未解决原因'
    )
    end_time = models.DateTimeField(
        blank=True, null=True,  verbose_name='完结时间'
    )
    priority = models.IntegerField(default=0, editable=False)

    class Meta:
        abstract = True


class Express(ExpressBase):
    follower = models.ForeignKey(
        User,
        related_name='express_set',
        limit_choices_to={'is_superuser': False},
        verbose_name='跟进人'
    )

    def __str__(self):
        return '{0}'.format(self.number)

    class Meta(ExpressBase.Meta):
        verbose_name = '运单管理'
        verbose_name_plural = '运单管理'
        ordering = ['-priority', '-start_time']
        permissions = (
            ('change_detail', '只允许修改需求,用于客户帐号'),
            ('change_follower', '只允许修改跟进相关，用于跟单帐号'),
        )


class ExpressArchive(ExpressBase):
    follower = models.ForeignKey(
        User,
        related_name='expressarchive_set',
        verbose_name='跟进人'
    )
    message = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='留言'
    )
    msg_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='留言完成时间'
    )

    def __str__(self):
        return '{0}'.format(self.number)

    class Meta(ExpressBase.Meta):
        verbose_name = '历史运单'
        verbose_name_plural = '历史运单'
        ordering = ['-end_time', 'message']
        permissions = (
            ('change_time', '编辑留言时间，用于跟单帐号'),
            ('change_msg', '编辑留言，用于客户帐号')
        )
        default_permissions = ('add', 'change', 'delete')

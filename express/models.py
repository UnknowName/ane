# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class ExpressBase(models.Model):
    ERROR_TYPES = (
        ('miss', '遗失'),
        ('break', '破损'),
        ('back', '已退回'),
        ('nosend', '未发出'),
        ('received', '已收到'),
        ('rollback', '拦截退回'),
        ('notreceived', '签收未收'),
        ('false_recevied', '虚假签收'),
        ('not_recevied', '未签收'),
        ('recevied', '已签收'),
        ('loading', '中转中'),
    )
    RESAONS = (
        ('error_received', '错录签收/无法签收'),
        ('wrong_count', '多件/少件'),
        ('cost', '费用类'),
        ('wrong_allot', '货物错分'),
        ('error_goods', '货物异常'),
        ('goods_exchange', '货物转同行'),
        ('deny', '拒收退件'),
        ('client', '客户原因'),
        ('break', '拦截件'),
        ('no_sender', '盲区件'),
        ('error_sender', '派送异常'),
        ('error_sites', '网点异常'),
        ('time_over', '特殊派送时效'),
        ('miss', '遗失/破损'),
        ('notify', '已催未派'),
        ('received_later', '以收未签'),
        ('self', '自提件'),
        ('other', '其他'),
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

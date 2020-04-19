from django.db import models

class CommonModels(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')
    update_at = models.DateTimeField(null=True, auto_now=True, help_text='更新时间', verbose_name='更新时间')
    delete_at = models.DateTimeField(null=True, help_text='删除时间', verbose_name='删除时间')

    class Meta:
        abstract = True
        verbose_name = 'Common'
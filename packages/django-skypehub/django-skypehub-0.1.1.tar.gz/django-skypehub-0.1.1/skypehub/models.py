# coding: utf-8
from django.db import models

class Message(models.Model):
    body = models.TextField(u'本文')
    sender = models.CharField(u'送信者', max_length=200)
    chat_name = models.CharField(u'チャット名', max_length=100)
    ctime = models.DateTimeField(u'作成日時', auto_now_add=True)

    def __unicode__(self):
        return self.body

    class Meta:
        ordering = ('-ctime',)
        verbose_name = u'スカイプメッセージ'
        verbose_name_plural = u'スカイプメッセージ'

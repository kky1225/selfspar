from django.db import models


class Project(models.Model):
    """점검할 내 서비스 하나. 예: investfeed"""

    # 이름으로 서비스를 구분하므로 중복을 막는다.
    name = models.CharField('이름', max_length=100, unique=True)
    description = models.TextField('설명', blank=True)
    stack = models.CharField('기술 스택', max_length=200, blank=True)
    created_at = models.DateTimeField('등록일', auto_now_add=True)

    class Meta:
        verbose_name = '프로젝트'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

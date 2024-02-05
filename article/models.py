from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown


class Avatar(models.Model):
    objects = models.Manager()

    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Tag(models.Model):
    objects = models.Manager()

    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text


class Category(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class Article(models.Model):
    objects = models.Manager()

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')

    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='articles')

    # 标题图
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        return md_body, md.toc

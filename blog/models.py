from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

from read_statistics.models import ReadNum, ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    # id = models.IntegerField(primary_key=True, max_length=10)
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, related_name='blog_blog')
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return '<Blog: %s>' % self.title

    class Meta:
        ordering = ['-created_time']


# class ReadNum(models.Model):
#     read_num = models.IntegerField(default=0)
#     blog = models.OneToOneField(Blog, on_delete=models.CASCADE)

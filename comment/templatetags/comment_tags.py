from django import template
from django.contrib.contenttypes.models import ContentType

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


# 第一次使用该功能需重启服务器
@register.simple_tag()
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag()
def get_comment_form(obj):
    blog_content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type': blog_content_type.model,
                                'object_id': obj.pk,
                                'reply_comment_id': 0})
    return form


@register.simple_tag()
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')


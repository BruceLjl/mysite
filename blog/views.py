from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from blog.models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10页进行分页
    page_num = request.GET.get('page', 1)  # 获取URL的页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取对应博客分类的数量 或 BlogType.objects.annotate(blog_count=Count('blog_blog'))
    # blog_types = BlogType.objects.all()
    # blog_type_list = []
    # for blog_type in blog_types:
    #     blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    #     blog_type_list.append(blog_type)

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'day', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month,
                                         created_time__day=blog_date.day).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = Blog.objects.all()
    context['page_of_blogs'] = page_of_blogs
    context['blogs_count'] = Blog.objects.all().count()
    context['page_range'] = page_range
    context['blogs_types'] = BlogType.objects.annotate(blog_count=Count('blog_blog'))
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()

    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    # if not request.COOKIES.get('blog_%s_read' % blog.pk):
    #     ct = ContentType.objects.get_for_model(Blog)
    #     if ReadNum.objects.filter(content_type=ct, object_id=blog.pk):
    #         readnum = ReadNum.objects.get(content_type=ct, object_id=blog.pk)
    #     else:
    #         readnum = ReadNum(content_type=ct, object_id=blog.pk)
    #     readnum.read_num += 1
    #     readnum.save()

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    # context['login_form'] = LoginForm()
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month, day):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month, created_time__day=day)

    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blogs_with_date.html', context)
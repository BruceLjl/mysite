import datetime

from read_statistics.models import ReadNum, ReadDetail
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
        #     readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        # else:
        #     readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
        readDetail, created1 = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key
    # if not request.COOKIES.get(key):
    #     #  总阅读数
    #     readnum = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
    #     readnum.read_num += 1
    #     readnum.save()
    #
    #     # 每日阅读数
    #     date = timezone.now().date()
    #     readDetail = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
    #     readDetail.read_num += 1
    #     readDetail.save()


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]


# def get_7_days_hot_data(content_type):
#     today = timezone.now().date()
#     date = today - datetime.timezone(days=7)
#     read_details = ReadDetail.objects\
#                              .filter(content_type=content_type, date__lt=today, date__gte=date)\
#                              .values('content_type', 'object_id')\
#                              .annotate(read_num_sum=Sum('read_num'))\
#                              .order_by('-read_num_sum')
#     return read_details[:7]


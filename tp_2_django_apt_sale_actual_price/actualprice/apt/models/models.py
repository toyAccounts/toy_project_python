from django.db import models

# Create your models here.

class AptInfo(models.Model):
    region_code = models.PositiveIntegerField(max_length=10, verbose_name="시도명 코드")
    city_code = models.PositiveIntegerField(max_length=10, verbose_name="도시명 코드", null=True)
    apt_name = models.TextField(max_length=30, verbose_name="아파트 명")
    address_normal = models.TextField(verbose_name="주소(일반)")
    address_road = models.TextField(verbose_name="주소(도로명)")
    building_no = models.CharField(max_length=10, verbose_name="동 번호")
    floor = models.PositiveIntegerField(verbose_name="층수")
    price = models.CharField(max_length=30, verbose_name="가격")
    begin_date = models.CharField(max_length=10, verbose_name="시작일")
    end_date = models.CharField(max_length=10, verbose_name="종료일")
    lon = models.FloatField(verbose_name="위도")
    lat = models.FloatField(verbose_name="경도")



from django.db import models

# Create your models here.

class AptInfo(models.Model):
    address_normal = models.TextField(verbose_name="주소(일반)")
    address_road = models.TextField(verbose_name="주소(도로명)")
    building_no = models.PositiveIntegerField(verbose_name="동 번호")
    floor = models.PositiveIntegerField(verbose_name="층수")
    price = models.PositiveBigIntegerField(verbose_name="가격")

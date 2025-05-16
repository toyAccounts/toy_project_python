from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
##### 신규 생성 ##################################################
class PayPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

##### 기존 장고 테이블 수정 ##################################################
# 방법 1) 1개 테이블에 데이터 쌓임
class Users(AbstractUser):
    full_name = models.CharField(max_length=100, null=True)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True, blank=True)

# 방법 2) 2개 테이블에 데이터 쌓임
# class UserDetail(models.Model):
#     user = models.OneToOneField(Users, on_delete=models.CASCADE)
#     pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING)
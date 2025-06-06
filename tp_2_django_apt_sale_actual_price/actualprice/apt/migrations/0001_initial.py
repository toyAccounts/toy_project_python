# Generated by Django 5.2.1 on 2025-05-21 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AptInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "region_code",
                    models.PositiveIntegerField(max_length=10, verbose_name="시도명 코드"),
                ),
                (
                    "city_code",
                    models.PositiveIntegerField(
                        max_length=10, null=True, verbose_name="도시명 코드"
                    ),
                ),
                ("apt_name", models.TextField(max_length=30, verbose_name="아파트 명")),
                ("address_normal", models.TextField(verbose_name="주소(일반)")),
                ("address_road", models.TextField(verbose_name="주소(도로명)")),
                ("building_no", models.CharField(max_length=10, verbose_name="동 번호")),
                ("floor", models.PositiveIntegerField(verbose_name="층수")),
                ("price", models.CharField(max_length=30, verbose_name="가격")),
                ("begin_date", models.CharField(max_length=10, verbose_name="시작일")),
                ("end_date", models.CharField(max_length=10, verbose_name="종료일")),
                ("lon", models.FloatField(verbose_name="위도")),
                ("lat", models.FloatField(verbose_name="경도")),
            ],
        ),
    ]

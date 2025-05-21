from django.urls import path
from apt import views as v

urlpatterns = [
    path("main", v.get_region_all),
    path("get-citys", v.get_city_all),
    path("search", v.search),
    path('download', v.download_excel, name='download_excel'),
]

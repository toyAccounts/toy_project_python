from django.urls import path
from apt import views as v

urlpatterns = [
    path("main", v.apt_main),
    path("get-citys", v.city_list),
    path("search", v.search)
]

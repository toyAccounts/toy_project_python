from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from typing import TypeVar
from apt import settings
from apt.services.molit import Molit
from apt.models.dataclasses import SearchRegionInfo, SearchCityInfo, SearchInfo, MapConfig, Region
from apt.config.logging_config import init_logging
import logging
import json
from django.db.models.query import QuerySet
from apt.models.models import AptInfo
from apt.services.map_service import MapService
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
import matplotlib

# setting
T = TypeVar('T')
molit = Molit()
map_service = MapService(MapConfig(15, "OpenStreetMap"))
matplotlib.use('Agg')


# setting
# 폰트
plt.rc('font', family = "Malgun Gothic")
# 음수
plt.rc("axes", unicode_minus=False)

# logging
init_logging()
logger = logging.getLogger(__name__)


# Create your views here.
def apt_main(request: HttpRequest):
    '''
        메인
    '''

    # 시도 목록
    regions:list[dict[Region]] = molit.region_info

    return render(request, "main.html", {"regions": regions})

def city_list(request: HttpRequest):
    '''
        도시(시군구) 조회
    '''

    # 1. parse
    region_info:SearchRegionInfo = convert_req_to_info(request, "region_info", SearchRegionInfo)

    # 2. 검증
    if(region_info is None): return

    # 3. 도시 목록 조회
    # 코드 앞 2자리만 사용
    citys = molit.fetch_city_info(int(region_info.signguCode[:2]))

    return render(request, "partials/city_options.html", {"citys": citys})

def search(request: HttpRequest):
    '''
        검색
    '''

    # 0. 준비사항
    region_info:SearchRegionInfo = convert_req_to_info(request, "region_info", SearchRegionInfo)
    city_info:SearchCityInfo = convert_req_to_info(request, "city_info", SearchCityInfo)
    begin_date: str = request.GET.get("begin")
    end_date: str = request.GET.get("end")

    # 1. 검증
    if(region_info is None or city_info is None): return render(request, 'main.html')

    # 2. 검색 정보 생성
    search_info:SearchInfo = SearchInfo(region_info, city_info, begin_date, end_date)

    # 3. DB 확인
    search_result:QuerySet = AptInfo.objects.filter(region_code = search_info.region.signguCode,
                                                    city_code = search_info.city.signguCode,
                                                    begin_date = search_info.begin_date,
                                                    end_date = search_info.end_date)
    
    df_search_result:pd.DataFrame | None = None

    # 신규
    if(search_result.exists() is False):
        # 4. DB 저장
        molit.csv_download_save(search_info)

        
    df_search_result = pd.DataFrame.from_records(search_result.values())

    df_search_result['price'] = df_search_result['price'].str.replace(",", "").astype(int)
    df_sorted_search_result:pd.DataFrame = df_search_result.sort_values(by="price", ascending=False)

    map_html = map_service.get_map_html(df_sorted_search_result)

    # 데이터프레임을 HTML 테이블로 변환
    table_html = df_sorted_search_result.to_html(classes='table table-striped')

    # 차트 생성
    fig, ax = plt.subplots()
    ax.barh(df_sorted_search_result['apt_name'], df_sorted_search_result['price'])
    ax.set_title('아파트별 가격')
    ax.set_xlabel('price')
    ax.set_ylabel('apt_name')

    # 차트를 이미지로 변환하여 HTML에 포함
    buffer = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)
    # chart_image = buffer.getvalue()

    buffer.seek(0)

    # base64 인코딩
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)  # 메모리 누수 방지

    context = {
            'map': map_html,
            'table': table_html,
            'chart': image_base64,
            "regions": molit.region_info,
            "search_info": search_info
        }
    return render(request, 'main.html', context)


def convert_req_to_info(request: HttpRequest, key: str, convert_type:T) -> T | None:
    '''
        req -> info 변환
    '''
    # 1. 키 조회
    req_info:str = request.GET.get(key)

    # 2. 검증
    if(req_info == ""): return None

    # 3. parse
    parse_req_info:dict = json.loads(req_info)

    # 4. instance 생성 (convert)
    convert_req_info:T = convert_type(**parse_req_info)

    return convert_req_info
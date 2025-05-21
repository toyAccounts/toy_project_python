import json
from urllib.parse import quote
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from typing import TypeVar
from apt.models.dataclasses import SearchRegionInfo, SearchCityInfo, SearchInfo, GlobalException
from apt.config.logging_config import init_logging
from apt.services.apt_info_service import AptInfoService
from apt.utils.date_util import DateUtil


# setting
T = TypeVar('T')

# logging
init_logging()

# Create your views here.
def get_region_all(request: HttpRequest):
    '''
        지역(시도) 조회
    '''

    # 지역 조회
    regions = AptInfoService.get_region_all()
    return render(request, "main.html", {"regions": regions})

def get_city_all(request: HttpRequest):
    '''
        도시(시군구) 조회
    '''

    # 0. 준비사항
    search_region_info:SearchRegionInfo = convert_req_to_info(request, "region_info", SearchRegionInfo)
    
    # 1. 검증
    if(search_region_info is None): return

    # 1. 도시 조회
    # 코드 앞 2자리만 사용
    citys = AptInfoService.get_city_all(int(search_region_info.signguCode[:2]))
    return render(request, "partials/city_options.html", {"citys": citys})

def search(request: HttpRequest):
    '''
        검색
    '''

    # 0. 준비사항
    region_info:SearchRegionInfo = convert_req_to_info(request, "region_info", SearchRegionInfo)
    city_info:SearchCityInfo = convert_req_to_info(request, "city_info", SearchCityInfo)
    begin_date: str = request.GET.get("begin_date")
    end_date: str = request.GET.get("end_date")

    # 1. 검증
    if(region_info is None):
        return render(request, 'main.html', {"exception": GlobalException(message="지역(시도)을 선택하세요.")})
    if(DateUtil.get_diff_days(begin_date, end_date) > DateUtil.MAX_DIFF_DAY):
        return render(request, 'main.html', {"exception": GlobalException(message="시작일과 종료일은 1년이하로 검색하세요.")})
    if(city_info is None): city_info = SearchCityInfo("", "")

    # 2. 검색 정보 생성
    search_info:SearchInfo = SearchInfo(region_info, city_info, begin_date, end_date)

    # 3. response
    response = AptInfoService.search(search_info)
    return render(request, 'main.html', response)


def download_excel(request: HttpRequest):
    '''
        excel 다운로드
    '''
    # 0. 준비사항
    region_info:SearchRegionInfo = convert_req_to_info(request, "region_info", SearchRegionInfo)
    city_info:SearchCityInfo = convert_req_to_info(request, "city_info", SearchCityInfo)
    begin_date: str = request.GET.get("begin_date")
    end_date: str = request.GET.get("end_date")

     # 1. 검증
    if(region_info is None): return render(request, 'main.html')
    if(city_info is None): city_info = SearchCityInfo("", "")

    # 2. 검색 정보 생성
    search_info:SearchInfo = SearchInfo(region_info, city_info, begin_date, end_date)

    # 3. 검색
    excel_byte = AptInfoService.download_excel(search_info)

    # 4. 엑셀 다운로드 설정
    filename:str = f'{search_info.region.ctprvnNm}_{search_info.city.signguNm}_{search_info.begin_date}_{search_info.end_date}'
    response = HttpResponse(excel_byte, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(filename)}.xlsx'

    return response


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
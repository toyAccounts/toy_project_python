
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
import requests
import os
import io

from apt import settings
from apt.services.molit import Molit


molit = Molit()

# csv 다운로드
def csv_download_save(region_id:int, city_id: int):
    print(f'region_id: {region_id} / city_id: {city_id} / settings.APT_DATA_PATH: {settings.APT_DATA_PATH}')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    cookies = {
        "JSESSIONID": "pMdtNm0hLcTAbp-pXyM7gAhdAJYzwX7NUIorkwoF.RT_DN10",
        "WMONID": "MI9m58xffEn"
    }

    payload = {
        "srhSidoCd": region_id,
        "srhSggCd": "" if city_id is None else city_id,
        "srhThingNo": "A", # 설명 > 실거래 구분 (A: 아파트, B: 연립다세대, ...)
        "srhFromDt": "2024-01-01", # 설명 > 계약일자 (시작)
        "srhToDt":"2024-12-31", # 설명 > 계약일자 (종료)
        "srhDelngSecd": 1, # 설명 > 실거래 구분 (1: (매매), 2: (전월세), ...)

        "sidoNm": "인천광역시", # 설명 > 시도
        "sggNm": "강화군", # 설명 > 시군구
        # "emdNm": "전체1",
        "loadNm": "전체2",  # 설명 > 도로명
        "areaNm": "전체3", # 설명 > 면적
        # "hsmpNm": "전체4",
        "srhFromAmount": "",
        "srhToAmount": ""
    }

    response = requests.post(molit.MOLIT_URL_DOWN_CSV,
                             headers=headers,
                             cookies=cookies,
                             data=payload,
                             stream=True)

    if response.status_code == 200:
        
        # test
        cnt = 1
        for line in response.iter_lines(decode_unicode=True):
            if line and cnt > 100 and cnt < 110:
                print(line.decode('cp949'))
            cnt+=1


        file_name = "downloaded_file.csv"  # 또는 Content-Disposition 헤더에서 추출
        save_path = os.path.join(settings.APT_DATA_PATH, 'downloads', file_name)

        print(f'save_path: {save_path}')

        # 디렉토리 생성
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 파일 저장
        # print(response.content)
        # with open(save_path, 'wb') as f:
        #     f.write(response.content)

            # for chunk in response.iter_content(chunk_size=8192):
            #     if chunk:
            #         f.write(chunk)
    else:
        print(f"파일 다운로드 실패: {response.status_code}")
        # raise Exception(f"파일 다운로드 실패: {response.status_code}")


# Create your views here.
def apt_main(request: HttpRequest):

    # 시도 목록
    regions = molit.region_info

    return render(request, "main.html", {"regions": regions})

# 도시(시군구) 조회
def city_list(request: HttpRequest):
    region_id = request.GET.get("region_id")

    # 도시 목록
    citys = molit.fetch_city_info(int(region_id[:2]))
    return render(request, "partials/city_options.html", {"citys": citys})

def search(request: HttpRequest):
    region_id:int = int(request.GET.get('region_id'))
    city_id:int = int(request.GET.get('city_id'))

    # 1. DB 확인

    # 기존

    # 신규
    # 2. 파일 확인

    # 3. 파일 다운로드

    # 4. DB 저장
    csv_download_save(region_id, city_id)
    
    return JsonResponse({"status": "done"})

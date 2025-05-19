import requests
from apt.models.dataclasses import Region, City
import logging
import os
from apt import settings
from apt.models.dataclasses import SearchInfo
from apt.models.models import AptInfo
import pandas as pd
from io import StringIO

from apt.services.data_processor import DataProcessor
from apt.utils.geo_util import GeoUtil

# setting
processor = DataProcessor(GeoUtil())

# logging
logger = logging.getLogger(__name__)


class Molit():
    # 필드
    __slot__ = [

        # set
        "region_info", # 지역(시도) 정보
        "city_info", # 도시(시군구) 정보
        "req_cookie_csv_download", # 요청 쿠키 (csv 다운로드)
        

        # init
        "MOLIT_URL_REGION",
        "MOLIT_URL_CITY",
        "MOLIT_URL_DOWN_CSV"
    ]

    # 생성자
    def __init__(self):
        self.MOLIT_URL_REGION = "https://rt.molit.go.kr/data/sido.do"
        self.MOLIT_URL_CITY = "https://rt.molit.go.kr/data/sgg.do"
        self.MOLIT_URL_DOWN_CSV = "https://rt.molit.go.kr/pt/xls/ptXlsCSVDown.do"
        self.region_info = self.fetch_region_info()


    def fetch_region_info(self) -> list[dict[Region]]:
        '''
            지역(시도) 정보 조회
        '''

        # 1. 조회
        response = requests.get(self.MOLIT_URL_REGION)

        # 2. 조회 결과확인
        if response.status_code == 200:
            data:list[dict[Region]] = response.json()
            return data
        else:
            return []
            

    def fetch_city_info(self, region_id: int) -> list[dict[City]]:
        '''
            도시(시군구) 정보 조회
        '''

        # 0. 준비사항
        payload = {
            "signguCode": region_id
        }

        # 1. 조회
        try:
            response = requests.post(self.MOLIT_URL_CITY, data=payload)
            response.raise_for_status()
            data:list[dict[City]] = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return []
        
    def fetch_cookie_for_csv_download(self):
        '''
            쿠키 정보 조회
        '''
        response = requests.get(self.MOLIT_URL_DOWN_CSV)

        # 쿠키 키: JSESSIONID, WMONID
        self.req_cookie_csv_download = response.cookies


    def csv_download_save(self, search_info:SearchInfo):
        '''
            csv 다운로드
        '''

        # 0. 준비사항
        # 0.1 헤더 설정
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # 1. payload 설정
        payload = {
            "srhSidoCd": "" if search_info.region.signguCode == "" else search_info.region.signguCode,
            "srhSggCd": "" if search_info.city.signguCode == "" else search_info.city.signguCode,
            "srhThingNo": "A", # 설명 > 실거래 구분 (A: 아파트, B: 연립다세대, ...)
            "srhFromDt": search_info.begin_date, # 설명 > 계약일자 (시작)
            "srhToDt":search_info.end_date, # 설명 > 계약일자 (종료)
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

        # 2. 쿠키 조회
        self.fetch_cookie_for_csv_download()

        # 3. url 호출
        response = requests.post(self.MOLIT_URL_DOWN_CSV,
                                headers=headers,
                                cookies=self.req_cookie_csv_download,
                                data=payload,
                                stream=True)

        # 4. 저장
        if response.status_code == 200:
            
            '''
            # 4.1 파일명 설정
            file_name = f"{search_info.region.ctprvnNm}_{search_info.city.signguNm}_{search_info.begin_date}_{search_info.end_date}.csv"

            # 4.2 저장 경로 설정
            save_path = os.path.join(settings.APT_DATA_PATH, 'downloads', file_name)

            print(f'save_path: {save_path}')

            # 4.3 디렉토리 생성
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # 4.4 파일 저장
            with open(save_path, 'wb') as f:
                f.write(response.content)
            '''

            # 5. csv -> data frame
            csv_data = StringIO(response.content.decode('cp949'))
            df = pd.read_csv(csv_data, encoding="cp949", sep=",", skiprows=15)

            processor.set_data(df)
            city_df:pd.DataFrame = processor.get_city_df(search_info.city.signguNm)
            
            arrange_city_df:pd.DataFrame = city_df[["주소", "도로명", "단지명", "동", "층", "거래금액(만원)", "위도", "경도"]].copy()

            arrange_city_df = arrange_city_df.rename(columns = {"주소": "address_normal",
                                                      "도로명": "address_road",
                                                      "단지명": "apt_name",
                                                      "동": "building_no",
                                                      "층": "floor",
                                                      "거래금액(만원)": "price",
                                                      "위도": "lon",
                                                      "경도": "lat"
                                                    })

            arrange_city_df = arrange_city_df.dropna(subset=['lon', 'lat'])

            apt_infos:list[AptInfo] = [
                AptInfo(
                    **row,
                    region_code = search_info.region.signguCode,
                    city_code = search_info.city.signguCode,
                    begin_date = search_info.begin_date,
                    end_date = search_info.end_date,
                )
                for _, row in arrange_city_df.iterrows()
            ]

            AptInfo.objects.bulk_create(apt_infos, ignore_conflicts=True)

        else:
            print(f"파일 다운로드 실패: {response.status_code}")
            # raise Exception(f"파일 다운로드 실패: {response.status_code}")
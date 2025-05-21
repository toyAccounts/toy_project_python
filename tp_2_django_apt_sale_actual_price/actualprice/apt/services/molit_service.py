import requests
from apt.models.dataclasses import Region, City
import logging
from apt.models.dataclasses import SearchInfo
import pandas as pd
from io import StringIO


# logging
logger = logging.getLogger(__name__)


class MolitService():
    # 필드
    __slot__ = [

        # set
        "city_info", # 도시(시군구) 정보
        "req_cookie_csv_download", # 요청 쿠키 (csv 다운로드)
        

        # init
        "MOLIT_URL_REGION", # 지역(시도) 정보 조회 URL
        "MOLIT_URL_CITY", # 도시(시군구) 정보 조회 URL
        "MOLIT_URL_DOWN_CSV" # CSV 파일 다운로드 URL
        "region_info", # 지역(시도) 정보
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
        try:
            response = requests.get(self.MOLIT_URL_REGION)
            response.raise_for_status()

            # 2. 결과확인
            data:list[dict[Region]] = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"[fetch_region_info] API 요청 실패: {e}")
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

            # 2. 결과확인
            data:list[dict[City]] = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"[fetch_city_info] API 요청 실패: {e}")
            return []
        
    def fetch_cookie_for_csv_download(self):
        '''
            쿠키 정보 조회
        '''

        # 1. 조회
        try:
            response = requests.get(self.MOLIT_URL_DOWN_CSV)
            response.raise_for_status()

            # 2. 쿠키 설정
            # 쿠키 키: JSESSIONID, WMONID
            self.req_cookie_csv_download = response.cookies

        except requests.exceptions.RequestException as e:
            logger.error(f"[fetch_cookie_for_csv_download] API 요청 실패: {e}")
            self.req_cookie_csv_download = None


    def get_df_from_csv_download(self, search_info:SearchInfo) -> pd.DataFrame | None:
        '''
            csv 다운로드

            [참고사항]
            - url을 호출해서 다운로드시 쿠키필요
        '''

        # 0. 준비사항
        # 0.1 헤더 설정
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # 1. payload 설정
        payload = {
            "srhSidoCd": search_info.region.signguCode,
            "srhSggCd": search_info.city.signguCode,
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

        # 3. 조회
        try:
            response = requests.post(self.MOLIT_URL_DOWN_CSV,
                                    headers=headers,
                                    cookies=self.req_cookie_csv_download,
                                    data=payload,
                                    stream=True)
            response.raise_for_status()

            # 4. csv -> data frame
            csv_data:StringIO = StringIO(response.content.decode('cp949'))
            df:pd.DataFrame = pd.read_csv(csv_data, encoding="cp949", sep=",", skiprows=15)

            return df

        except requests.exceptions.RequestException as e:
            logger.error(f"[csv_download_save] API 요청 실패: {e}")
            return None
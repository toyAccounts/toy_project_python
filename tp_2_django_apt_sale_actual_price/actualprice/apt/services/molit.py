import requests


# from apt.models.dataclasses import Region, City

class Molit():
    # 필드
    __slot__ = [

        # set
        "region_info", # 지역(시도) 정보
        "city_info", # 도시(시군구) 정보
        

        # init
        "MOLIT_URL_REGION",
        "MOLIT_URL_CITY",
        "MOLIT_URL_DOWN_CSV"
    ]

    # 생성자
    def __init__(self):
        self.MOLIT_URL_REGION = "https://rt.molit.go.kr/data/sido.do",
        self.MOLIT_URL_CITY = "https://rt.molit.go.kr/data/sgg.do",
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


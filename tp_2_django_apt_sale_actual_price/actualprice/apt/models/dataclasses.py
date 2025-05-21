from dataclasses import dataclass
import pandas as pd
import folium as f

@dataclass
class SearchRegionInfo():
    signguCode: str # 시도 코드
    ctprvnNm: str # 시도명

@dataclass
class SearchCityInfo():
    signguCode: str # 도시 코드
    signguNm: str # 도시명

@dataclass
class SearchInfo():
    region: SearchRegionInfo # 지역정보
    city: SearchCityInfo # 도시정보
    begin_date: str # 시작일
    end_date: str # 종료일

@dataclass
class Region():
    signguCode: str # 시도 코드
    emdCode: str
    ctprvnNm: str # 시도명

@dataclass
class City(Region):
    signguNm: str # 도시명


@dataclass
class CityInfo:
    city_name: str # 도시명
    city_df: pd.DataFrame # 도시 dataFrame
    address_max_price_df: pd.DataFrame # 주소별 최대 가격 dataFrame

    def __init__(self, city_name:str, city_df: pd.DataFrame):
        self.city_name = city_name
        self.city_df = city_df

@dataclass
class LOCATION:
    address: str # 주소
    lat: float # 위도
    lon: float # 경도 

@dataclass
class MapConfig:
    zoom_start: int # 확대 크기
    tiles: f.TileLayer # 지도 타일


@dataclass
class GlobalException:
    message: str # 에러 메시지
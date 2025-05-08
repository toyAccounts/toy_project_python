from dataclasses import dataclass
from typing import Optional
import pandas as pd
import folium as f

@dataclass
class CityInfo:
    city_name: str # 도시명
    city_df: pd.DataFrame # 도시 dataFrame
    address_max_price_df: pd.DataFrame # 주소별 최대 가격 dataFrame

    def __init__(self, city_name:str, city_df: pd.DataFrame):
        self.city_name = city_name
        self.city_df = city_df

@dataclass
class MapConfig:
    zoom_start: int # 확대 크기
    tiles: f.TileLayer # 지도 타일

@dataclass
class FileInfo:
    file_name: str # 파일명
    folder_path: Optional[str] # 파일경로

@dataclass
class CSVFileInfo(FileInfo):
    encoding: str # 인코딩 방식
    sep: Optional[str] # 분할기호
    skiprows: Optional[int] # 건너뛸 행(row) 수

@dataclass
class JSONFileInfo(FileInfo):
    encoding: str = "utf-8" # 인코딩 방식

@dataclass
class LOCATION:
    address: str # 주소
    lat: float # 위도
    lon: float # 경도 
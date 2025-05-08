import pandas as pd
import folium as f
from models.dataclasses import MapConfig

class MapService:

    # 생성자
    def __init__(self, df:pd.DataFrame, map_config: MapConfig):
        self.df:pd.DataFrame = df
        self.map_config = map_config
        self.map:f.Map = self.initMap()
    
    # 초기화
    def initMap(self):

        # 0. 준비사항
        required_cols = ['위도', '경도']

        # 1. 검증
        if not all(col in self.df.columns for col in required_cols): return

        # 2. 위도, 경도 조회
        lat_df = self.df["위도"]
        lon_df = self.df["경도"]
        lat_validate = lat_df[~lat_df.isna()].copy()
        lon_validate = lon_df[~lon_df.isna()].copy()

        # 2. 위도, 경도 설정 (평균값)
        lat = lat_validate.mean()
        long = lon_validate.mean()

        return f.Map(location=[lat, long],
                     zoom_start=self.map_config.zoom_start,
                     tiles=self.map_config.tiles)


    # 마크 표시
    def __mark_to_map(self):
        for index, rowSeries in self.df.iterrows():
            # 0. 준비사항
            lat:float = rowSeries["위도"]
            lon:float = rowSeries["경도"]
            mark = f'[{rowSeries["시군구"]}][{rowSeries["단지명"]}] {rowSeries["거래금액(만원)"]}'

            # 1. 검증
            # 위도, 경도가 없는 경우 제외
            if((pd.isna(lat)) | (pd.isna(lon))): continue
            
            # 2. map에 표시
            f.Marker([lat, lon], tooltip=mark).add_to(self.map)


    # 브라우저 표시
    def show_browser(self):

        # 1. 마크 표시
        self.__mark_to_map()

        # 2. 브라우저 표시
        self.map.show_in_browser() 
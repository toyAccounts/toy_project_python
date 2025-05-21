import pandas as pd
import folium as f
from apt.models.dataclasses import MapConfig

class MapService:

    # 생성자
    def __init__(self, map_config: MapConfig):
        self.map_config = map_config
    
    # map 생성
    def generate_map(self, df: pd.DataFrame):

        # 0. 준비사항
        required_cols = ['lon', 'lat']

        # 1. 검증
        if not all(col in df.columns for col in required_cols): return

        # 2. 위도, 경도 조회
        lat_df = df["lon"]
        lon_df = df["lat"]
        lat_validate = lat_df[~lat_df.isna()].copy()
        lon_validate = lon_df[~lon_df.isna()].copy()

        # 2. 위도, 경도 설정 (평균값)
        lat = lat_validate.mean()
        long = lon_validate.mean()

        return f.Map(location=[lat, long],
                     zoom_start=self.map_config.zoom_start,
                     tiles=self.map_config.tiles)


    # 맵 html 조회
    def get_map_html(self, df: pd.DataFrame):

        # 1. 중복제거
        df = df.drop_duplicates(subset=["lon", "lat"])

        # 2. 맵 생성
        map = self.generate_map(df)

        if(map is None): return

        # 3. 맵에 표시
        for _index, rowSeries in df.iterrows():
            # 3.0 준비사항
            lat:float = rowSeries["lon"]
            lon:float = rowSeries["lat"]
            mark = f'[{rowSeries["apt_name"]}][{rowSeries["address_road"]}] {rowSeries["price"]}'

            # 3.1 검증
            # 위도, 경도가 없는 경우 제외
            if((pd.isna(lat)) | (pd.isna(lon))): continue
            
            # 3.2 map에 표시
            f.Marker([lat, lon], tooltip=mark).add_to(map)

        # 4. html 반환
        return map._repr_html_()

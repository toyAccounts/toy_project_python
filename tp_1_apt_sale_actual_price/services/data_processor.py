import pandas as pd
import numpy as np
from pandas.core.groupby.generic import DataFrameGroupBy
from models.dataclasses import CityInfo, CSVFileInfo, JSONFileInfo
from enums.filename import FileName
from utils.file_util import FileUtil
from utils.geo_util import GeoUtil

class DataProcessor:
    # 필드
    __slots__ = [
                 # set
                 'df_apt_sale_actual_price', # 아파트(매매) 실거래가 dataFrame
                 
                 # init
                 'file_util', # 파일관련 유틸
                 'geo_util', # 위도, 경도관련 유틸
                 'data_folder_path', # data 관련 폴더 경로
                 'city_infos' # 도시 정보
                ]


    # 생성자
    def __init__(self, file_util: FileUtil, geo_util: GeoUtil, data_folder_path: str):
        self.file_util = file_util
        self.geo_util = geo_util
        self.data_folder_path = data_folder_path
        self.city_infos: dict[str, CityInfo] = {}


    # 데이터 설정
    def set_data(self, csv_file_info: CSVFileInfo):
        self.df_apt_sale_actual_price:pd.DataFrame | None = self.file_util.file_load_csv(csv_file_info)


    # 도시 dataFrame 조회
    def get_city_df(self, city_name:str) -> pd.DataFrame:

        # 1. 도시 정보 생성
        self.generate_city_info(city_name)

        # 2. 주소 컬럼 생성
        self.generate_column_address(city_name)

        # 3. 주소별 최대 거래금액 설정
        self.set_address_max_price(city_name)

        # 4. 최대 거래금액의 주소별 위도, 경도 결합
        self.concat_address_max_price_to_lon_lat(city_name)

        return self.city_infos.get(city_name).address_max_price_df


    # 도시 정보 생성
    def generate_city_info(self, city_name:str):

        # 1. 시군구 조회
        region:pd.Series = self.df_apt_sale_actual_price["시군구"]

        # 2. 도시 정보 설정
        self.city_infos.setdefault(city_name, 
                                   CityInfo(city_name=city_name,
                                            city_df=self.df_apt_sale_actual_price[region.str.contains(city_name)].copy()))
    

    # 주소 컬럼 생성
    def generate_column_address(self, city_name:str):

        # 1. 도시 조회
        city_info:CityInfo | None = self.city_infos.get(city_name)

        # 2. 검증
        if(city_info is None): return

        # 3. 도시 dataFrame 조회
        city_df:pd.DataFrame = city_info.city_df

        # 4. 주소 컬럼 생성
        city_df["주소"] = city_df["시군구"] + " " + city_df["번지"]


    # 주소별 최대 거래금액 설정
    def set_address_max_price(self, city_name:str):

        # 1. 도시 조회
        city_info:CityInfo | None = self.city_infos.get(city_name)

        # 2. 검증
        if(city_info is None): return

        # 3. 주소별 최대 거래금액 설정
        city_info.address_max_price_df = self.__get_max_price_group_by_address(city_info.city_df)


    # 주소별 최대 거래금액 조회
    def __get_max_price_group_by_address(self, df:pd.DataFrame):

        # 1. 그룹화
        df_group:DataFrameGroupBy = df.groupby(["주소"])

        # 2. 그룹별 최대금액만 선택
        df_group_max:pd.DataFrame = df.loc[df_group["거래금액(만원)"].idxmax()].copy()

        return df_group_max
    

    # 최대 거래금액의 주소별 위도, 경도 결합
    def concat_address_max_price_to_lon_lat(self, city_name:str):

        # 1. 도시 조회
        city_info:CityInfo | None = self.city_infos.get(city_name)

        # 2. 검증
        if(city_info is None): return

        # 3. 주소의 위도, 경도 생성
        # 3.1 중복 주소 제외
        addresses:np.ndarray = city_info.address_max_price_df["주소"].unique()

        # 3.2 주소별 위도, 경도 생성
        self.geo_util.generate_lon_lat(addresses, self.data_folder_path, city_name)

        # 4. 위도, 경도 결합
        city_info.address_max_price_df = self.__get_df_concat_lon_lat(city_info.address_max_price_df, city_name)
    

    # 위도, 경도 결합 dataFrame 조회
    def __get_df_concat_lon_lat(self, df:pd.DataFrame, city_name: str):

        # 0. 준비사항
        json_info:JSONFileInfo = JSONFileInfo(file_name=f'{city_name}_{FileName.LON_LAT_JSON.value}',
                                              folder_path=self.data_folder_path)

        # 1. json 파일 조회
        lon_lat_data:pd.DataFrame | None = self.file_util.file_load_json(json_info)

        # 2. 검증
        if(lon_lat_data is None): return
        
        # 3. 빈값 제거
        lon_lat_data_unique = lon_lat_data[(~lon_lat_data["lat"].isnull()) & (~lon_lat_data["lon"].isnull())]
        
        # 4. 컬럼명 수정
        lon_lat_data_unique = lon_lat_data_unique.rename(columns={"address": "주소", "lat":"위도", "lon": "경도"})

        # 5. 결합
        return df.merge(lon_lat_data_unique[["주소" ,"위도", "경도"]], on="주소", how="left") 
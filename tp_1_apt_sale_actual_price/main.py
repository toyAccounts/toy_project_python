import os
import pandas as pd
from models.dataclasses import CSVFileInfo, MapConfig
from utils.file_util import FileUtil
from utils.geo_util import GeoUtil
from services.data_processor import DataProcessor
from services.map_service import MapService

def main():

    # 0. 준비사항
    data_folder_path:str = f'{os.path.dirname(os.path.abspath(__file__))}\\data' # 데이터 폴더 경로
    dp:DataProcessor = DataProcessor(FileUtil(), GeoUtil(), data_folder_path) # 프로세서

    # 1. 데이터 설정
    dp.set_data(CSVFileInfo(folder_path=data_folder_path,
                            file_name="아파트(매매)_실거래가_20240101_20241231.csv",
                            encoding="cp949",
                            sep=",",
                            skiprows=15))

    # 2. 도시 데이터 생성
    city_df:pd.DataFrame = dp.get_city_df(city_name="부천시")

    # 3. 맵
    # 3.1 맵 생성
    map = MapService(city_df, MapConfig(15, "OpenStreetMap"))

    # 3.2 브라우저 표시
    map.show_browser()

if __name__ == "__main__":
    main() 
import numpy as np
import pandas as pd
import time
from geopy.geocoders import Nominatim
from models.dataclasses import LOCATION, JSONFileInfo
from enums.filename import FileName
from utils.file_util import FileUtil

class GeoUtil:

    # 생성자
    def __init__(self):
        self.file_util = FileUtil()

    # 위도, 경도 생성
    def generate_lon_lat(self, addresses:np.ndarray, folder_path: str, city_name:str):

        # 0. 준비사항
        json_info:JSONFileInfo = JSONFileInfo(file_name=f'{city_name}_{FileName.LON_LAT_JSON.value}', folder_path=folder_path)

        # 1. json 파일 조회
        lon_lat_json = self.file_util.file_load_json(json_info)

        # 2. 검증
        # json파일 존재시 재생성x
        if(lon_lat_json is not None): return

        # 3. geopy
        # 3.0 준비사항
        locations:list[LOCATION] = []
        geolocator = Nominatim(user_agent="myGeocoder")

        # 3.1 위도, 경도 조회
        for i, addr in enumerate(addresses):
            # 3.1.0 진행률
            progress = (i + 1) / len(addresses) * 100  # 진행률 계산
            print(f"\r다운로드 중: {progress:.2f}% ({i + 1}/{len(addresses)})", end="", flush=True)

            # 3.1.1 위도, 경도 조회
            try:
                location = geolocator.geocode(addr)
                if location:
                    locations.append({
                        "address": addr,
                        "lat": location.latitude,
                        "lon": location.longitude
                    })
                else:
                    locations.append({"address": addr, "lat": None, "lon": None})

                # geopy 호출 간격 조정
                time.sleep(0.1)
            except:
                locations.append({"address": addr, "lat": None, "lon": None})

        # 4. 저장
        self.file_util.file_save_json(pd.DataFrame(locations), json_info) 
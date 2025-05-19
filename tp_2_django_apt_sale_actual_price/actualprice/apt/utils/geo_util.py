import numpy as np
import pandas as pd
import time
from geopy.geocoders import Nominatim
from apt.models.dataclasses import LOCATION

class GeoUtil:

    # 위도, 경도 생성
    def generate_lon_lat(self, addresses:np.ndarray) -> pd.DataFrame:

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
                time.sleep(0.15)
            except:
                locations.append({"address": addr, "lat": None, "lon": None})

        # 4. 반환
        return pd.DataFrame(locations)
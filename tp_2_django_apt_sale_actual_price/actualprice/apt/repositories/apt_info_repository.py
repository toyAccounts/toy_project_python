import pandas as pd
from apt.models.models import AptInfo
from apt.models.dataclasses import SearchInfo
from django.db.models.query import QuerySet

class AptInfoRepository:

    CONVERT_COLUMNS:dict[str, str] = {"주소": "address_normal",
                                      "도로명": "address_road",
                                      "단지명": "apt_name",
                                      "동": "building_no",
                                      "층": "floor",
                                      "거래금액(만원)": "price",
                                      "위도": "lon",
                                      "경도": "lat"}

    @staticmethod
    def search_by_search_info(search_info: SearchInfo):
        search_result:QuerySet = AptInfo.objects.filter(region_code = search_info.region.signguCode,
                                                        city_code = None if search_info.city.signguCode == "" else search_info.city.signguCode,
                                                        begin_date = search_info.begin_date,
                                                        end_date = search_info.end_date)
        return search_result

    @staticmethod
    def save_all(city_df: pd.DataFrame, search_info: SearchInfo):
        
        # 1. df 수정
        arrange_city_df:pd.DataFrame = city_df[list(AptInfoRepository.CONVERT_COLUMNS.keys())].copy()
        arrange_city_df = arrange_city_df.rename(columns = AptInfoRepository.CONVERT_COLUMNS)
        arrange_city_df = arrange_city_df.dropna(subset=['lon', 'lat'])

        # 2. db 저장
        apt_infos:list[AptInfo] = [
            AptInfo(
                **row,
                region_code = search_info.region.signguCode,
                city_code = None if search_info.city.signguCode == "" else search_info.city.signguCode,
                begin_date = search_info.begin_date,
                end_date = search_info.end_date,
            )
            for _, row in arrange_city_df.iterrows()
        ]

        AptInfo.objects.bulk_create(apt_infos, ignore_conflicts=True)
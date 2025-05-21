import pandas as pd
import matplotlib
from apt.services.molit_service import MolitService
from apt.models.dataclasses import Region, City, SearchInfo, MapConfig
from apt.repositories.apt_info_repository import AptInfoRepository
from apt.services.data_processor import DataProcessor
from apt.utils.geo_util import GeoUtil
from apt.services.map_service import MapService
from apt.services.chart_service import ChartService
from apt.services.excel_service import ExcelService


# setting
data_processor = DataProcessor(GeoUtil())
molit = MolitService()
map_service = MapService(MapConfig(12, "OpenStreetMap"))

matplotlib.use('Agg')

class AptInfoService:

    @staticmethod
    def get_region_all() -> list[dict[Region]]:
        '''
            지역(시도) 조회
        '''
         # 시도 목록
        regions:list[dict[Region]] = molit.region_info

        return regions
    
    @staticmethod
    def get_city_all(region_code:int) -> list[dict[City]]:
        '''
            도시(시군구) 조회
        '''
        # 도시 목록 조회
        citys:list[dict[City]] = molit.fetch_city_info(region_code)

        return citys
    
    @staticmethod
    def search(search_info:SearchInfo) -> dict:
        '''
            검색
        '''

        # 0. 준비사항
        df_search_result:pd.DataFrame | None = None

        # 1. DB 확인
        search_result_query_set = AptInfoRepository.search_by_search_info(search_info)
        
        # 1.1 DB 결과가 없는 경우
        if(search_result_query_set.exists() is False):
            # 1.1.1 csv 다운로드 및 df 변환
            df = molit.get_df_from_csv_download(search_info)

            # 1.1.2 df 가공 
            data_processor.set_data(df)
            city_df:pd.DataFrame = data_processor.get_city_df(search_info.city.signguNm)
            
            # 1.1.3 저장
            AptInfoRepository.save_all(city_df, search_info)

        # 2. queryset -> df
        df_search_result:pd.DataFrame = pd.DataFrame.from_records(search_result_query_set.values())

        # 3. df 가공
        df_search_result['price'] = df_search_result['price'].str.replace(",", "").astype(int)
        df_sorted_search_result:pd.DataFrame = df_search_result.sort_values(by="price", ascending=False)

        # 4. response
        # 4.1 map
        map_html = map_service.get_map_html(df_sorted_search_result)

        # 4.2 table
        table_df = df_sorted_search_result[["address_normal", "apt_name", "price"]].copy()
        table_df = table_df.rename(columns={value: key for key, value in AptInfoRepository.CONVERT_COLUMNS.items()})
        table_html = table_df.to_html(classes='table table-striped', index=False)

        # 4.3 chart
        chart_image = ChartService.barh_to_image_base64(data_info={"df": df_sorted_search_result[:10], "x": "price", "y": "apt_name"}, title="Top 가격", label={"x": "가격", "y": "아파트명"})
        
        return {
            'map': map_html,
            'table': table_html,
            'chart': chart_image,
            "regions": molit.region_info,
            "search_info": search_info
        }

    @staticmethod
    def download_excel(search_info:SearchInfo):
        '''
            excel 다운로드
        '''

        # 0. 준비사항
        df_search_result:pd.DataFrame | None = None

        # 1. DB 확인
        search_result_query_set = AptInfoRepository.search_by_search_info(search_info)
        
        # 2. queryset -> df
        df_search_result:pd.DataFrame = pd.DataFrame.from_records(search_result_query_set.values())

        # 3. df 수정
        # 3.1 컬럼명 변경
        df_search_result = df_search_result.rename(columns={value: key for key, value in AptInfoRepository.CONVERT_COLUMNS.items()})

        # 3.2 df 컬럼 설정
        df_search_result = df_search_result[list(AptInfoRepository.CONVERT_COLUMNS.keys())].copy()

        # 3.3 df 인덱스 설정
        df_search_result.index = df_search_result.index + 1

        # 4. df -> excel byte
        excel_byte = ExcelService.download_excel_to_byte(df=df_search_result, sheet_name=f'{search_info.region.ctprvnNm}_{search_info.city.signguNm}')


        return excel_byte
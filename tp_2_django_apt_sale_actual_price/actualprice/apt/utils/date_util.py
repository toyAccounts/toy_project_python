from datetime import datetime

class DateUtil:

    MAX_DIFF_DAY:int = 365 # 최대 사이 일수

    @staticmethod
    def get_diff_days(begin_date_str: str, end_date_str:str):
        '''
            두 날짜 사이의 일수 조회
        '''
        
        # 1. str -> datetime 변환
        begin_date:datetime = datetime.strptime(begin_date_str, "%Y-%m-%d")
        end_date:datetime = datetime.strptime(end_date_str, "%Y-%m-%d")

        # 2. 날짜 차이 계산
        date_diff = abs((end_date - begin_date).days)

        return date_diff
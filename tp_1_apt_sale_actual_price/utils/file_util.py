import os
import pandas as pd
from models.dataclasses import CSVFileInfo, JSONFileInfo

class FileUtil:

    # csv 파일 load
    def file_load_csv(self, file_info: CSVFileInfo) -> pd.DataFrame | None:

        # 1. 파일 경로 설정
        file_path = os.path.join(file_info.folder_path, file_info.file_name)

        # 2. 파일 load
        try:
            return pd.read_csv(file_path,
                               encoding=file_info.encoding,
                               sep=file_info.sep,
                               skiprows=file_info.skiprows)
        except FileNotFoundError:
            print(f'해당 경로에서 파일을 찾을 수 없음 (경로: {file_path})')
            return None
        except Exception as e:
            print(f"파일 로드 오류 발생: {str(e)}")
            return None


    # json 파일 load
    def file_load_json(self, file_info: JSONFileInfo) -> pd.DataFrame | None:

        # 1. 파일 경로 설정
        file_path = os.path.join(file_info.folder_path, file_info.file_name)

        # 2. 파일 load
        try:
            return pd.read_json(file_path, encoding=file_info.encoding)
        except:
            return None


    # json 파일 save
    def file_save_json(self, file: pd.DataFrame, file_info: JSONFileInfo):

        # 1. 파일 경로 설정
        file_path = os.path.join(file_info.folder_path, file_info.file_name)

        # 2. 파일 save
        file.to_json(file_path, orient='records', force_ascii=False) 

import seaborn as sns
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# setting
# 폰트
plt.rc('font', family = "Malgun Gothic")
# 음수
plt.rc("axes", unicode_minus=False)


class ChartService:

    @staticmethod
    def barh_to_image_base64(data_info:dict, title:str, label:dict[str]):
        '''
            data frame -> 이미지 변환
        '''
        
        # 1. 차트 생성
        # fig, ax = plt.subplots()
        # ax.barh(df['apt_name'], df['price'])
        # ax.set_title(title)
        # ax.set_xlabel(label["x"])
        # ax.set_ylabel(label["y"])
        fig = plt.figure(figsize=(8, 4))
        sns.barplot(data=data_info["df"], x=data_info["x"], y=data_info["y"], palette='Set3')
        plt.xlabel(label["x"])
        plt.ylabel(label["y"])
        plt.title(title)
        plt.tight_layout()

        # 2. 차트 -> 이미지
        buffer = BytesIO()
        canvas = FigureCanvas(fig)
        canvas.print_png(buffer)
        buffer.seek(0)
        plt.close(fig)

        # 3. base64 인코딩
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')


        return image_base64
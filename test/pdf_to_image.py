from pdf2image import convert_from_path
import os

# PDF 경로 설정
pdf_path = r'.\data\Python_Doc.pdf'

# Poppler 경로 (환경변수 설정했으면 생략 가능)
poppler_path = r'.\poppler-24.08.0\Library\bin'

# 고급 옵션: 300+ DPI, 이미지 포맷 PNG, 배경 제거, 멀티스레딩 등
images = convert_from_path(
    pdf_path,
    dpi=500,  # 고해상도 (300 이상이면 고품질)
    fmt='png',
    grayscale=False,  # 컬러 유지
    thread_count=4,
    poppler_path=poppler_path
)

# 결과 저장
output_dir = 'converted_images'
os.makedirs(output_dir, exist_ok=True)

for i, image in enumerate(images):
    filename = os.path.join(output_dir, f'page_{i + 1}.png')
    image.save(filename, 'PNG')

print("✅ 고화질 이미지로 변환 완료!")
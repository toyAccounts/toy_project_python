import pathlib
import openpyxl as op
from openpyxl.packaging.core import DocumentProperties
from openpyxl.workbook.protection import WorkbookProtection
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from openpyxl.styles import Protection


################################################## chapter 4. ##################################################
# 경로
path = pathlib.Path(r".\data")

# for path_obj in path.iterdir():
#     if(path_obj.match("*.xlsx")):
for path_obj in path.glob("*.xlsx"):
    # workbook
    wb:op.Workbook = op.load_workbook(path_obj)

    # 시트 이름 목록
    print("시트 목록:", wb.sheetnames)

    # 시트 활성화 조회
    ws:Worksheet = wb.active
    print("활성 시트 이름:", ws.title)

    # 시트 확인
    for sheet_name in wb.sheetnames:

        # 시트 선택
        # 방법 1)
        ws:Worksheet = wb[sheet_name]

        # 방법 2)
        # ws = wb.worksheets[0]

        print(f"\n시트: {sheet_name} / title: {ws.title}")
        print(f' - 시트 상태: {ws.sheet_state}')
        print(" - 데이터 범위:", ws.dimensions)  # 예: A1:E15
        print(" - 최대 행:", ws.max_row)
        print(" - 최대 열:", ws.max_column)

    # 활성 시트 변경
    index:int = wb.sheetnames.index("Sheet5")
    # wb.active = index

    # 속성
    wbp:DocumentProperties = wb.properties
    print(wbp)
    # wbp.creator = "작성자"
    # wbp.title = "제목"
    # wbp.last_modified_by = "최근 수정자"

    # 특정 셀 값
    print(ws["A1"].value)

    # wooksheet 보호
    wb.security = WorkbookProtection(workbookPassword="test",
                                    #  lockStructure=True
                                    lockStructure=False
                                    )

    ################################################## chapter 5. ##################################################
    # 시트 생성
    # wb_new_sheet = wb.create_sheet(title="새로운 시트")

    # 시트명 변경
    # ws = wb["Sheet1"]
    # ws.title = "표222"

    # 시트 삭제
    # wb.remove(ws)


    # 시트 조작
    for ws in wb:
        ws["B2"].value = ws.title

        # 시트 이동시 그룹화 해제
        ws.sheet_view.tabSelected = None


    # 시트 이동
    # offset: 이동하는 수 (양수: 오른쪽 이동 / 음수: 왼쪽 이동)
    # active한 시트 이동시 그룹화 됨
    wb.move_sheet("새로운 시트", offset=-3)


    # 시트 복사
    ws_copy_target:Worksheet = wb.worksheets[1]
    ws_copy = wb.copy_worksheet(ws_copy_target)
    ws_copy.title =f'{ws_copy_target.title}의 복사본'


    # 시트 표시 / 비표시
    ws_copy_target.sheet_state = Worksheet.SHEETSTATE_HIDDEN


    # 시트 보호
    # 입력가능한 셀의 잠금 off -> 시트의 보호 on
    ws_protect_target:Worksheet = wb.worksheets[2]

    for row in ws_protect_target["B2:D6"]:
        
        for cell in row:
            # 1) 셀의 잠금 off
            # cell_protect_target:Cell = ws_protect_target["B2"]
            # cell_protect_target.protection = Protection(locked=False)
            cell.protection = Protection(locked=False)

    # 2) 시트 보호 on
    ws_protect_target.protection.password = "sheet"
    ws_protect_target.protection.enable()


    ################################################## chapter 6. ##################################################

    # 행 추가 (수식범위가 연관된 경우 범위자동수정 안됨)
    ws:Worksheet = wb.active
    print(f'활성화된 시트명: {ws.title}')
    for i, v in enumerate(["D1", "D2", "D3"]):
        cell:Cell = ws[v]
        cell.value = i

    ws["D4"] = "=sum(D1:D3)"
    ws.insert_rows(2) # 2번째 행에 추가

    ws["D5"] = "=sum(D1:D4)" # 관련 수식 수정


    # 행 삭제
    ws.delete_rows(10)


    # 열 추가
    ws.insert_cols(3)

    for row in ws.iter_rows(min_row=2):
        cell:Cell = row[4] # 4 == D
        cell.value = f'=B{row[0].row}*D{row[0].row}' # 수식처리
        # cell.value = row[1].value * row[3].value # 직접 계산

    # 열 삭제
    ws.delete_cols(3)

    # 마지막 열, 행
    print(f'마지막 행: {ws.max_row}, 마지막 열; {ws.max_column}')
    for row in range(1, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            cell: Cell = ws.cell(row, col)
            print(cell.value)


    # 행 높이 맞추기
    # 행번호
    ws.row_dimensions[1].height = 24

    # 열 폭 맞추기
    # 열 이름
    ws.column_dimensions["A"].width = 28

    # 틀고정
    ws.freeze_panes = "B2" # A1 고정
    ws.freeze_panes = "A2" # 행고정 (A2, A3, ...)
    ws.freeze_panes = "B1" # 열고정 (B1, C1, ...)

    # 틀고정 해제
    ws.freeze_panes = "A1"

    # 행 숨김/표시
    ws.row_dimensions[3].hidden = True

    # 열 숨김/표시
    ws.column_dimensions["A"].hidden = True

    # 열 이름 확인
    for col_index in range(3, ws.max_column + 1):
        col_letter = ws.cell(row=1, column=col_index).column_letter # 열 이름
        print(f'col_letter: {col_letter}')
        ws.column_dimensions[col_letter].hidden = False


    ################################################## chapter 7. ##################################################
    # 셀 값
    # 방법 1)
    cell:Cell = ws["C2"]
    cell.value

    # 방법 2)
    # row, column은 모두 1부터 시작
    cell:Cell = ws.cell(row=2, column=3)
    cell.value

    # 셀값 추가
    cell.value = "값"


    # 셀값 범위
    # 방법 1)
    cell_scope:tuple[tuple[Cell, ...], ...] = ws["B2:C6"]

    for row in cell_scope:
        for cell in row:
            print(cell)
    print("-" * 50)

    # 방법 2)
    for row in ws.iter_rows(min_row=2, max_row=6,
                            min_col=2, max_col=3):
        for cell in row:
            print(cell)
    print("-" * 50)
    
    # 방법 3)
    for row_index in range(2, 7):
        for col_index in range(2, 4):
            print(ws.cell(row=row_index, column=col_index))

    print(type(cell_scope))


    # 셀 범위 값 -> 다른 셀 범위에 복사
    mov_row = 5
    mov_col = 4
    for row_index in range(2, 7):
        for col_index in range(2, 4):
            ws.cell(row=(row_index + mov_row),
                    column=(col_index + mov_col)).value = ws.cell(row=row_index, column=col_index).value

    # 행렬 변경
    mov_row = 10
    for row_index in range(2, 7):
        for col_index in range(2, 4):
            ws.cell(row=(col_index + mov_row),
                    column=(row_index)).value = ws.cell(row=row_index, column=col_index).value


    # 다른 시트에 옮겨 적기
    ws_3 = wb.worksheets[3]
    ws_4 = wb.worksheets[4]

    for row in cell_scope:
        for cell in row:
            ws_3.cell(row_index, col_index).value = ws_4.cell(row_index, col_index).value

    # 다른 북에 옮겨 적기
    ws_5 = wb.worksheets[5] # 복사 대상
    wb_new_1 = op.Workbook() # 붙이기 대상
    ws_new_1 = wb_new_1.active

    for row in cell_scope:
        for cell in row:
            ws_new_1.cell(row_index, col_index).value = ws_5.cell(row_index, col_index).value


    print(f"stem: {path_obj.stem} / suffix :{path_obj.suffix}")
    print(type(path_obj)) 
    wb_new_1.save(path_obj.with_name(f'{path_obj.stem}_copy{path_obj.suffix}'))


    ################################################## chapter 8. ##################################################
    # 수치 표시 방식 설정
    ws.cell(1, 2).number_format = "#.##0" # 3자릿수마다 제로 억제




    # 저장
    wb.save(path_obj)

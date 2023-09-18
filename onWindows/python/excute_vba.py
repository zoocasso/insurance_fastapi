import xlwings as xw

def excute_vba(file_name):
    #엑셀 매크로파일 열기(path는 매크로 파일이 있는 경로)
    wb = xw.Book(f"./input_file/{file_name}")

    #엑셀 VBA의 매크로 함수 'test'를 파이썬 함수로 지정
    macro_test = wb.macro('PV_Table_Create')

    #VBA 함수 실행
    macro_test()

    #함수를 실행한 엑셀파일 따로 저장하기
    wb.save(f"./output_file/{file_name}")

    #WorkBook 객체 닫기
    wb.close

if __name__ == "__main__":
    excute_vba("생보사_Test_샘플.xlsm")
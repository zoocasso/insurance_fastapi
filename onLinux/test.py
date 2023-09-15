from openpyxl import load_workbook
import pandas as pd

# xlsx_path = "input_xlsx/sample.xlsx"

# input_xlsx_df = pd.read_excel(xlsx_path, sheet_name = 1)
# input_xlsx_df.columns = input_xlsx_df.iloc[8]
# input_xlsx_df = input_xlsx_df.iloc[9:,2:]

# ACC_PERIOD = 202203
# PORTF = "KGNNPX_PD"
# ACC_PERIOD_TYPE = "Q"
# M_LIAB_ITEM = 2101
# M_ACC_EVENT = 10101

# print(input_xlsx_df[
#     (input_xlsx_df['ACC_PERIOD']==ACC_PERIOD)
#     &(input_xlsx_df['ACC_PERIOD_TYPE']==ACC_PERIOD_TYPE)
#     &(input_xlsx_df['M_LIAB_ITEM']==M_LIAB_ITEM)
#     &(input_xlsx_df['M_ACC_EVENT']==M_ACC_EVENT)
#     ])

test_df = pd.DataFrame({"판매일자":[20220101,20230101],
            "거래처명":['신촌','서초'],
            "돈":[100,200]})

input_str = '=SUMIFS(OFFSET(Data!$O$10,1,0,Data!$C$7,1),OFFSET(Data!$D$10,1,0,Data!$C$7,1),ACC_PERIOD,OFFSET(Data!$E$10,1,0,Data!$C$7,1),ACC_PERIOD_TYPE,OFFSET(Data!$G$10,1,IF(IF(LEFT(L$28,1)="1",원수_PORTF,출재_PORTF)="",-1,0),Data!$C$7,1),IF(IF(LEFT(L$28,1)="1",원수_PORTF,출재_PORTF)="","ALL",IF(LEFT(L$28,1)="1",원수_PORTF,출재_PORTF)),OFFSET(Data!$H$10,1,IF(IF(LEFT(L$28,1)="1",원수_GOC,출재_GOC)="",-2,0),Data!$C$7,1),IF(IF(LEFT(L$28,1)="1",원수_GOC,출재_GOC)="","ALL",IF(LEFT(L$28,1)="1",원수_GOC,출재_GOC)),OFFSET(Data!$J$10,1,IF(LEN(L$28)=4,0,1),Data!$C$7,1),L$28,OFFSET(Data!$L$10,1,IF(LEN($K30)=5,0,1),Data!$C$7,1),$K30)/$F$8'
test_str = '=SUMIFS(C2:C3,OFFSET(A1,1,0,2,1),20220101,OFFSET(B1,1,0,2,1),"신촌")'

def func1(input_str):
    open_cnt = 0
    close_cnt = 0
    new_str = ''
    result_list = list()
    for i in input_str:
        if i == "(":
            open_cnt += 1
        if i == ")":
            close_cnt += 1
        if open_cnt >0:
            new_str += i
        if open_cnt == close_cnt and open_cnt != 0:
            result = new_str.lstrip("(").rstrip(")")
            new_str = ''
            result_list.append(result)
            break
    return result_list

def find_func_name(input_str):
    open_cnt = 0
    new_str = ''
    for i in input_str:
        new_str += i
        if i == "(":
            open_cnt += 1
        if open_cnt == 1:
            break
    return new_str

print(find_func_name(test_str))
print(func1(func1(test_str)))

# =SUMIFS(

#     OFFSET(Data!$O$10,1,0,Data!$C$7,1),

#     OFFSET(Data!$D$10,1,0,Data!$C$7,1),

#     ACC_PERIOD,

#     OFFSET(Data!$E$10,1,0,Data!$C$7,1),

#     ACC_PERIOD_TYPE,

#     OFFSET(Data!$G$10,1,IF(IF(LEFT(L$28,1)="1",원수_PORTF,출재_PORTF)="",-1,0),Data!$C$7,1),

#     IF(IF(LEFT(L$28,1)="1",원수_PORTF,출재_PORTF)="","ALL",IF(LEFT(L$28,1)="1",원수_PORTF,출재_PORTF)),

#     OFFSET(Data!$H$10,1,IF(IF(LEFT(L$28,1)="1",원수_GOC,출재_GOC)="",-2,0),Data!$C$7,1),

#     IF(IF(LEFT(L$28,1)="1",원수_GOC,출재_GOC)="","ALL",IF(LEFT(L$28,1)="1",원수_GOC,출재_GOC)),

#     OFFSET(Data!$J$10,1,IF(LEN(L$28)=4,0,1),Data!$C$7,1),L$28,OFFSET(Data!$L$10,1,IF(LEN($K30)=5,0,1),Data!$C$7,1),

#     $K30)

#     /$F$8
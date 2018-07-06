import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from collections import OrderedDict
import datetime

def build_worksheet(workbook, name, records):
    worksheet = workbook.add_worksheet(name)
    cells = OrderedDict([
        ('STOCK', ('Stock', None)),
        ('CURRENT_PRICE', ('Current price', None)),
        ('DATE', ('Date', None)),
        ('TYPE', ('Type', None)),
        ('AMOUNT', ('Amount', None)),
        ('PRICE', ('Price paid', None)),
        ('FEES', ('Fees', None)),
        ('TOTAL_PRICE', ('Total price', '={PRICE}*{AMOUNT}')),
        ('TOTAL_W_FEE', ('Total price (+fee)', '={TOTAL_PRICE}+IF({TYPE}<>"CASH",{FEES},0)')),
        ('DIV_YIELD', ('Dividend yield', '=IF({TYPE}<>"CASH", W2/{AMOUNT} + IF({TYPE}="DIV", 0, AA2/{TOTAL_PRICE}), "")')),
        ('CAP_GAIN', ('Capital gain', '=IF({TYPE}<>"BUY","",({CURRENT_PRICE}-{PRICE})/{PRICE})')),
        ('GROSS_PROFIT', ('Gross profit', '=IF({TYPE}<>"BUY", "", (({AMOUNT}+W2)*{CURRENT_PRICE} - {TOTAL_PRICE} + AA2)/{TOTAL_PRICE})')),
        ('NET_PROFIT', ('Net profit', '=IF({TYPE}<>"BUY", "", (({AMOUNT}+W2)* {CURRENT_PRICE}-{TOTAL_W_FEE}+AA2)/{TOTAL_W_FEE})')),
        ('ANNUALIZED', ('Annual profit', '=IF({TYPE}<>"BUY","",((M2+1)^(1/((TODAY()-{DATE})/365))-1))')),
        ('TOTAL_VALUE', ('Total value', None)), # =E11 * $B$2
        ('GROSS_GAIN', ('Gross gain', None)), # =O2-H11+AB6
        ('NET_GAIN', ('Net gain', None)), # =(O2-I11)+AB6
        ('__BLANK__', ('', None)),
        ('SHARE_RUNNING', ('Share running total', '=SUM({AMOUNT_ZERO}:{AMOUNT})')),
        ('PREV_RUNNING', ('Previous running total', '={SHARE_RUNNING}-{AMOUNT}')),
        ('DIV_PER_SHARE', ('Dividends per share', '=IF({TYPE}="DIV",{AMOUNT}/{PREV_RUNNING},0)')),
        ('TOT_DIV_PER_SHARE', ('Total dividends per share', '=IF(ROW()>={FINAL_ROW}, 0, SUM(INDIRECT(ADDRESS(ROW({DIV_PER_SHARE})+1, COLUMN({DIV_PER_SHARE}))):INDIRECT(ADDRESS({FINAL_ROW}, COLUMN({DIV_PER_SHARE})))))')),
        ('TOTAL_DIVIDEND', ('Total dividends', '={TOT_DIV_PER_SHARE}*{AMOUNT}')),
        ('DIV_RUNNING', ('Dividend running total', '=SUM(INDIRECT(ADDRESS({FIRST_ROW},COLUMN({TOTAL_DIVIDEND}))):{TOTAL_DIVIDEND})')),
    ])

    order = cells.keys()
    DATE = order.index('DATE')
    TYPE = order.index('TYPE')
    AMOUNT = order.index('AMOUNT')
    PRICE = order.index('PRICE')
    FEES = order.index('FEES')

    cur_row = 0

    header_format = workbook.add_format({'text_wrap': True,
                                         'bold': True,
                                         'font_color': 'white',
                                         'bg_color': 'black',
                                         'valign': 'vcenter'})

    # Write header
    for i, key in enumerate(cells):
        worksheet.write(cur_row, i, cells[key][0], header_format)

    cur_row += 1

    date_format = workbook.add_format({'num_format': 'dd/mm/yy'})

    for row in records:
        # Write non-formula fields
        worksheet.write_datetime(cur_row, DATE, row['date'], date_format)
        worksheet.write(cur_row, TYPE, row['type'])
        worksheet.write(cur_row, AMOUNT, row['amount'])
        worksheet.write(cur_row, PRICE, row['price'])
        worksheet.write(cur_row, FEES, row['fee'])

        # Write formula fields
        A1_DICT = dict([(x, xl_rowcol_to_cell(cur_row, i)) for i, x in enumerate(cells)])
        A1_DICT['AMOUNT_ZERO'] = xl_rowcol_to_cell(2, AMOUNT)
        A1_DICT['FIRST_ROW'] = 2
        A1_DICT['FINAL_ROW'] = len(records) + 1

        for cell in cells:
            if cells[cell][1] is not None:
                tmp_cell = cells[cell][1].format(**A1_DICT)
                print(tmp_cell)
                worksheet.write(A1_DICT[cell], tmp_cell)
        cur_row += 1

    # Write aggregated fields

workbook = xlsxwriter.Workbook('stocks.xlsx')
records = [{'date': datetime.datetime.strptime('2013-01-23', '%Y-%m-%d'),
            'type': 'BUY',
            'amount': 100,
            'price': 2.17,
            'fee': 30
           }]
build_worksheet(workbook, 'FNZ', records)
workbook.close()

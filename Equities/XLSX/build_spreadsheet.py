import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from collections import OrderedDict

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
    ])

    DATE = cells.index('DATE')
    TYPE = cells.index('TYPE')
    AMOUNT = cells.index('AMOUNT')
    PRICE = cells.index('PRICE')
    FEES = cells.index('FEES')

    for row in records:
        # Write non-formula fields
        worksheet.write_datetime(cur_row, DATE, row['date'])
        worksheet.write(cur_row, TYPE, row['type'])
        worksheet.write(cur_row, AMOUNT, row['amount'])
        worksheet.write(cur_row, PRICE, row['price'])
        worksheet.write(cur_row, FEES, row['fee'])

        # Write formula fields
        A1_DICT = dict([(x, xl_rowcol_to_cell(cur_row, i)) for i, x in enumerate(cells)])

        for cell in cells:
            if cells[cell][1] is not None:
                tmp_cell = cells[cell][1].format(**A1_DICT)
                worksheet.write(A1_DICT[cell], tmp_cell)

    # Write aggregated fields

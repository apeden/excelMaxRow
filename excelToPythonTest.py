from openpyxl import load_workbook

try:
    wb = load_workbook("RTQUIC_18_017.xlsx")
except IOError:
    print("Could not open file")


"""
reads from a row and obtaines maximum value
"""

#get sheet
sheet = wb.active
print("sheet")
print(sheet["B9"].value)

rowVals = []
for i in range(4,1000):
    val = sheet.cell(row=13, column=i).value
    if val == None:
        break
    rowVals.append(val)
    
print(max(rowVals))

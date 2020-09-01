# Program to extract a particular row value 
import xlrd
import xlsxwriter
  
loc = ("Respuestas.xlsx") 

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

sheet.cell_value(0, 0)

rows = []

for i in range(sheet.nrows):
    rows.append(sheet.row_values(i))

header = rows[0]

for i in range(1, len(rows)):
    respuesta = rows[i] 
    nombre = respuesta[1]
    
    wb = xlsxwriter.Workbook(".\indv" + '\\'+ nombre + ".xlsx") 
    sheet1 = wb.add_worksheet('Respuestas')

    for i in range(1, len(header)): # First column
        sheet1.write(i-1, 0, header[i])
    
    for i in range(1, len(respuesta)): # Respuesta
        sheet1.write(i-1, 1, respuesta[i])

    # Formatting
    sheet1.set_column('A:A', 100) # 100 column width
    sheet1.set_column('B:B', 20)

    sheet1.conditional_format('B3:B33', {'type': '3_color_scale',
                                         'min_value': 1,
                                         'max_value': 3,
                                         'min_color': "#63BE7B",
                                         'mid_color': "#FFEB84",
                                         'max_color': "#F8696B",
                                         })


    wb.close() 


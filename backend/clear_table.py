from google_sheets import table


worksheets = table.worksheets()
worksheets_names = []
try:
    table.add_worksheet("Test", rows=1, cols=1)
except:
    pass
for worksheet in worksheets:
    if worksheet.title != "Test":
        table.del_worksheet(worksheet)
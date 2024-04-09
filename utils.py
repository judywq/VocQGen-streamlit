import pandas as pd
from io import BytesIO


# Taken from: https://discuss.streamlit.io/t/download-button-for-csv-or-xlsx-file/17385
def to_excel(df: pd.DataFrame):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    # workbook = writer.book
    # worksheet = writer.sheets['Sheet1']
    # format1 = workbook.add_format({'num_format': '0.00'}) 
    # worksheet.set_column('A:A', None, format1)  
    writer.close()
    excel_data = output.getvalue()
    return excel_data

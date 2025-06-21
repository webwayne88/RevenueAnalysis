import zipfile
from io import BytesIO
import re
import pandas as pd

def process_zip_file(zip_buffer: BytesIO) -> dict:
    result = {}
    
    with zipfile.ZipFile(zip_buffer, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            if (not file_name.lower().endswith(('.xls', '.xlsx')) 
                or file_name.endswith('/')):
                continue
            
            if not (match := re.search(r'(?<!\d)(19|20)\d{2}(?!\d)', file_name)):
                continue
            
            year = match.group()
            try:
                with zip_ref.open(file_name) as excel_file:
                    df = pd.read_excel(excel_file, header=None)
                    
                    totals_row = df[df.iloc[:, 0].astype(str).str.contains(
                        "Итоги за год", case=False, na=False)]
                    if totals_row.empty:
                        continue
                    
                    revenue_cols = [col for col in df.columns 
                                  if df[col].astype(str).str.contains(
                                      "Выручка", case=False, na=False).any()]
                    if not revenue_cols:
                        continue
                    
                    revenue_value = totals_row.iloc[0][revenue_cols[0]]
                    if pd.notna(revenue_value):
                        result[year] = float(revenue_value)
            except Exception:
                continue
                
    return result
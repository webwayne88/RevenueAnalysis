import zipfile
from io import BytesIO
import re
import pandas as pd

def process_zip_file(zip_buffer: BytesIO) -> dict:
    result = {}
    with zipfile.ZipFile(zip_buffer, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            try:
                match = re.search(r'(?<!\d)(19|20)\d{2}(?!\d)', file_name)
                if match:
                    year = match.group()
                    with zip_ref.open(file_name) as excel_file:
                        df = pd.read_excel(excel_file)
                        try:
                            revenue = df.loc[df.iloc[:, 0] == "Итоги за год", "Выручка"].values[0]
                            result[year] = float(revenue)
                        except (IndexError, KeyError):
                            continue         
            except (ValueError, IndexError):
                continue
    return result


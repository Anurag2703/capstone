#   Purpose:
#       reads the Excel file, loads the verses into a structure


import pandas as pd

class GitaLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = pd.read_excel("app/gita/Bhagwad_Gita.xlsx", engine='openpyxl')
        self._prepare_data()

    def _prepare_data(self):
        # standardize columns if needed
        self.df.columns = [col.strip().lower() for col in self.df.columns]
        
        # show available columns:
        print("Columns in Gita dataset:", self.df.columns)

    def get_all_verses(self):
        return self.df.to_dict(orient="records")

    def search_by_keyword(self, keyword: str):
        return self.df[self.df['verse'].str.contains(keyword, case=False, na=False)].to_dict(orient="records")
import pandas as pd

class ExcelParser():
    def __init__(self, path) -> None:
        self.path = path
        self.groups = SheetParser(path=path, sheet_name="GROUPS").load_data()
        self.last_sixteen = SheetParser(path=path, sheet_name="2NDROUND").load_data()
        self.quarter_finals = SheetParser(path=path, sheet_name="3RDROUND").load_data()
        self.semi_finals = SheetParser(path=path, sheet_name="4THROUND").load_data()
        self.finals = SheetParser(path=path, sheet_name="5THROUND").load_data()
        self.finals_results = SheetParser(path=path, sheet_name="6THROUND").load_data()

class SheetParser():
    def __init__(self, path, sheet_name) -> None:
        self.path = path
        self.sheet_name = sheet_name

    def load_data(self) -> pd.DataFrame:
        data_frame = pd.read_excel(self.path, sheet_name=self.sheet_name, index_col=0)
        return data_frame
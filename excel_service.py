import openpyxl


class ExcelService:

    _workbook = None
    _sheet = None

    def get_sheet(self):
        return self._sheet

    def set_workbook(self, workbook: openpyxl.Workbook) -> None:
        self._workbook = workbook

    def get_workbook(self) -> openpyxl.Workbook | None:
        return self._workbook

    def set_sheet(self, sheet) -> None:
        self._sheet = sheet

    def load_file(self, filename: str) -> None:
        workbook: openpyxl.Workbook = openpyxl.load_workbook(filename=filename)

        self.set_workbook(workbook)
        self.set_sheet(workbook.active)

    def write_file(self, row: int, column: int, value: str) -> None:
        cell = self._sheet.cell(row=row, column=column)

        cell.value = value

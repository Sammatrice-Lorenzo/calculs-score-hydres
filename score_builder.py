from generate_score_I import GenerateScoreI
from calculate_score_M import GenerateScoreM
from calculate_score_T_E import GenerateScoreTOrE
from columns_keys import (
    COLUMN_COMPARAISON_LONG_BODY,
    COLUMN_COMPARAISON_LONG_BODY_TRIPLICAT,
    COLUMN_NUMBER_OF_TENTACLES_UPPER_A_HALF_LONG_BODY_TRIPLICAT,
    COLUMN_NUMBER_OF_TENTACLES_UPPER_A_LONG_BODY_CTRL,
    COLUMN_SCORE_E,
    COLUMN_SCORE_I,
    COLUMN_SCORE_M,
    COLUMN_SCORE_T,
    COLUMN_NUMBER_OF_TENTACLES_UPPER_A_HALF_LONG_BODY
)
from excel_service import ExcelService


class ScoreBuilder:

    def __init__(self):
        self.excel_service: ExcelService = ExcelService()

    def load_service(self, sheet) -> None:
        self.score_calculator_T_E = GenerateScoreTOrE(sheet)
        self.score_calculator_I = GenerateScoreI(sheet)
        self.score_calculator_M = GenerateScoreM(sheet)

    def calculate(self, filename: str, total_row: int):
        self.excel_service.load_file(filename=filename)
        sheet = self.excel_service.get_sheet()
        self.load_service(sheet)

        for i in range(2, total_row + 1):
            cell_N = sheet.cell(
                row=i,
                column=COLUMN_NUMBER_OF_TENTACLES_UPPER_A_LONG_BODY_CTRL
            ).value
            cell_O = sheet.cell(
                row=i,
                column=COLUMN_NUMBER_OF_TENTACLES_UPPER_A_HALF_LONG_BODY
            ).value

            cell_J = sheet.cell(
                row=i,
                column=COLUMN_COMPARAISON_LONG_BODY
            ).value

            cell_P = sheet.cell(
                row=i,
                column=COLUMN_NUMBER_OF_TENTACLES_UPPER_A_HALF_LONG_BODY_TRIPLICAT
            ).value

            cell_L = sheet.cell(
                row=i,
                column=COLUMN_COMPARAISON_LONG_BODY_TRIPLICAT
            ).value

            cells = (cell_N, cell_O, cell_J)
            if any(cell is None or isinstance(cell, str) for cell in cells):
                raise ValueError(f"Une ou plusieurs cellules sont invalides à la ligne {i} : {cells}")

            if i > 4 and any(cell is None or isinstance(cell, str) for cell in [cell_P, cell_L]):
                raise ValueError(f"Une ou plusieurs cellules sont invalides à la ligne {i} : {cell_P, cell_L}")

            score_T = self.score_calculator_T_E.get_score_T_or_E(
                row=i,
                total_tentacles_upper=cell_N,
                column_comparaison=cell_J
            )
            score_I = self.score_calculator_I.get_score_I(i, cell_O)
            score_M = self.score_calculator_M.get_score_M(i, cell_O)

            self.excel_service.write_file(i, COLUMN_SCORE_T, score_T)
            self.excel_service.write_file(i, COLUMN_SCORE_I, score_I)
            self.excel_service.write_file(i, COLUMN_SCORE_M, score_M)
            if i > 4:
                score_E = self.score_calculator_T_E.get_score_T_or_E(
                    i,
                    cell_P,
                    cell_L
                )
                self.excel_service.write_file(i, COLUMN_SCORE_E, score_E)

        name = f"{filename.replace('.xlsx', '')}_score_calculated.xlsx"
        self.excel_service.get_workbook().save(name)

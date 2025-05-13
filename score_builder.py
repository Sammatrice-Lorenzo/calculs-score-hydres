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
from services.excel_service import ExcelService


class ScoreBuilder:

    def __init__(self):
        self.excel_service: ExcelService = ExcelService()

    def _load_service(self, sheet) -> None:
        self.score_calculator_T_E = GenerateScoreTOrE(sheet)
        self.score_calculator_I = GenerateScoreI(sheet)
        self.score_calculator_M = GenerateScoreM(sheet)

    def calculate(self, filename: str, total_row: int):
        self.excel_service.load_file(filename=filename)
        sheet = self.excel_service.get_sheet()
        self._load_service(sheet)

        for i in range(2, total_row + 1):
            try:
                values = self._get_row_values(sheet, i)
                self._validate_cells(values, i)
                self._calculate_scores(i, values)
            except ValueError as e:
                print(f"[Erreur] Ligne {i} : {e}")
                continue

        self.excel_service.save_file(filename)

    def _get_row_values(self, sheet, row: int) -> dict:
        return {
            "cell_N": sheet.cell(
                row=row,
                column=COLUMN_NUMBER_OF_TENTACLES_UPPER_A_LONG_BODY_CTRL
            ).value,
            "cell_O": sheet.cell(
                row=row,
                column=COLUMN_NUMBER_OF_TENTACLES_UPPER_A_HALF_LONG_BODY
            ).value,
            "cell_J": sheet.cell(
                row=row,
                column=COLUMN_COMPARAISON_LONG_BODY).value,
            "cell_P": sheet.cell(
                row=row,
                column=COLUMN_NUMBER_OF_TENTACLES_UPPER_A_HALF_LONG_BODY_TRIPLICAT
            ).value,
            "cell_L": sheet.cell(
                row=row,
                column=COLUMN_COMPARAISON_LONG_BODY_TRIPLICAT
            ).value,
        }

    def _validate_cells(self, values: dict, row: int):
        core_cells = (values["cell_N"], values["cell_O"], values["cell_J"])
        if any(cell is None or isinstance(cell, str) for cell in core_cells):
            raise ValueError(f"Cellules de base invalides : {core_cells}")

        if row > 4:
            extra_cells = (values["cell_P"], values["cell_L"])
            if any(cell is None or isinstance(cell, str) for cell in extra_cells):
                raise ValueError(f"Cellules supplémentaires invalides : {extra_cells}")

    def _calculate_scores(self, row: int, values: dict):
        score_T = self.score_calculator_T_E.get_score_T_or_E(
            row=row,
            tentacles_surpass_half_body=values["cell_N"],
            column_comparaison=values["cell_J"]
        )
        score_I = self.score_calculator_I.get_score_I(row, values["cell_O"])
        score_M = self.score_calculator_M.get_score_M(row, values["cell_O"])

        self.excel_service.write_file(row, COLUMN_SCORE_T, score_T)
        self.excel_service.write_file(row, COLUMN_SCORE_I, score_I)
        self.excel_service.write_file(row, COLUMN_SCORE_M, score_M)

        if row > 4:
            score_E = self.score_calculator_T_E.get_score_T_or_E(
                row,
                values["cell_P"],
                values["cell_L"]
            )
            self.excel_service.write_file(row, COLUMN_SCORE_E, score_E)

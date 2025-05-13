from typing import Optional
from columns_keys import (
    COLUMN_BASAL_DISC,
    COLUMN_HEALING,
    COLUMN_HYDRA_DISINTEGRATED,
    COLUMN_MOUNTH,
    COLUMN_NUMBER_TOTAL_OF_TENTACLES,
    COLUMN_START_TENTACLES
)


class HydraRulesService:

    @staticmethod
    def is_case_not_well_formed(
        cell_D: int,
        cell_E: int,
        cell_F: int
    ) -> bool:
        return cell_D == 0 and cell_E == 0 and cell_F == 0

    @staticmethod
    def is_hydra_disintegrated(cell_C: int) -> bool:
        return cell_C == 1

    @staticmethod
    def hydra_not_have_mouth(cell_D: int) -> bool:
        return cell_D == 0

    @staticmethod
    def has_healing(cell_G: int) -> bool:
        return cell_G == 0

    @staticmethod
    def has_more_tentacles(cell_M: int) -> bool:
        return cell_M > 0

    @staticmethod
    def is_above_average_body(column_comparaison: int) -> bool:
        return column_comparaison == 1

    @staticmethod
    def has_basal_disc(sheet, row: int) -> bool:
        cell_D = sheet.cell(row=row, column=COLUMN_MOUNTH).value
        cell_E = sheet.cell(row=row, column=COLUMN_BASAL_DISC).value
        cell_F = sheet.cell(row=row, column=COLUMN_START_TENTACLES).value

        return HydraRulesService.hydra_not_have_mouth(cell_D) and cell_E == 1 and cell_F == 0

    @staticmethod
    def is_hydra_complete(
        sheet,
        row: int,
        tentacles_surpass_half_body: int
    ) -> bool:
        has_basal_disc: bool = HydraRulesService.has_basal_disc(
            sheet,
            row
        )

        cell_M = sheet.cell(
            row=row,
            column=COLUMN_NUMBER_TOTAL_OF_TENTACLES
        ).value

        has_more_tentacles: bool = HydraRulesService.has_more_tentacles(
            cell_M
        )

        return (
            has_basal_disc and has_more_tentacles and tentacles_surpass_half_body == 0
        )

    @staticmethod
    def has_started_tentacles(cell_D: int, cell_E: int, cell_F: int) -> bool:
        return HydraRulesService.hydra_not_have_mouth(cell_D) and cell_E == 0 and cell_F == 1

    def calculate_score_base_conditions(
        self,
        sheet,
        row: int
    ) -> Optional[int]:
        """Calculate score 0 to 4
        """
        cell_C = sheet.cell(
            row=row,
            column=COLUMN_HYDRA_DISINTEGRATED
        ).value
        cell_G = sheet.cell(row=row, column=COLUMN_HEALING).value
        cell_D = sheet.cell(row=row, column=COLUMN_MOUNTH).value
        cell_E = sheet.cell(row=row, column=COLUMN_BASAL_DISC).value
        cell_F = sheet.cell(row=row, column=COLUMN_START_TENTACLES).value

        if None in (cell_C, cell_G):
            raise Exception(f"Problème sur la ligne {row}")

        hydra_not_have_mouth: bool = HydraRulesService.hydra_not_have_mouth(
            cell_D
        )

        is_hydra_not_well_formed: bool = HydraRulesService.is_case_not_well_formed(
            cell_D,
            cell_E,
            cell_F
        )
        has_basal_disc: bool = HydraRulesService.has_basal_disc(
            sheet,
            row
        )
        has_started_tentacles: bool = HydraRulesService.has_started_tentacles(
            cell_D,
            cell_E,
            cell_F
        )

        if HydraRulesService.is_hydra_disintegrated(cell_C):
            return 0

        if is_hydra_not_well_formed and HydraRulesService.has_healing(cell_G):
            return 1

        # Default cell_G has 1
        score: float | None = None
        if is_hydra_not_well_formed and not HydraRulesService.has_healing(cell_G):
            score = 2
        elif has_basal_disc or has_started_tentacles:
            score = 3
        elif hydra_not_have_mouth and cell_E == 1 and cell_F == 1:
            score = 4

        return score
